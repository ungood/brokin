# -*- coding: utf-8 -*-
import logging
from tipfy import request, RequestHandler
from tipfy.ext import auth, session, jinja2

from keys import KeyGenerator
from google.appengine.ext import db

key_generator = KeyGenerator(20)

class BaseHandler(RequestHandler, jinja2.Jinja2Mixin, session.SessionMixin):
    def dispatch(self, *args, **kwargs):
        """Sets up a lot of common context variables as well as session stuff."""
                
        if self.session and self.session.get('key') == None:
            self.session['key'] = key_generator.create_key()
        
        self.context = self.context or {}
        self.context['user']        = auth.get_current_user()
        self.context['signup_url']  = auth.create_signup_url(request.url)
        self.context['login_url']   = auth.create_login_url(request.url)
        self.context['logout_url']  = auth.create_logout_url(request.url)
        
        return RequestHandler.dispatch(self, *args, **kwargs)
        