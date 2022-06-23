#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 28/Apr/2014 13:17

import os
import sys


# Root Path
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
_parent_path = os.path.split(ROOT_PATH)[0]


for folder in ('../../bin', '../../lib', '../tasks'):
    folder_path = os.path.abspath(os.path.join(_parent_path, folder))
    if os.path.isdir(folder_path):
        sys.path.insert(0, folder_path)


# Application
DEBUG = True
TRACK = False
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
    'com.feedback.handlers.auth',
    'com.feedback.handlers.common',
    'com.feedback.handlers.admin',
    'com.feedback.handlers.public',
    'com.feedback.handlers.services'
)

# Session Engine
SESSION = {
    'engine': 'memcached',
    'servers': ('localhost:11211',),
    'expires': 60 * 60 * 10,
    'serializer': 'marshal'
}

# DataBase Engine
DATABASE = {
    'default': {
        'name': 'mx_com_feedback',
        'username': '',
        'password': '',
        'settings': {
            'host': 'localhost',
            'port': 27017,
            'max_pool_size': 250,
            'auto_start_request': True,
            'use_greenlets': False
        }
    }
}

DATABASE_SQL = {
    'default': {
        'dbname': 'mx_com_feedback',
        'username': 'root',
        'password': 'root',
        'host': 'localhost',
        'port': 3306
    }
}

DATABASE_SQL_STRING = \
    'mysql+mysqlconnector://' \
    '%(username)s:%(password)s@%(host)s:%(port)s/%(dbname)s'

# UI Modules
UI_MODULES = {
    'ViewErrors': 
        'com.feedback.ui_modules.common.ViewErrorsModule',
    'ViewSearchResult': 
        'com.feedback.ui_modules.common.ViewSearchResultModule',
    'ViewEvaluations': 
        'com.feedback.ui_modules.admin.ViewEvaluationsModule',
    'ViewMyEvaluations': 
        'com.feedback.ui_modules.common.ViewMyEvaluationsModule',
    'ViewMyEvaluationsPending': 
        'com.feedback.ui_modules.common.ViewMyEvaluationsPendingModule',
    'ViewUsers': 
        'com.feedback.ui_modules.admin.ViewUsersModule',
    'ViewRegister': 
        'com.feedback.ui_modules.admin.ViewRegisterModule',
    'ViewExecutives': 
        'com.feedback.ui_modules.admin.ViewExecutivesModule'
}

# Email Account
# TODO: CONFIGURAR EL SMTP DE PRODUCCION, COMO ASÍ TAMBIÉN LA CUENTA DE ENVÍO
EMAIL = {
    'email': 'alejandro.bernardis@figment.com.mx',
    'host': 'smtp.gmail.com',
    'port': 587,
    'username': 'loyalty.figment@gmail.com',
    'password': 'fG+L0y@lTy-14.3',
    'use_tls': True
}

EMAIL_VERIFICATION_LIST = [
    'alejandro.bernardis@figment.com.mx'
]


# Site References
SITE_TITLE = u'Feedback'
SITE_DESCRIPTION = ''
SITE_DOMAIN = ''
SITE_ROOT = '/'
SITE_STATIC = SITE_ROOT + 'static'
SITE_GOOGLE_ANALYTICS = ''

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