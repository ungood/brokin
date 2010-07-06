# -*- coding: utf-8 -*-
import logging

from google.appengine.ext import db

import tipfy
from tipfy.ext import auth
from tipfy.ext.auth.model import User

USER_TYPES = ['own']

class CustomUser(User):
    user_type = db.StringProperty(required=True, choices=USER_TYPES)
    
    # This is the username as originally entered by the user.  We have to keep
    # this separate so we can store the lowercase username in `username`.  That
    # way we don't have "ungood", "ungOOd", and "ungOod" as separate users.
    formatted_username = db.StringProperty(required=True)
    
    @property
    def key_name(self):
        return self.key().name()
    
    @property
    def karma(self):
        return statistics.Counter('karma', self.key_name)
    
    @classmethod
    def register(cls, type, username, password, confirm, email):
        """Creates a new user and returns it.  Raises a validation error if unsuccessful."""
        formatted = username
        username = username.lower()
        auth_id = '%s|%s' % (type, username) # Create a unique auth id for this user.

        # Set the properties of our user.
        kwargs = {
            'email'              : email,
            'password'           : password,
            'user_type'          : type,
            'formatted_username' : formatted
        }
        logging.debug('Creating user: %s' % username)
        return auth.get_auth_system().create_user(username, auth_id, **kwargs)
    
    @classmethod
    def login(cls, username, password, remember):
        username = username.lower()
        if not auth.get_auth_system().login_with_form(username, password, remember):
            raise validation.BadFormatError('Username or password are not correct.')
    
    @classmethod
    def logout(cls):
        auth.get_auth_system().logout()
        
    @classmethod
    def get_current_user(cls):
        return auth.get_current_user()