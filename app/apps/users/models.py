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
    
    #@classmethod
    #def get_by_username(cls, username):
    #    return CustomUser.all(keys_only=True).filter('username=', username.lower()).get()
    
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