# -*- coding: utf-8 -*-
import logging

from tipfy import request, redirect, redirect_to
from tipfy.ext import auth
from tipfy.ext import session

from utils.handlers import BaseHandler
from models import CustomUser
from forms import RegistrationForm

class LogoutHandler(BaseHandler):
    def get(self):
        auth.get_auth_system().logout()
        return redirect_to('index')
        

class LoginHandler(BaseHandler):
    error = None
    
    def get(self):
        # Logged in users don't need to log in twice.
        if auth.get_current_user() is not None:
            return redirect(request.args.get('redirect', '/'))
        
        from tipfy.ext.auth import model
        logging.debug(model.User.all().fetch(1))
        
        context = {
            'error'      : self.error,
        }
        
        return self.render_response('users/login.html', **context)
        
    def post(self):
        # Logged in users don't need to log in twice.
        if auth.get_current_user() is not None:
            return redirect(request.args.get('redirect', '/'))
            
        # todo: use forms and stuff, k?
        # validation!
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        remember = request.form.get('remember', '') == 'y'
        
        try:
            CustomUser.login(username, password, remember)
        except validation.ValidationError, e:
            self.error = e

        return self.get()
        
        
class RegisterHandler(BaseHandler):
    def _get(self, form):
        context = {
            'form': form
        }
        return self.render_response('users/register.html', **context)
    
    def get(self, **kwargs):
        return self._get(RegistrationForm())

    def post(self, **kwargs):
        form = RegistrationForm(request.form)
        if form.validate():
            user = CustomUser.register('own',
                                       form.username.data,
                                       form.password.data,
                                       form.confirm.data,
                                       form.email.data)
            return redirect(request.args.get('redirect', '/'))
        
        return self._get(form)
                    