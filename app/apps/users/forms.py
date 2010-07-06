# -*- coding: utf-8 -*-
import tipfy
from tipfy.ext.wtforms.form import Form
from tipfy.ext.wtforms.fields import RecaptchaField

from wtforms.validators import *
from wtforms.fields import *

from models import CustomUser

reserved_names = tipfy.get_config('apps.users', 'reserved_usernames')
username_regex = r'^\s*(\w+)\s*$'

def username_check(form, field):
    if CustomUser.get_by_username(field.data):
        raise ValidationError(u'Username is already taken.')
        
def login_validator(form, field):
    if not CustomUser.login(form.username.data, form.password.data, form.remember.data):
        raise ValidationError(u'Username and password do not match.')
    

class RegistrationForm(Form):
    username = TextField('Username', [
        Required(),
        Length(min=4, max=25),
        NoneOf(reserved_names, message=u'Username is reserved.'),
        Regexp(username_regex, message=u'Username must be alphanumeric.'),
        username_check
    ])
    
    email = TextField('Email', [
        Required(),
        Length(min=6, max=35)
    ])
    
    password = PasswordField('Password', [
        Required(),
        Length(min=4, max=500),
        EqualTo('confirm', 'Passwords must match.')
    ])
    
    confirm = PasswordField('Confirm Password')
        
    captcha  = RecaptchaField('Human Test')
    
class LoginForm(Form):
    username = TextField('Username', [
        Required(),
        Length(max=500)
    ])
    
    password = PasswordField('Password', [
        Required(),
        Length(max=500),
        login_validator
    ])
    
    remember = BooleanField('Remember Me')
    
    
    
    
