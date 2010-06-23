# -*- coding: utf-8 -*-
from tipfy import Rule


def get_rules():
    """Returns a list of URL rules for the Hello, World! application."""
    handlers = 'apps.drawing.handlers.'
    rules = [
        Rule('/post/<post_key>',    handler=handlers + 'ViewPostHandler',  endpoint='view-post'),
        Rule('/image/<image_key>',  handler=handlers + 'ViewImageHandler', endpoint='view-image'),
        Rule('/post/new',           handler=handlers + 'NewPostHandler',   endpoint='new-post')
    ]

    return rules
