#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 21/06/2013 09:01

import os
import sys
import settings

# bootstrap

base_path = settings.ROOT_PATH

for folder in ('../bin', '../lib', '../../../lib'):
    sys.path.insert(0, os.path.abspath(os.path.join(base_path, folder)))


# version

__project_name__ = u'FC8S'
__project_full_name__ = u'Figment, Casino 8 Slots'
__project_owner__ = u'Figment, Inc'
__project_author__ = u'Figment, Inc'
__project_version__ = (1, 0, 0, 'alpha', 0)
__project_created__ = u'2013/06/21 09:01:00'


# imports

import copy
from pymongo.mongo_client import MongoClient
from pymongo.mongo_replica_set_client import MongoReplicaSetClient
from pymongo.database import Database
from pymongo.common import validate
from tornado.autoreload import watch as autoreload_watch, \
    start as autoreload_start
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options, parse_command_line

from casino8.security.sessions import ClientFactory


# server

define('debug', default=settings.DEBUG)
define('track', default=settings.TRACK)
define('port', default=settings.PORT)
define('ssl', default=settings.SSL)
define('cdn', default=settings.CDN)
define('cdn_prefix', default=settings.CDN_PREFIX)
define('prefork_process', default=settings.PREFORK_PROCESS)
define('xsrf_cookie', default=settings.XSRF_COOKIE)
define('cookie_secret', default=settings.COOKIE_SECRET)
define('cookie_user_session', default=settings.COOKIE_USER_SESSION)
define('autoreload', default=settings.AUTORELOAD_ENABLED)


# database

define('database_rset', default=settings.DATABASE_RSET)
define('database_name', default=settings.DATABASE_NAME)
define('database_host', default=settings.DATABASE_HOST)
define('database_huri', default=settings.DATABASE_HURI)
define('database_port', default=settings.DATABASE_PORT)
define('database_conn', default=settings.DATABASE_CONN)
define('database_areq', default=settings.DATABASE_AREQ)
define('database_ugls', default=settings.DATABASE_UGLS)
define('database_user', default=settings.DATABASE_USER)
define('database_pass', default=settings.DATABASE_PASS)


# async database

define('database_pool', default='%s_pool' % settings.DATABASE_NAME)


# application

