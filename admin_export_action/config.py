# -*- coding: utf-8 -*-
from django.conf import settings

default_config = {
    'ADMIN_SITE_PATH': None,
    'ENABLE_SITEWIDE': True,
    'VALUE_TO_XLSX_CELL': None,
}


def get_config(key):
    user_settings = getattr(settings, 'ADMIN_EXPORT_ACTION', None)

    if user_settings is None:
        value = default_config.get(key, None)
    else:
        value = user_settings.get(key, default_config.get(key, None))

    return value
