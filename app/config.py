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

config['tipfy.ext.wtforms'] = {
    'recaptcha_options'    : {
        'theme'            : 'red'
    },
    'recaptcha_use_ssl'    : False,
    'recaptcha_public_key' : '6LdNB7sSAAAAAPu5dRf2lV7X0TCQYO-exvzwhOUZ' if is_dev else '6LfrBrsSAAAAAChxU_tpTe6AcOy4CQsz1on2NpCk',
    'recaptcha_private_key': '6LdNB7sSAAAAAMUZ9vhcJWu4fT7lZq00qwW9zhi1' if is_dev else '6LfrBrsSAAAAAArQnAjvbVj18vxm9LKChrrPslvw',
}

