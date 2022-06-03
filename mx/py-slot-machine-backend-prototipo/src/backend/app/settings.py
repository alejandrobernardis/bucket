#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 21/06/2013 09:01


import os
from casino8.security.base import secret_key


# root
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


# config
DEBUG = True
TRACK = False
IN_APPROVAL = True
PORT = 8000
SSL = False
CDN = False
CDN_PREFIX = None
PREFORK_PROCESS = 0
XSRF_COOKIE = False
COOKIE_SECRET = secret_key()
COOKIE_USER_SESSION = 'user_session'
LOGIN_URL = '/auth/login'
PLATFORMS = ('ipad', 'ipadhd', 'iphone', 'iphonehd', 'android_wvga',)


# handlers
HANDLERS_PKG = 'casino8.handlers'
HANDLERS_LIST = (
    'devices',
    'machines',
    'machines_v2',
    'coins',
    'social',
    'social_redeem',
    'notifications',
    'nags_screen',
    'graph',
)


# session
SESSION = dict(
    engine='memcached',
    servers=('localhost:11211',),
    serializer='marshal',
)


# database (default)
DATABASE_RSET = 'r0'
DATABASE_HURI = 'localhost:27017,'\
                'localhost:27020,'\
                'localhost:27021,'\
                'localhost:27022'
DATABASE_HOST = 'localhost'
DATABASE_PORT = 27017
DATABASE_CONN = 100
DATABASE_AREQ = True
DATABASE_UGLS = False
DATABASE_USER = None
DATABASE_PASS = None


SOCIAL_DATABASE_HOST = 'localhost'
SOCIAL_DATABASE_PORT = 27017
SOCIAL_DATABASE_CONN = 100
SOCIAL_DATABASE_AREQ = True
SOCIAL_DATABASE_UGLS = False
SOCIAL_DATABASE_USER = None
SOCIAL_DATABASE_PASS = None


TRACK_DATABASE_HOST = 'localhost'
TRACK_DATABASE_PORT = 27017
TRACK_DATABASE_CONN = 100
TRACK_DATABASE_AREQ = True
TRACK_DATABASE_UGLS = False
TRACK_DATABASE_USER = None
TRACK_DATABASE_PASS = None


# databases names
DATABASE_NAME = 'c8'           # casino8
DATABASE_TRACK_NAME = 't8'     # tracking8
DATABASE_SOCIAL_NAME = 's8'    # social8
DATABASE_NOTIFY_NAME = 'n8'    # notifications8
DATABASE_GRAPH_NAME = 'g8'     # graph8


# email
EMAIL_ACCOUNT = ''
EMAIL_USER = ''
EMAIL_PASS = ''
EMAIL_HOST = 'smtp.google.com'
EMAIL_PORT = 587
EMAIL_TLS = True


# site
SITE_TITLE = 'Casino 8'
SITE_DESCRIPTION = 'Casino 8'
SITE_DOMAIN = 'app.casino-8.net'
SITE_ROOT = '/'
SITE_STATIC = SITE_ROOT + 'static'


# paths
CA_PATH = os.path.join(ROOT_PATH, 'CA')
STATIC_PATH = os.path.abspath(os.path.join(ROOT_PATH, '../../public/static'))
TEMPLATES_PATH = os.path.join(ROOT_PATH, 'templates')
TEMP_PATH = '/tmp'


# autoreload
AUTORELOAD_ENABLED = True
AUTORELOAD_FILES = ()


# static files
STATIC_FILES = ()


# lang
LANGUAGES_DEFAULT = 'es'
LANGUAGES = (LANGUAGES_DEFAULT, 'en', 'pt')