class MainApplication(Application):
    def __init__(self):
        self._database_client = None
        self._database_config = None
        self._simple_database_config = None
        self._memory_client = None

        _handlers = []

        for item in settings.STATIC_FILES:
            _handlers.append((item, StaticFileHandler,
                              dict(path=settings.STATIC_PATH)))

        for item in settings.HANDLERS_LIST:
            _name = '%s.%s' % (settings.HANDLERS_PKG, item)
            _module = __import__(_name, globals(), locals(), [item], 0)
            _handlers.extend(_module.handlers_list)

        for item in settings.AUTORELOAD_FILES:
            autoreload_watch(os.path.join(settings.ROOT_PATH, item))

        _database = dict(
            database=options.database_name,
            databases=dict(
                track=settings.DATABASE_TRACK_NAME,
                social=settings.DATABASE_SOCIAL_NAME,
                notify=settings.DATABASE_NOTIFY_NAME,
                graph=settings.DATABASE_GRAPH_NAME,
            ),
            replicaset=options.database_rset,
            hosts_or_uri=options.database_huri,
            host=options.database_host,
            port=options.database_port,
            max_pool_size=options.database_conn,
            auto_start_request=options.database_areq,
            use_greenlets=options.database_ugls,
            username=options.database_user,
            password=options.database_pass,
        )

        _settings = dict(
            debug=options.debug,
            track=options.track,
            ssl=options.ssl,
            cdn=options.cdn,
            cdn_prefix=options.cdn_prefix,
            xsrf_cookies=options.xsrf_cookie,
            cookie_secret=options.cookie_secret,
            cookie_user_session=options.cookie_user_session,
            login_url=settings.LOGIN_URL,
            session=settings.SESSION,
            path=settings.ROOT_PATH,
            static_path=settings.STATIC_PATH,
            template_path=settings.TEMPLATES_PATH,
            temp_path=settings.TEMP_PATH,
            ca_path=settings.CA_PATH,
            site_title=settings.SITE_TITLE,
            site_description=settings.SITE_DESCRIPTION,
            site_domain=settings.SITE_DOMAIN,
            site_root=settings.SITE_ROOT,
            platforms=settings.PLATFORMS,
            in_approval=settings.IN_APPROVAL,
            database=_database,
        )

        super(MainApplication, self).__init__(_handlers, **_settings)

    @property
    def memory_client(self):
        if not self._memory_client:
            self._memory_client = ClientFactory.create(
                self.settings.get('session', settings.SESSION)
            )
        return self._memory_client

    @property
    def ssl_support(self):
        return self.settings.get('ssl', False)

    def ssl_config(self):
        import ssl
        ca_path = self.settings.get('ca_path', settings.CA_PATH)
        if self.ssl_support and os.path.isdir(ca_path):
            return dict(
                cert_reqs=ssl.CERT_REQUIRED,
                certfile=os.path.join(ca_path, 'server.crt'),
                keyfile=os.path.join(ca_path, 'server.key'),
                ca_certs=os.path.join(ca_path, 'cacert.crt')
            )
        return None

    # def db(self, database=None, not_replica_set=False):
    #     _ref = None
    #     _settings = self.settings.get('database')
    #     if _settings:
    #         if database:
    #             _databases = _settings.get('databases')
    #             if database not in _databases:
    #                 raise KeyError('Database "%s" is not supported.' % database)
    #             database = _databases.get(database)
    #         else:
    #             database = _settings.get('database')
    #         if 'hosts_or_uri' not in _settings:
    #             raise KeyError('Hosts or Uri is not defined.')
    #         elif not getattr(self, '_database_config'):
    #             _config = copy.deepcopy(_settings)
    #             for key, value in _config.items():
    #                 try:
    #                     validate(key, value)
    #                 except Exception:
    #                     del _config[key]
    #             self._database_config = _config
    #             self._simple_database_config = copy.deepcopy(_config)
    #             del self._simple_database_config['replicaset']
    #         if not not_replica_set:
    #             client = MongoReplicaSetClient(
    #                 _settings['hosts_or_uri'], **self._database_config)
    #         else:
    #             client = MongoClient(
    #                 _settings['host'], _settings['port'],
    #                 **self._simple_database_config)
    #         if database:
    #             _ref = Database(client, database)
    #         elif not getattr(self, '_database_client'):
    #             _ref = Database(client, database)
    #             self._database_client = _ref
    #         try:
    #             username = _settings.get('username')
    #             password = _settings.get('password')
    #             if username and password:
    #                 _ref.authenticate(username, password, database)
    #         except Exception:
    #             raise ValueError('Authentication failure.')
    #         return _ref or self._database_client
    #     raise KeyError('Database is not found.')

    def db(self, database=None, not_replica_set=False):
        if not database:
            database = settings.DATABASE_NAME
        try:
            cnx = Database(MongoClient(
                host=settings.DATABASE_HOST,
                port=settings.DATABASE_PORT,
                max_pool_size=settings.DATABASE_CONN,
                auto_start_request=settings.DATABASE_AREQ,
                use_greenlets=settings.DATABASE_UGLS,
            ), database)
            username = settings.DATABASE_USER
            password = settings.DATABASE_PASS
            try:
                if username and password:
                    cnx.authenticate(username, password, database)
            except Exception:
                raise ValueError('Authentication failure.')
            return cnx
        except Exception:
            raise KeyError('Database is not found.')

    def db_track(self, database=None):
        if not database:
            database = settings.DATABASE_TRACK_NAME
        try:
            cnx = Database(MongoClient(
                host=settings.TRACK_DATABASE_HOST,
                port=settings.TRACK_DATABASE_PORT,
                max_pool_size=settings.TRACK_DATABASE_CONN,
                auto_start_request=settings.TRACK_DATABASE_AREQ,
                use_greenlets=settings.TRACK_DATABASE_UGLS,
            ), database)
            username = settings.TRACK_DATABASE_USER
            password = settings.TRACK_DATABASE_PASS
            try:
                if username and password:
                    cnx.authenticate(username, password, database)
            except Exception:
                raise ValueError('Authentication failure.')
            return cnx
        except Exception:
            raise KeyError('Database is not found.')

    def db_social(self, database=None):
        try:
            database = {
                'social': settings.DATABASE_SOCIAL_NAME,
                'notify': settings.DATABASE_NOTIFY_NAME,
            }.get(database or 'social')
            cnx = Database(MongoClient(
                host=settings.SOCIAL_DATABASE_HOST,
                port=settings.SOCIAL_DATABASE_PORT,
                max_pool_size=settings.SOCIAL_DATABASE_CONN,
                auto_start_request=settings.SOCIAL_DATABASE_AREQ,
                use_greenlets=settings.SOCIAL_DATABASE_UGLS,
            ), database)
            username = settings.SOCIAL_DATABASE_USER
            password = settings.SOCIAL_DATABASE_PASS
            try:
                if username and password:
                    cnx.authenticate(username, password, database)
            except Exception:
                raise ValueError('Authentication failure.')
            return cnx
        except Exception:
            raise KeyError('Database is not found.')

# Main

if __name__ == '__main__':
    try:
        parse_command_line()
        app = MainApplication()
        config = dict(xheaders=True, ssl_options=app.ssl_config())
        http_server = HTTPServer(app, **config)
        if options.prefork_process > 1:
            http_server.bind(options.port)
            http_server.start(options.prefork_process)
        else:
            http_server.listen(options.port)
        io_loop = IOLoop.instance()
        if options.autoreload:
            autoreload_start(io_loop)
        io_loop.start()
    except KeyboardInterrupt:
        sys.exit(0)
