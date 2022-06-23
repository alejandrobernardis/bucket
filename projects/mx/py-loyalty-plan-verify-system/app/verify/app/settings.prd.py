#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 02/Dec/2013 16:16

import os
from addicted.verify.ui_modules.admin import ViewUsersModule, \
    ViewRegisterModule
from addicted.verify.ui_modules.common import ViewErrorsModule, \
    ViewSearchResultModule

# Root Path
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

# Application
DEBUG = False
TRACK = True
PORT = 8000
SSL = False
CDN_PREFIX = None
PREFORK_PROCESS = 0
XSRF_COOKIE = True
COOKIE_SECRET = 'U2F!dGVkX18mMCwdcu1@zaakCU$4iNx#zNFL0Q+o4ev5u&S1Wre^N54JMT1Uk='
COOKIE_SESSION = 'session'
LOGIN_URL = '/auth/signin'

# Applications
HANDLERS_LIST = (
    'addicted.verify.handlers.auth',
    'addicted.verify.handlers.common',
    'addicted.verify.handlers.admin',
    'addicted.verify.handlers.services'
)

# Session Engine
SESSION = {
    'engine': 'memcached',
    'servers': ('localhost:11211',),
    'expires': 60 * 10,
    'serializer': 'marshal'
}

# DataBase Engine
DATABASE = {
    'default': {
        'name': 'mx_com_addicted_verify',
        'username': 'mca_socios',
        'password': '',
        'settings': {
            'host': 'localhost',
            'port': 27000,
            'max_pool_size': 250,
            'auto_start_request': True,
            'use_greenlets': False
        }
    }
}

DATABASE_SQL = {
    'default': {
        'dbname': 'mx_com_addicted_concierge',
        'username': 'mca_socios',
        'password': '',
        'host': 'localhost',
        'port': 3306
    }
}

DATABASE_SQL_STRING = \
    'mysql+mysqlconnector://' \
    '%(username)s:%(password)s@%(host)s:%(port)s/%(dbname)s'

# UI Modules
UI_MODULES = {
    'ViewErrors': ViewErrorsModule,
    'ViewSearchResult': ViewSearchResultModule,
    'ViewUsers': ViewUsersModule,
    'ViewRegister': ViewRegisterModule
}

# Email Account
EMAIL = {
    'email': 'no-reply@addicted.com.mx',
    'host': 'email-smtp.us-west-2.amazonaws.com',
    'port': 587,
    'username': '',
    'password': '',
    'use_tls': True
}

EMAIL_VERIFICATION_LIST = [
    'concierge@antara.com.mx',
    'concierge@addicted.com.mx',
    'adenova@kinetiq.com.mx',
    'alejandro.bernardis@kinetiq.com.mx'
]


# Site References
SITE_TITLE = u'addicted / verificación de socios'
SITE_DESCRIPTION = ''
SITE_DOMAIN = 'socios.addicted.com.mx'
SITE_ROOT = '/'
SITE_STATIC = SITE_ROOT + 'static'
SITE_GOOGLE_ANALYTICS = 'UA-47596137-2'

# Paths
CA_PATH = os.path.join(ROOT_PATH, 'CA')
STATIC_PATH = os.path.abspath(os.path.join(ROOT_PATH, '../../public/static'))
TEMPLATES_PATH = os.path.join(ROOT_PATH, 'templates')
TEMP_PATH = '/tmp'

# Autoreload
AUTORELOAD_ENABLED = True
AUTORELOAD_FILES = ()

# Static Files
STATIC_FILES = ()
