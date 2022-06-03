#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
pkg = '/src'
root_path = os.path.dirname(__file__)
sys.path.insert(0, root_path.replace(pkg, '/src'))
sys.path.insert(0, root_path.replace(pkg, '/lib'))
sys.path.insert(0, root_path.replace(pkg, '/libs'))
sys.path.insert(0, '/development/library/python')

# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Jan 4, 2013 12:16:43 PM
__project_name__ = u"MXDMVOJ"
__project_full_name__ = u"MX, di Paola Marquéz, Veracruz, Orgullo Jarocho"
__project_owner__ = u'Asumi Kamikaze'
__project_author__ = u'Alejandro M. Bernardis'
__project_version__ = (1,0,0,'alpha',0)
__project_created__ = u"Jan 4, 2013 12:16:43 PM"

#: imports
import settings
from com.ak.common.roles import Role
from com.ak.common.security import secret_key
from pymongo import Connection as mongodb_connection
from mongoengine import connect as mongodb_connect
from mongoengine import register_connection
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options, parse_command_line

#: server
define('debug', default=settings.DEBUG)
define('port', default=settings.PORT)
define('ssl', default=settings.SSL)
define('cdn', default=settings.CDN)
define('prefork', default=settings.PREFORK)
define('xsrf_cookie', default=settings.XSRF_COOKIES)

#: database
define('database_name', default=settings.DATABASE_NAME)
define('database_user', default=settings.DATABASE_USER)
define('database_pass', default=settings.DATABASE_PASS)
define('database_host', default=settings.DATABASE_HOST)
define('database_port', default=settings.DATABASE_PORT)
define('database_conn', default=settings.DATABASE_CONN)
define('database_areq', default=settings.DATABASE_AREQ)
define('database_ugls', default=settings.DATABASE_UGLS)

#: database async
define('database_pool', default='%s_pool' % settings.DATABASE_NAME)
define('database_cach', default=settings.DATABASE_CACH)

#: application
class MainApplication(Application):
    def __init__(self):
        _handlers = []
        pkg_root_path = os.path.join(root_path, settings.PKG_DIR)
        _static_path = os.path.join(pkg_root_path, 'static')
        _static_path_ditc = dict(path=os.path.join(_static_path, 'root'))

        for a in settings.STATIC_FILES:
            _handlers.append((a, StaticFileHandler, _static_path_ditc))

        for a in settings.HANDLERS_LIST:
            _name = '%s.%s' % (settings.PKG_HANDLERS, a)
            _module = __import__(_name, globals(), locals(), [a], -1)
            _handlers.extend(_module.handlers_list)

        for a in settings.USER_ROLES:
            Role(**settings.USER_ROLES[a])

        try:
            _cdn_file = os.path.join(root_path, 'cdn_prefix.conf')
            _cdn_prefix = [a.strip() for a in file(_cdn_file)
                           if a.strip() and not a.strip().startswith('#')][0]
        except (IOError, IndexError):
            _cdn_prefix = None

        _settings = dict(
            debug=options.debug,
            ssl= options.ssl,
            cdn=options.cdn,
            cdn_prefix=_cdn_prefix,
            xsrf_cookies=options.xsrf_cookie,
            cookie_secret=secret_key(64),
            cookie_user_session=settings.COOKIE_USER_SESSION,
            login_url=settings.LOGIN_URL,
            path=pkg_root_path,
            static_path=_static_path,
            template_path=os.path.join(pkg_root_path, 'templates'),
            temp_path=os.path.join(pkg_root_path, 'tmp'),
            upload_path=os.path.join(pkg_root_path, 'upload'),
            download_path=os.path.join(pkg_root_path, 'download'),
            backup_path=os.path.join(pkg_root_path, 'backup'),
            roles=Role.get_roles(),)
        _settings['site_name'] = settings.SITE_TITLE
        _settings['site_description'] = settings.SITE_DESCRIPTION

        self._database_name = options.database_name
        self._database_settings = dict(
            host=options.database_host,
            port=options.database_port,
            username=options.database_user,
            password=options.database_pass,
            max_pool_size=options.database_conn,
            auto_start_request=options.database_areq,
            use_greenlets=options.database_ugls,)

        if settings.DATABASE_ORM:
            mongodb_connect(self._database_name, **self._database_settings)
            for a in settings.DATABASE_MULTIPLE:
                _cfg = settings.DATABASE_MULTIPLE[a]
                register_connection(**_cfg)

        Application.__init__(self, _handlers, **_settings)

        if options.debug:
            print '\nROLES:'
            print Role.get_roles()
            print '\nHANDLERS:'
            print _handlers
            print '\nSETTINGS:'
            print _settings

    @property
    def db_conn(self):
        try:
            if not hasattr(self, '_database_connection'):
                self._database_connection = None if settings.DATABASE_ORM \
                    else mongodb_connection(**self._database_settings)
            return self._database_connection
        except:
            return None

    @property
    def db(self):
        try:
            if not hasattr(self, '_database'):
                self._database =  self.db_conn[self._database_name]
            return self._database
        except:
            return None

    def db_by_name(self, name=None):
        try:
            if name and settings.DATABASE_MULTIPLE.has_key(name):
                name = settings.DATABASE_MULTIPLE[name]['name']
            else:
                name = name or 'test'
            return self.db_conn[name]
        except:
            return None

    @property
    def ssl_support(self):
        return self.settings.get('ssl')

    def ssl_config(self):
        if not self.ssl_support:
            return None
        CA_dir = os.path.join(self.settings.get('path'), 'CA')
        return dict(
            certfile=os.path.join(CA_dir, 'server.crt'),
            keyfile=os.path.join(CA_dir, 'server.key'),)

    @property
    def cdn_support(self):
        return self.settings.get('cdn')

    @property
    def cdn_prefix(self):
        return self.settings.get('cdn_prefix') or ''

#: main
if __name__ == '__main__':
    try:
        parse_command_line()
        app = MainApplication()
        cfg = dict(xheaders=True, ssl_options=app.ssl_config())
        http_server = HTTPServer(app, **cfg)
        if options.prefork:
            http_server.bind(options.port)
            http_server.start()
        else:
            http_server.listen(options.port)
        IOLoop.instance().start()

    except KeyboardInterrupt:
        exit(u'\n\x1b[0;31m[kill]\x1b[0m => %s' % __project_full_name__)
