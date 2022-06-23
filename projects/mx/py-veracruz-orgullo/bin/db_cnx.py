#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
pkg = '/bin'
root_path = os.path.dirname(__file__)
sys.path.insert(0, root_path.replace(pkg, '/src'))
sys.path.insert(0, root_path.replace(pkg, '/lib'))
sys.path.insert(0, root_path.replace(pkg, '/libs'))
sys.path.insert(0, '/development/library/python')

# imports
import settings
from mongoengine import connect as mongodb_connect
from mongoengine import register_connection

# database
_database_name = settings.DATABASE_NAME

_database_settings = dict(
    host=settings.DATABASE_HOST,
    port=settings.DATABASE_PORT,
    username=settings.DATABASE_USER,
    password=settings.DATABASE_PASS)

mongodb_connect(_database_name, **_database_settings)

for a in settings.DATABASE_MULTIPLE:
    _cfg = settings.DATABASE_MULTIPLE[a]
    register_connection(**_cfg)
