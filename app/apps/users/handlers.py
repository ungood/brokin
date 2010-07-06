# -*- coding: utf-8 -*-
import logging

from tipfy import request, redirect, redirect_to

from utils.handlers import BaseHandler
from models import CustomUser
from forms import RegistrationForm, LoginForm

class LogoutHandler(BaseHandler):
    def get(self):
        CustomUser.logout()
        return redirect_to('index')
        

class LoginHandler(BaseHandler):
    def _get(self, form):
        context = {
            'form': form
        }
        return self.render_response('users/login.html', **context)
    
    def get(self):
        # Logged in users don't need to log in twice.
        if CustomUser.get_current_user() is not None:
            return redirect(request.args.get('redirect', '/'))
        
        return self._get(LoginForm())
        
    def post(self):
        # Logged in users don't need to log in twice.
        if CustomUser.get_current_user() is not None:
            return redirect(request.args.get('redirect', '/'))
        
        form = LoginForm(request.form)
        if form.validate():
            return redirect(request.args.get('redirect', '/'))
        else:
            return self._get(form)
                
        
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
           
        
        return self._get(form)
                    