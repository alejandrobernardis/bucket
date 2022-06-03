#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 23/Jan/2014 14:04

try:
    import pickle
except ImportError:
    pickle = None

try:
    import marshal
except ImportError:
    marshal = None

try:
    import json
except ImportError:
    json = None

import datetime
import dateutil.parser
import inspect
import json
import hashlib
from bson.objectid import ObjectId
from optparse import OptionParser
from uuid import uuid4

SESSION_NAME = 'sid'
SESSION_PREFIX = 'session'
SESSION_EXPIRE = 60 * 20
SESSION_CONFIG = {
    'engine': 'memcached',
    'servers': ('c8-prd-session.bux2pt.0001.usw2.cache.amazonaws.com:11211',),
    'serializer': 'marshal',
}

PICKLE_SERIALIZER = 'pickle'
MARSHAL_SERIALIZER = 'marshal'
JSON_SERIALIZER = 'json'
REDIS_ENGINE = 'redis'
MEMCACHED_ENGINE = 'memcached'
MEMCACHED_CLIENT_ARGS = (
    'servers', 'behaviors', 'binary', 'username', 'password',
)


def swallow_args(func):
    def decorator(arg, *unused_args):
        if not arg:
            return None
        return func(arg, *unused_args)
    return decorator


@swallow_args
def unicode_to_str(arg):
    return arg.encode('utf-8')


def datetime_parser(value, default=None):
    kwargs = {}
    if isinstance(value, datetime.date) \
            or isinstance(value, datetime.time) \
            or isinstance(value, datetime.datetime) \
            or isinstance(value, datetime.timedelta):
        return value
    elif isinstance(value, (tuple, list)):
        value = ' '.join([str(x) for x in value])
    elif isinstance(value, int):
        value = str(value)
    elif isinstance(value, dict):
        kwargs = value
        value = kwargs.pop('date')
    try:
        try:
            parsedate = dateutil.parser.parse(value, **kwargs)
        except ValueError:
            parsedate = dateutil.parser.parse(value, fuzzy=True, **kwargs)
        return parsedate
    except Exception:
        return default or datetime.datetime.utcnow()


def str_complex_type(value):
    if type(value) in (int, float, long, bool) or isinstance(value, ObjectId):
        return str(value)
    elif type(value) is unicode:
        return unicode_to_str(value)
    elif isinstance(value, datetime.date) \
        or isinstance(value, datetime.time) \
            or isinstance(value, datetime.datetime):
        return value.isoformat()
    return value


def hash_uid(uid, fbuid=None):
    if not fbuid:
        return uid
    else:
        h = hashlib.md5()
        h.update('%s-%s' % (uid, fbuid))
        return h.hexdigest()


class Client(object):
    def __init__(self, settings):
        self._settings = settings
        self._engine = None
        self._serializer = None

    @property
    def engine(self):
        if not self._engine:
            self._engine = self._do_create()
        return self._engine

    @property
    def serializer(self):
        if not self._serializer:
            self._serializer = self._settings.get('serializer', None)
        return self._serializer

    def get(self, sid):
        session = self._do_get(sid)
        return self.deserialize(session) if session else dict()

    def save(self, sid, value, expire=None):
        value = self.serialize(value)
        expire = self._settings.get('expire', expire or SESSION_EXPIRE)
        self._do_save(sid, value, expire)

    def delete(self, sid):
        self._do_delete(sid)

    def has(self, sid):
        return self._do_has(sid)

    def serialize(self, value):
        if json and self.serializer == JSON_SERIALIZER:
            return json.dumps(value)
        elif marshal and self.serializer == MARSHAL_SERIALIZER:
            return marshal.dumps(value)
        return pickle.dumps(value)

    def deserialize(self, value):
        if json and self.serializer == JSON_SERIALIZER:
            value = value.decode() if isinstance(value, bytes) else value
            return json.loads(value)
        elif marshal and self.serializer == MARSHAL_SERIALIZER:
            return marshal.loads(value)
        return pickle.loads(value)

    def _do_create(self):
        raise NotImplementedError()

    def _do_get(self, sid):
        raise NotImplementedError()

    def _do_save(self, sid, value, expire):
        raise NotImplementedError()

    def _do_delete(self, sid):
        raise NotImplementedError()

    def _do_has(self, sid):
        raise NotImplementedError()

    def __repr__(self):
        return '<%s>' % self.__class__.__name__


