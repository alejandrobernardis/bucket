#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Asumi Kamikaze Inc.
# Copyright (c) 2012 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Sep 12, 2012 1:41:15 PM
import os

#: root
ROOT_PATH = os.path.dirname(__file__)

#: port
DEBUG = True
PORT = 8000
SSL = False
CDN = False
PREFORK = False
XSRF_COOKIES = True
PKG = 'mx.dip.voj'
PKG_HANDLERS = 'mx.dip.voj.handlers'
PKG_MODELS = 'mx.dip.voj.models'
PKG_MODULES = 'mx.dip.voj.modules'
PKG_DIR = 'mx/dip/voj'
COOKIE_USER_SESSION = 'user_session'

#: handlers
LOGIN_URL = '/auth/login'
HANDLERS_LIST = ['common', 'admin']

#: database (default)
DATABASE_ORM  = True
DATABASE_NAME = 'admin'
DATABASE_USER = 'admin'
DATABASE_PASS = '1G#r+jI2s:1'
DATABASE_HOST = '127.0.0.1'
DATABASE_PORT = 27017
DATABASE_CONN = 100   # poll_size
DATABASE_AREQ = True  # auto_start_request
DATABASE_UGLS = False # greenlets

#: database async
DATABASE_CACH = 10

#: database (others)
DATABASE_MULTIPLE = dict(
    users=dict(
        alias='users-db',
        name='mx-dip-voj-local-users',
        username='admin',
        password='1G#r+jI2s:1',
        host='127.0.0.1',
        port=27017,
        max_pool_size=100,
        auto_start_request=True,
        use_greenlets=False
    ),

    events=dict(
        alias='events-db',
        name='mx-dip-voj-local-events',
        username='admin',
        password='1G#r+jI2s:1',
        host='127.0.0.1',
        port=27017,
        max_pool_size=100,
        auto_start_request=True,
        use_greenlets=False
    ),
)

#: roles
USER_ROLES = dict(
    admin=dict(
        name='admin',
        admin=True
    ),

    moderator=dict(
        name='moderator',
        write=True
    ),

    user=dict(
        name='user'
    ),
)

USER_ROLE_ID = 1

USER_DATA_IGNORE = [
    'policy','remote_ip','terms','activation_key','news','password',
    'secret_answer','available','notes','enabled','secret_question',
    'activation_key_expire','password'
]

USER_DATA_IGNORE_EXTENDS = [
    'policy','remote_ip','terms','activation_key','password',
    'secret_answer','available','notes','enabled','secret_question',
    'activation_key_expire','password','id','role_id','role_name',
    'facebook_uid','twitter_uid'
]

#: email
EMAIL_ACCOUNT = ''
EMAIL_USER = ''
EMAIL_PASS = ''
EMAIL_HOST = 'smtp.google.com'
EMAIL_PORT = 587
EMAIL_TLS = True

#: site
SITE_TITLE = u'#OrgulloJarocho (admin)'
SITE_DESCRIPTION = u'AK-Administrador'
SITE_DOMAIN = 'localhost'
SITE_ROOT = '/'
SITE_STATIC = '/static'
SITE_IMAGE_PAT_EVENTS = '/static/img/events'
SITE_IMAGE_IMG_EVENTS = '/static/img/events/default.jpg'

if DEBUG:
    SITE_STATIC_IMG_EVENTS = '/development/projects/eclipse/mx-dipa-veracruz-orgullo/public/static/img/events'
    SITE_STATIC_DAT_EVENTS = '/development/projects/eclipse/mx-dipa-veracruz-orgullo/public/data/events'
    SITE_TEMP_IMG_EVENTS = '/development/projects/eclipse/mx-dipa-veracruz-orgullo/src/mx/dip/voj/tmp'
else:
    SITE_STATIC_IMG_EVENTS = '/var/www/vhosts/orgullojarocho.mx/httpdocs/static/img/events'
    SITE_STATIC_DAT_EVENTS = '/var/www/vhosts/orgullojarocho.mx/httpdocs/data/events'
    SITE_TEMP_IMG_EVENTS = '/var/www/vhosts/orgullojarocho.mx/backoffice/apps/administrator/mx/dip/voj/tmp'

#: static
STATIC_FILES = [
    r'/(404\.html)',
    r'/(apple-touch-icon\.png)',
    r'/(apple-touch-icon-precomposed\.png)',
    r'/(apple-touch-icon-57x57-precomposed\.png)',
    r'/(apple-touch-icon-72x72-precomposed\.png)',
    r'/(apple-touch-icon-114x114-precomposed\.png)',
    r'/(apple-touch-icon-144x144-precomposed\.png)',
    r'/(channel\.html)',
    r'/(crossdomain\.xml)',
    r'/(favicon\.ico)',
    r'/(humans\.txt)',
    r'/(robots\.txt)',
    r'/(sitemap\.xml)',
    r'/(xd_receiver\.html)'
]
