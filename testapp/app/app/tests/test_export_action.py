# -- encoding: UTF-8 --
import json

from admin_export_action import report
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from news.models import Attachment, Category, News, NewsTag, Video


class AdminExportActionTest(TestCase):
    fixtures = ["tests.json"]

    def test_get_field_verbose_name(self):
        res = report.get_field_verbose_name(News.objects, 'tags__name')
        assert res == 'all tags verbose name'

    def test_list_to_method_response_should_return_200_and_correct_values(
            self):
        admin = User.objects.get(pk=1)
        data, messages = report.report_to_list(News.objects.all(),
                                               ['id', 'title', 'status'],
                                               admin)
        method = getattr(report, 'list_to_{}_response'.format('html'))
        res = method(data)
        assert res.status_code == 200

        method = getattr(report, 'list_to_{}_response'.format('csv'))
        res = method(data)

        assert res.status_code == 200
        assert res.content == b'1,Lucio Dalla,published\r\n2,La mano de Dios,draft\r\n'

        method = getattr(report, 'list_to_{}_response'.format('xlsx'))
        res = method(data)
        assert res.status_code == 200

        method = getattr(report, 'list_to_{}_response'.format('json'))
        res = method(data, header=['id', 'title', 'status'])
        d = json.loads(res.content)
        assert d[0]['id'] == 1
        assert d[0]['title'] == "Lucio Dalla"
        assert d[0]['status'] == 'published'
        assert d[1]['id'] == 2
        assert d[1]['title'] == "La mano de Dios"
        assert d[1]['status'] == 'draft'
        assert res.status_code == 200

        data, messages = report.report_to_list(News.objects.all(),
                                               ['id', 'title', 'status'],
                                               admin,
                                               raw_choices=True)

        method = getattr(report, 'list_to_{}_response'.format('json'))
        res = method(data, header=['id', 'title', 'status'])
        d = json.loads(res.content)
        assert d[0]['id'] == 1
        assert d[0]['title'] == "Lucio Dalla"
        assert d[0]['status'] == 2
        assert d[1]['id'] == 2
        assert d[1]['title'] == "La mano de Dios"
        assert d[1]['status'] == 1
        assert res.status_code == 200

    def test_list_to_csv_response_should_have_expected_content(self):
        admin = User.objects.get(pk=1)
        data, messages = report.report_to_list(News.objects.all(),
                                               ['id', 'title'], admin)

        method = getattr(report, 'list_to_{}_response'.format('csv'))
        res = method(data)

        assert res.status_code == 200
        assert res.content == b'1,Lucio Dalla\r\n2,La mano de Dios\r\n'

    def test_list_to_json_response_should_have_expected_content(self):
        admin = User.objects.get(pk=1)
        data, messages = report.report_to_list(News.objects.all(),
                                               ['id', 'title'], admin)

        method = getattr(report, 'list_to_{}_response'.format('json'))
        res = method(data, header=['id', 'title'])
        d = json.loads(res.content)
        assert d[0]['id'] == 1
        assert d[0]['title'] == "Lucio Dalla"
        assert d[1]['id'] == 2
        assert d[1]['title'] == "La mano de Dios"
        assert res.status_code == 200

    def test_admin_export_post_should_return_200(self):
        for output_format in ['html', 'csv', 'xslx', 'json']:
            params = {
                'ct':
                ContentType.objects.get_for_model(News).pk,
                'ids':
                ','.join(
                    repr(pk)
                    for pk in News.objects.values_list('pk', flat=True))
            }
            data = {
                "title": "on",
                "__format": output_format,
            }
            url = "{}?{}".format(reverse('admin_export_action:export'),
                                 urlencode(params))
            self.client.login(username='admin', password='admin')
            response = self.client.post(url, data=data)
            assert response.status_code == 200

    def test_admin_export_get_should_return_200(self):
        params = {
            'ct':
            ContentType.objects.get_for_model(News).pk,
            'ids':
            ','.join(
                repr(pk) for pk in News.objects.values_list('pk', flat=True))
        }
        url = "{}?{}".format(reverse('admin_export_action:export'),
                             urlencode(params))
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        assert response.status_code == 200

    def test_admin_export_with_related_get_should_return_200(self):
        params = {
            'related': True,
            'model_ct': ContentType.objects.get_for_model(News).pk,
            'field': 'category',
            'path': 'category.name',
        }
        url = "{}?{}".format(reverse('admin_export_action:export'),
                             urlencode(params))
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)
        assert response.status_code == 200

    def test_admin_export_with_related_of_indirect_field_get_should_return_200(
            self):
        params = {
            'related': True,
            'model_ct': ContentType.objects.get_for_model(News).pk,
            'field': 'newstag',
            'path': 'newstag.id',
        }
        url = "{}?{}".format(reverse('admin_export_action:export'),
                             urlencode(params))
        self.client.login(username='admin', password='admin')
        response = self.client.get(url)

        assert response.status_code == 200

    def test_admin_export_with_unregistered_model_should_raise_ValueError(
            self):
        params = {
            'ct':
            ContentType.objects.get_for_model(NewsTag).pk,
            'ids':
            ','.join(
                repr(pk)
                for pk in NewsTag.objects.values_list('pk', flat=True))
        }
        url = "{}?{}".format(reverse('admin_export_action:export'),
                             urlencode(params))

        self.client.login(username='admin', password='admin')
        try:
            self.client.get(url)
            self.fail()
        except ValueError:
            pass

    def test_admin_action_should_redirect_to_export_view(self):
        objects = News.objects.all()

        ids = [repr(obj.pk) for obj in objects]
        data = {
            "action": "export_selected_objects",
            "_selected_action": ids,
        }
        url = reverse('admin:news_news_changelist')
        self.client.login(username='admin', password='admin')
        response = self.client.post(url, data=data)

        expected_url = "{}?ct={ct}&ids={ids}".format(
            reverse('admin_export_action:export'),
            ct=ContentType.objects.get_for_model(News).pk,
            ids=','.join(reversed(ids)))
        assert response.status_code == 302
        assert response.url.endswith(expected_url)

    def test_export_with_related_should_return_200(self):
        for output_format in ['html', 'csv', 'xslx', 'json']:
            news = News.objects.all()

            params = {
                'ct':
                ContentType.objects.get_for_model(News).pk,
                'ids':
                ','.join(
                    repr(pk)
                    for pk in News.objects.values_list('pk', flat=True))
            }
            data = {
                'id': 'on',
                'title': 'on',
                'status': 'on',
                'category__name': 'on',
                'tags__name': 'on',
                'newstag__created_on': 'on',
                "__format": output_format,
            }
            url = "{}?{}".format(reverse('admin_export_action:export'),
                                 urlencode(params))
            self.client.login(username='admin', password='admin')
            response = self.client.post(url, data=data)
            assert response.status_code == 200
            assert response.content