class MemcachedClient(Client):
    def _do_create(self):
        from pylibmc import Client as Memcached
        settings = self._settings.copy()
        for key in self._settings:
            if key not in MEMCACHED_CLIENT_ARGS:
                del settings[key]
        return Memcached(**settings)

    def _do_get(self, sid):
        return self.engine.get(sid)

    def _do_save(self, sid, value, expire):
        self.engine.set(sid, value, expire)

    def _do_delete(self, sid):
        self.engine.delete(sid)

    def _do_has(self, sid):
        return self.get(sid) is not None


class ClientFactory(object):
    @staticmethod
    def create(settings):
        if 'engine' not in settings:
            raise KeyError('Engine not define.')
        engine = settings['engine']
        client = getattr(ClientFactory, '_create_%s' % engine, None)
        if not client:
            raise TypeError('Engine "%s" is not supported.' % engine)
        return client(settings)

    @staticmethod
    def _create_memcached(settings):
        return MemcachedClient(settings)


class Session(object):
    def __init__(self, sid):
        self._sid = sid
        self._client = None
        self._settings = None

    @property
    def settings(self):
        if not self._settings:
            self._settings = SESSION_CONFIG.copy()
        return self._settings

    @property
    def client(self):
        if not self._client:
            self._client = ClientFactory.create(self.settings)
        return self._client

    @property
    def data(self):
        return self.client.get(self.sid)

    @property
    def is_empty(self):
        return not self.data

    @property
    def keys(self):
        return self.data.keys()

    @property
    def iterkeys(self):
        return iter(self.data)

    @property
    def sid(self):
        if not self._sid:
            raise ValueError('Session ID argument is not found.')
        return str(self._sid)

    def get(self, key, default=None):
        session = self.data
        if key not in session:
            raise KeyError('%s not found in session' % key)
        return session.get(key, default)

    def set(self, key, value):
        session = self.data
        session[key] = value
        self._save_data(session)

    def update(self, **kwargs):
        session = self.data
        session.update(kwargs)
        self._save_data(session)

    def delete(self, *keys):
        session = self.data
        for key in keys:
            if key in session:
                del session[key]
        self._save_data(session)

    def clear(self):
        self._save_data(dict())

    def revoke(self):
        self.client.delete(self.sid)

    def expire(self, value):
        self._save_data(self.data, value)

    def has_key(self, key):
        return key in self.data

    def create_sid(self):
        return str(uuid4())

    def _save_data(self, value, expire=None):
        self.client.save(self.sid, value, expire)


class DeviceSession(object):
    ai_session_enabled = None
    ai_session_balance = None
    ai_session_begin = None
    ai_session_finish = None
    ai_session_spins = None
    balance = 0
    bet = 0
    device = None
    fbuid = None
    free_spins = 0
    game = 0
    gift_available = False
    gift_award = 0
    gift_time_begin = None
    gift_time_finish = None
    gift_total = 0
    last_login = None
    level = 0
    lines = 0
    mid = 0
    points = 0
    points_next_level = 0
    remote_ip = '0.0.0.0'
    sale = False
    sid = None
    spin_time = 0
    total_machines = 0
    uid = None
    uid_fbuid = None

    # Helpers

    _DATETIME_VALUES = (
        'ai_session_begin',
        'ai_session_finish',
        'gift_time_begin',
        'gift_time_finish',
        'created',
        'modified',
        'last_login',
    )

    def __init__(self, ignore=None, **kwargs):
        if not ignore:
            ignore = []
        for key, value in kwargs.items():
            if key == '_id':
                key = 'uid'
            if ignore and key in ignore:
                continue
            elif key in self._DATETIME_VALUES:
                value = datetime_parser(value)
            elif isinstance(value, ObjectId):
                value = str(value)
            setattr(self, key, value)

    def parse_datetime(self):
        for key in self._DATETIME_VALUES:
            setattr(self, key, datetime_parser(getattr(self, key)))

    def todict(self):
        result = {}
        for key in dir(self):
            value = getattr(self, key)
            if not key.startswith('_') and not inspect.ismethod(value):
                if key in self._DATETIME_VALUES:
                    value = str_complex_type(value)
                result[key] = value
        return result


def options_parser():
    parser = OptionParser()
    parser.add_option(
        '-i', '--id', dest='sid', default=None, type='string')
    parser.add_option(
        '-v', '--verbose', action='store_true', dest='verbose', default=False)
    return parser.parse_args()

if __name__ == '__main__':
    opts, args = options_parser()
    if not opts.sid:
        raise KeyError('SID not found')
    ss = Session(opts.sid)
    print json.dumps(ss.data, indent=4, sort_keys=True)
