# -*- coding: utf-8 -*-
from tipfy import get_config, import_string, Rule


def get_rules():
    rules = [
        Rule('/', handler='apps.handlers.IndexHandler',   endpoint='index'),
    ]

    for app_module in get_config('tipfy', 'apps_installed'):
        try:
            # Load the urls module from the app and extend our rules.
            app_rules = import_string('%s.urls' % app_module)
            rules.extend(app_rules.get_rules())
        except ImportError:
            pass

    return rules
