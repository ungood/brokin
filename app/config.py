# -*- coding: utf-8 -*-
import os, logging

config = {}

is_dev = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

# Configurations for the 'tipfy' module.
config['tipfy'] = {
    'dev': is_dev,
    
    'middleware': [
        'tipfy.ext.debugger.DebuggerMiddleware',
        'tipfy.ext.session.SessionMiddleware',
        'tipfy.ext.auth.AuthMiddleware',
    ],
    
    'apps_installed': [
        'apps.users',
        'apps.drawing',
    ]
}

config['tipfy.ext.auth'] = {
    'auth_system'       : 'tipfy.ext.auth.MultiAuth',
    'cookie_key'        : 'brokin-auth',
    'user_model'        : 'apps.users.models.CustomUser',
    'cookie_httponly'   : True
}

config['tipfy.ext.session'] = {
    'session_type'        : 'securecookie',
    'session_cookie_name' : 'brokin-session',
    'secret_key'          : 'vujEvdanyunholyoircEujimreshDyodhacmyzquajryerckAushrenOyWra',
}


