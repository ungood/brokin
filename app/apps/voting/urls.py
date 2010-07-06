# -*- coding: utf-8 -*-
from tipfy import Rule

def get_rules():
    """Returns a list of URL rules for the Hello, World! application."""
    handlers = 'apps.voting.handlers.'
    rules = [
        Rule('/vote/<post_key>/<value>', handler=handlers + 'VoteHandler', endpoint='vote'),
    ]

    return rules