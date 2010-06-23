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
                
        if self.session and self.session['key'] == None:
            self.session['key'] = key_generator.create_key()
        
        self.context = {
            'user'      : auth.get_current_user(),
            'signup_url': auth.create_signup_url(request.url),
            'login_url' : auth.create_login_url(request.url),
            'logout_url': auth.create_logout_url(request.url),
        }
        
        return RequestHandler.dispatch(self, *args, **kwargs)
        
#def transaction():
#    """Runs a method in a transaction."""
#    def decorator(fxn):
#        def wrapper(*args, **kwargs):
#            return db.run_in_transaction(fxn)
#        return wrapper
#    
#    return decorator