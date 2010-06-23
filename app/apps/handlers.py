# -*- coding: utf-8 -*-
import logging, tipfy

from utils.handlers import BaseHandler
from apps.drawing.models import Post

class IndexHandler(BaseHandler):
    def get(self):
        context = {
            'posts': Post.list_recent()
        }
        
        return self.render_response('index.html', **context)
        
