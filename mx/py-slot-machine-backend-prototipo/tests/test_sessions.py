#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 19/08/2013 19:39

import os
import sys
import time

ROOT_PATH = '/Users/bernardisa/Development/projects/mate/' \
            'figment-latino-casino-server/src/backend/'

ROOT_PATH = '/deploy/src/backend/'

for item in ['app', 'bin', 'lib']:
    sys.path.insert(0, os.path.join(ROOT_PATH, item))

import unittest
import uuid
from casino8.security.sessions import *
from tornado.testing import LogTrapTestCase, AsyncHTTPTestCase
from tornado.web import Application, RequestHandler

GENERIC_RESPONSE = 'success'

cfg_memcached = dict(
    engine=MEMCACHED_ENGINE,
    servers=('127.0.0.1:11211',),
    serializer=MARSHAL_SERIALIZER,
)

serializers = (
    PICKLE_SERIALIZER,
    MARSHAL_SERIALIZER,
    JSON_SERIALIZER
)


def generate_key():
    return 'test-' + str(uuid.uuid4())


# Clients

class TestClient(unittest.TestCase):
    obj = dict(a=1, b=2, c=3, d=4, e=5, f=6)

    def test_01_factory(self):
        for item in (cfg_memcached,):
            cfg = item.copy()
            for serializer in serializers:
                cfg['serializer'] = serializer
                c = ClientFactory.create(cfg)
                k = generate_key()
                c.save(k, self.obj)
                self.assertEqual(c.get(k), self.obj)
                c.delete(k)
                self.assertNotEqual(c.get(k), self.obj)
                self.assertEqual(c.get(k), dict())
                self.assertEqual(c.get('undefined'), dict())

    def test_03_memcached_client(self):
        c = MemcachedClient(cfg_memcached)
        k = generate_key()
        c.save(k, self.obj)
        self.assertEqual(c.get(k), self.obj)
        c.delete(k)
        self.assertNotEqual(c.get(k), self.obj)
        self.assertEqual(c.get(k), dict())
        self.assertEqual(c.get('undefined'), dict())


# Tornado Application

class BaseHandler(RequestHandler, SessionMixin):
    def initialize(self):
        self._current_user = dict(
            uid=1 << 8, username='sysadmin', rid=2 << 8, role_name='admin',
            email='sysadmin@localhost', enabled=True, available=True,
        )

    def get_secure_cookie(self, name, value=None, max_age_days=31):
        if not hasattr(self, '_cookie_sid'):
            self._cookie_sid = generate_key()
        return self._cookie_sid

    def get(self):
        self.finish(GENERIC_RESPONSE)


class MemcachedBaseHandler(BaseHandler):
    def initialize(self):
        self.settings['session'] = cfg_memcached.copy()


class SessionCreateBaseHandler(BaseHandler):
    def get(self):
        self.session.clear()
        assert self.session.is_empty
        assert not self.session.data
        self.session.set('first_name', 'my-first-name')
        user = DeviceSession(uid='myuid').todict()
        self.session.update(**user)
        assert self.session.get('uid') == 'myuid'
        assert not self.session.is_empty
        assert self.session.data
        assert self.session.get('first_name') == 'my-first-name'
        super(SessionCreateBaseHandler, self).get()


class SessionManipulateBaseHandler(BaseHandler):
    def get(self):
        self.session.clear()
        assert self.session.is_empty
        assert not self.session.data
        self.session.set('first_name', 'my-first-name')
        assert self.session.get('first_name') == 'my-first-name'
        self.session.set('last_name', 'my-last-name')
        assert self.session.get('last_name') == 'my-last-name'
        self.session.delete('last_name')
        try:
            assert not self.session.get('last_name')
        except BaseException:
            pass
        self.session.update(a=1, b=2, c=3)
        assert self.session.get('a') == 1
        assert self.session.get('b') == 2
        assert self.session.get('c') == 3
        assert self.session.has_key('a')
        assert self.session.has_key('b')
        assert self.session.has_key('c')
        assert not self.session.has_key('d')
        assert not self.session.has_key('e')
        assert not self.session.has_key('f')
        self.session.clear()
        assert self.session.is_empty
        assert not self.session.data
        super(SessionManipulateBaseHandler, self).get()


class SessionExpireBaseHandler(BaseHandler):
    def get(self):
        self.session.clear()
        assert self.session.is_empty
        assert not self.session.data
        self.session.set('first_name', 'my-first-name')
        assert self.session.get('first_name') == 'my-first-name'
        self.session.expire(1)
        time.sleep(2)
        assert self.session.is_empty
        self.session.expire(5)
        self.session.set('new_key', 'value_new_key')
        assert not self.session.is_empty
        super(SessionExpireBaseHandler, self).get()


class SessionDeleteBaseHandler(BaseHandler):
    def get(self):
        self.session.clear()
        assert self.session.is_empty
        assert not self.session.data
        self.session.set('first_name', 'my-first-name')
        self.session.delete('first_name')
        assert self.session.data == dict()
        self.session.revoke()
        try:
            assert self.session.data
        except BaseException:
            pass
        super(SessionDeleteBaseHandler, self).get()

class MemcachedSessionCreateHandler(
        MemcachedBaseHandler, SessionCreateBaseHandler):
    pass


class MemcachedSessionManipulateHandler(
        MemcachedBaseHandler, SessionManipulateBaseHandler):
    pass


class MemcachedSessionExpireHandler(
        MemcachedBaseHandler, SessionExpireBaseHandler):
    pass


class MemcachedSessionDeleteHandler(
        MemcachedBaseHandler, SessionDeleteBaseHandler):
    pass


class TornadoApplicationTest(AsyncHTTPTestCase, LogTrapTestCase):
    def get_app(self):
        handlers = [
            ('/session-memcached', MemcachedSessionCreateHandler),
            ('/session-memcached-manipulate',
                MemcachedSessionManipulateHandler),
            ('/session-memcached-expire', MemcachedSessionExpireHandler),
            ('/session-memcached-delete', MemcachedSessionDeleteHandler),
        ]
        settings = dict()
        settings['cookie_secret'] = "SeCuR3+C00k1e!-#.#"
        return Application(handlers, **settings)

    def get_url_response(self, url='/', follow_redirects=False):
        self.http_client.fetch(
            self.get_url(url), self.stop, follow_redirects=follow_redirects)
        return self.wait()

    def test_05_memcached_create_session(self):
        response = self.get_url_response('/session-memcached?uid=ABC123-321CBA')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.buffer.read(), GENERIC_RESPONSE.encode())

    def test_06_memcached_manipulate_session(self):
        response = self.get_url_response('/session-memcached-manipulate?uid=ABC123-321CBA')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.buffer.read(), GENERIC_RESPONSE.encode())

    def test_07_memcached_expire_session(self):
        response = self.get_url_response('/session-memcached-expire?uid=ABC123-321CBA')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.buffer.read(), GENERIC_RESPONSE.encode())

    def test_08_memcached_delete_session(self):
        response = self.get_url_response('/session-memcached-delete?uid=ABC123-321CBA')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.buffer.read(), GENERIC_RESPONSE.encode())
