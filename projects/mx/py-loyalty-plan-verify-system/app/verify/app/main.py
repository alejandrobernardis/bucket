#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 02/Dec/2013 16:16

import os
import sys
import settings

_parent_path = os.path.split(settings.ROOT_PATH)[0]

for folder in ('../../bin', '../../lib',):
    folder_path = os.path.abspath(os.path.join(_parent_path, folder))
    if os.path.isdir(folder_path):
        sys.path.insert(0, folder_path)

__project_name__ = 'KAV'
__project_full_name__ = 'Kinetiq, Addicted Verify'
__project_owner__ = 'Kinetiq, inc'
__project_author__ = 'Alejandro M. Bernardis'
__project_version__ = (1, 0, 0, 'alpha', 0)
__project_created__ = 'Dec, 2013'

import copy
from addicted.verify.core.exceptions import ConfigurationError
from addicted.verify.core.utils import import_module
from mongoengine import register_connection
from mongoengine.connection import get_db
from pymongo.common import validate
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from pymongo.mongo_replica_set_client import MongoReplicaSetClient
from sqlalchemy import create_engine as sql_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from tornado.autoreload import watch as autoreload_watch, \
    start as autoreload_start
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options, parse_command_line
from tornadomail.backends.smtp import EmailBackend

define('debug', default=settings.DEBUG, type=bool)
define('track', default=settings.TRACK, type=bool)
define('port', default=settings.PORT, type=int)
define('ssl', default=settings.SSL, type=bool)
define('cdn_prefix', default=settings.CDN_PREFIX, type=basestring)
define('prefork_process', default=settings.PREFORK_PROCESS, type=int)
define('xsrf_cookie', default=settings.XSRF_COOKIE, type=bool)
define('cookie_secret', default=settings.COOKIE_SECRET, type=basestring)
define('cookie_session', default=settings.COOKIE_SESSION, type=basestring)
define('login_url', default=settings.LOGIN_URL, type=basestring)
define('autoreload', default=settings.AUTORELOAD_ENABLED, type=bool)


