# -*- coding: utf-8 -*-
import tipfy
from tipfy.ext.wtforms.form import Form
from tipfy.ext.wtforms.fields import RecaptchaField

from wtforms.validators import Required, Length, ValidationError, EqualTo, NoneOf
from wtforms.fields import TextField, PasswordField

from models import CustomUser

reserved_names = tipfy.get_config('apps.users', 'reserved_usernames')

def username_check(form, field):
    if CustomUser.get_by_username(field.data):
        raise ValidationError(u'Username is already taken.')    
    

class RegistrationForm(Form):
    username = TextField('Username', [
        Required(),
        Length(min=4, max=25),
        NoneOf(reserved_names, message=u'Username is reserved.'),
        username_check
    ])
    
    email = TextField('Email', [
        Required(),
        Length(min=6, max=35)
    ])
    
    password = PasswordField('Password', [
        Required(),
        EqualTo('confirm', 'Passwords must match.')
    ])
    
    confirm = PasswordField('Confirm Password')
        
    captcha  = RecaptchaField('Human Test')
    
    
