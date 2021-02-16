# Django Admin Export Action


![Version](https://img.shields.io/github/v/tag/otto-torino/django-admin-export-action?label=version)
[![Build status](https://travis-ci.com/otto-torino/django-admin-export-action.svg?branch=master)](https://travis-ci.com/github/otto-torino/django-admin-export-action)
![License](https://img.shields.io/github/license/otto-torino/django-admin-export-action)
[![Coverage](https://codecov.io/gh/otto-torino/django-admin-export-action/branch/master/graph/badge.svg)](https://codecov.io/gh/otto-torino/django-admin-export-action)

Export action for Django's Admin

## Quickstart

Install Django Admin Export Action::

``` python
pip install django-admin-export-action
```

Include it in INSTALLED_APPS::

```
INSTALLED_APPS = [
    # ...
    'admin_export_action',
]
```

Add to `urlpatterns` in `urls.py`:

``` python 
path('export_action/', include("admin_export_action.urls", namespace="admin_export_action")),
```

## Configuration

By default the export action will be added sitewide, which means for every app and every admin registered model.

You can disable this behaviour and decide to add manually the export action only for the models you desired:

``` python

# settings.py

ADMIN_EXPORT_ACTION = {
    'ENABLE_SITEWIDE': False
}

# model admin
from admin_export_action.admin import export_selected_objects

class MyModelAdmin(models.ModelAdmin):
    # ...
    actions = [export_selected_objects, ]

```

Convert any value to its xlsx representation can be a nightmare, and you may always find something weird you haven't considered.
In order to let you fix every case, you can define an hook which is called when adding a value to a cell:

``` python

# settings.py

ADMIN_EXPORT_ACTION = {
    'VALUE_TO_XLSX_CELL': 'news.admin.my_convert_function'
}

# admin.py
def my_convert_function(value):
    if (value == 'convert'):
        return True, 'converted'
    elif (type(value) == list):
        return json.dumps(value)
    return False, None
```

If called, the hook is called first, it shoud return a tuple `success, value`. If `success` is `True`, then the returned `value` is used, otherwise the default conversions are performed.

The intermediate admin page used to select the fields to be exported needs the extra context each admin page has. But such context depends on your `admin_site` instance, for example if you use `django-baton` the admin site is different from the default one.    
For this reason you can specify the path for your admin app:

``` python

# settings.py

ADMIN_EXPORT_ACTION = {
    'ADMIN_SITE_PATH': 'baton.autodiscover.admin'
}
```

This assures the site title and site header ar the ones you see in normal admin pages.

## Usage

Go to an admin page where the export action is enabled, select objects, run the action.

In the next page:
- select the fields you want to export
- select the output format
- select whether to get raw choices values or not
- select whether to include table header (field verbose name) or not
- click the "Export" button

## Features

* Generic or ready to use action to enable export data from Admin.
* Automatic traversal of model relations.
* Selection of fields to export.
* Can export to XSLx, CSV, JSON and HTML.

## Running Tests

Does the code actually work?

    cd testapp/app
    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements.txt
    (myenv) $ python manage.py test


## Security

This project assumes staff users are trusted. There may be ways for users to manipulate this project to get more data access than they should have.

## Credits

This project is developed by Otto srl, and originally foked from [fgmacedo/django-export-action](https://github.com/fgmacedo/django-export-action)
