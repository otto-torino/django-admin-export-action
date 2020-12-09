from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from .views import AdminExport

view = staff_member_required(AdminExport.as_view())

app_name = 'admin_export_action'

urlpatterns = [
    url(r'^export/$', view, name="export"),
]