class MainApplication(Application):
    def __init__(self):
        for item in settings.AUTORELOAD_FILES:
            file_path = os.path.join(settings.ROOT_PATH, item)
            if not os.path.isfile(file_path):
                raise ConfigurationError('File not found: %s' % file_path)
            autoreload_watch(file_path)

        _handlers = []

        for item in settings.STATIC_FILES:
            file_path = os.path.join(settings.STATIC_PATH, item)
            if not os.path.isfile(file_path):
                raise ConfigurationError('File not found: %s' % file_path)
            _handlers.append(
                (item, StaticFileHandler, {'path': settings.STATIC_PATH}))

        for item in settings.HANDLERS_LIST:
            attribute = 'handlers_list'
            try:
                module = import_module(item)
            except ImportError as e:
                raise ConfigurationError(
                    'ImportError %s: %s' % (item, e.args[0]))
            if not hasattr(module, attribute):
                raise ConfigurationError(
                    'Module "%s" does not define a "%s" attribute' %
                    (item, attribute))
            _handlers.extend(getattr(module, 'handlers_list'))

        for key, value in settings.DATABASE.items():
            database = copy.deepcopy(value)
            register_connection(
                alias=key,
                name=database.get('name'),
                username=database.get('username'),
                password=database.get('password'),
                **database.get('settings', {})
            )

        self._pymongo_connection_cache = {}
        self._sql_connection_cache = None

        super(MainApplication, self).__init__(_handlers, **{
            'debug': options.debug,
            'track': options.track,
            'ssl': options.ssl,
            'cdn_prefix': options.cdn_prefix,
            'xsrf_cookies': options.xsrf_cookie,
            'cookie_secret': options.cookie_secret,
            'cookie_session': options.cookie_session,
            'login_url': options.login_url,
            'path': settings.ROOT_PATH,
            'static_path': settings.STATIC_PATH,
            'template_path': settings.TEMPLATES_PATH,
            'temp_path': settings.TEMP_PATH,
            'ca_path': settings.CA_PATH,
            'site_title': settings.SITE_TITLE,
            'site_description': settings.SITE_DESCRIPTION,
            'site_domain': settings.SITE_DOMAIN,
            'site_root': settings.SITE_ROOT,
            'site_google_analytics': settings.SITE_GOOGLE_ANALYTICS,
            'session': settings.SESSION,
            'database': settings.DATABASE,
            'ui_modules': settings.UI_MODULES,
            'email': settings.EMAIL.get('email'),
        })

    def raw_pymongo(self, connection):
        return get_db(connection)

    def database(self, name, configuration=None):
        if name in self._pymongo_connection_cache:
            return self._pymongo_connection_cache[name]
        if not configuration:
            database_list = self.settings.get('database')
            if name not in database_list:
                raise ConfigurationError('Database not supported: %s' % name)
            configuration = copy.deepcopy(database_list[name])
            name = configuration.get('name', 'test')
        else:
            configuration = copy.deepcopy(configuration)
        username = configuration.get('username')
        password = configuration.get('password')
        config = copy.deepcopy(configuration.get('config'))
        if config:
            raise ConfigurationError('Database config not supported: %s' % name)
        host = config.get('host', 'localhost')
        port = config.get('port', 27017)
        host_or_uri = config.get('host_or_uri')
        for key, value in config.items():
            try:
                validate(key, value)
            except Exception:
                del config[key]
        if host_or_uri and config.get('replicaset'):
            client = MongoReplicaSetClient(host_or_uri, **config)
        else:
            client = MongoClient(host, port, **config)
        database = Database(client, name)
        if username and password:
            database.authenticate(username, password, database)
        self._pymongo_connection_cache[name] = database
        return database

    @property
    def database_config(self):
        value = self.settings.get('database', False)
        if not value:
            raise ConfigurationError('Database config is undefined')
        return value

    def sql_database(self):
        if not self._sql_connection_cache:
            self._sql_connection_cache = sql_engine(
                settings.DATABASE_SQL_STRING % settings.DATABASE_SQL['default'],
                convert_unicode=True, pool_size=20,
                pool_recycle=3600,  max_overflow=0
            )
        return scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._sql_connection_cache
            )
        )

    @property
    def session_config(self):
        value = self.settings.get('session', False)
        if not value:
            raise ConfigurationError('Session config is undefined')
        return value

    @property
    def email_client(self):
        return EmailBackend(**settings.EMAIL)

    @property
    def cdn_support(self):
        return self.settings.get('cdn_prefix', False)

    @property
    def ssl_support(self):
        return self.settings.get('ssl', False)

    @property
    def ssl_config(self):
        if not self.ssl_support:
            return None
        import ssl
        ca_path = self.settings.get('ca_path')
        if not ca_path:
            raise ConfigurationError(
                'SSL Certificate path is not defined')
        elif not os.path.isdir(ca_path):
            raise ConfigurationError(
                'SSL Certificate path does not exist: %s' % ca_path)
        return {
            'cert_reqs': ssl.CERT_REQUIRED,
            'ca_certs': os.path.join(ca_path, 'cacert.crt'),
            'certfile': os.path.join(ca_path, 'server.crt'),
            'keyfile': os.path.join(ca_path, 'server.key')
        }


if __name__ == '__main__':
    parse_command_line()
    app = MainApplication()
    http_server = HTTPServer(app, xheaders=True, ssl_options=app.ssl_config)
    if options.prefork_process > 1:
        http_server.bind(options.port)
        http_server.start(options.prefork_process)
    else:
        http_server.listen(options.port)
    io_loop = IOLoop.instance()
    if options.autoreload:
        autoreload_start(io_loop)
    try:
        io_loop.start()
    except KeyboardInterrupt:
        io_loop.stop()
        sys.exit(0)
