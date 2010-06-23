# -*- coding: utf-8 -*-
from tipfy import Rule

def get_rules():
    """Returns a list of URL rules for the Hello, World! application."""
    handlers = 'apps.users.handlers.'
    rules = [
        Rule('/login',      handler=handlers + 'LoginHandler',      endpoint='auth/login'),
        Rule('/logout',     handler=handlers + 'LogoutHandler',     endpoint='auth/logout'),
        Rule('/signup',     handler=handlers + 'RegisterHandler',   endpoint='auth/signup')
    ]

    return rules