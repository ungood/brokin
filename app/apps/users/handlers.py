# -*- coding: utf-8 -*-
import logging

from tipfy import request, redirect, redirect_to
from tipfy.ext import auth
from tipfy.ext import session

from models import CustomUser
from utils import validation, handlers

class LogoutHandler(handlers.BaseHandler):
    def get(self):
        auth.get_auth_system().logout()
        return redirect_to('index')
        

class LoginHandler(handlers.BaseHandler):
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
        
        
class RegisterHandler(handlers.BaseHandler):
    error = None

    def get(self, **kwargs):
        context = {
            'error': self.error,
        }
        return self.render_response('users/register.html', **context)

    def post(self, **kwargs):
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm  = request.form.get('confirm_password', '').strip()

        try:
            user = CustomUser.register('own', username, password, confirm, email)
            return redirect(request.args.get('redirect', '/'))
        except validation.ValidationError, e:
            self.error = e
            return self.get()
            