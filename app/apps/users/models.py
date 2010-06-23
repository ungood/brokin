# -*- coding: utf-8 -*-
import logging

from google.appengine.ext import db

import tipfy
from tipfy.ext import auth
from tipfy.ext.auth.model import User

from utils import validation

USER_TYPES = ['own']

class CustomUser(User):
    user_type = db.StringProperty(required=True, choices=USER_TYPES)
    
    # This is the username as originally entered by the user.  We have to keep
    # this separate so we can store the lowercase username in `username`.  That
    # way we don't have "ungood", "ungOOd", and "ungOod" as separate users.
    formatted_username = db.StringProperty(required=True)
    
    @classmethod
    def register(cls, type, username, password, confirm, email):
        """Creates a new user and returns it.  Raises a validation error if unsuccessful."""
        
        reserved_names = tipfy.get_config('apps.users', 'reserved_usernames')
                    
        if type not in USER_TYPES:
            raise validation.BadFormatError('Invalid user type.')
                    
        if not username:
            raise validation.MissingValueError('Username is required.')
        
        formatted = username
        username = username.lower()
            
        if username in reserved_names:
            raise validation.BadFormatError('That username is not allowed.')
        
        if not password:
            raise validation.MissingValueError('Please provide a password.')
            
        if password != confirm:
            raise validation.BadFormatError('Passwords must match.')
            
        if not email:
            raise validation.MissingValueError('Email is required.')
        
        # Create a unique auth id for this user.
        auth_id = '%s|%s' % (type, username)

        # Set the properties of our user.
        kwargs = {
            'email'              : email,
            'password'           : password,
            'user_type'          : type,
            'formatted_username' : formatted
        }
        logging.debug('%s %s %s %s %s' % (username, password, confirm, email, formatted))
        user = auth.get_auth_system().create_user(username, auth_id, **kwargs)
        if user is None:
            raise validation.BadFormatError('That username already exists.')
            
        return user
    
    @classmethod
    def login(cls, username, password, remember):
        username = username.lower()
        if not auth.get_auth_system().login_with_form(username, password, remember):
            raise validation.BadFormatError('Username or password are not correct.')