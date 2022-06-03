#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 19/08/2013 11:07


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

import inspect
import datetime
from functools import wraps
from uuid import uuid4
from casino8.common.utils import datetime_parser, str_complex_type, hash_uid
# from casino8.machines.configurations import AI_SESSION_MAXIMUM_TIME
from casino8.security.iron_man import IronMan
from bson.objectid import ObjectId
from celery_tasks import push_session_activity
from tornado.web import RequestHandler
from settings import LANGUAGES_DEFAULT


# engines

REDIS_ENGINE = 'redis'
MEMCACHED_ENGINE = 'memcached'


# serializators

PICKLE_SERIALIZER = 'pickle'
MARSHAL_SERIALIZER = 'marshal'
JSON_SERIALIZER = 'json'


# configurations

SESSION_NAME = 'sid'
SESSION_PREFIX = 'session'
SESSION_EXPIRE = 60 * 60 * 100


# redis

REDIS_CLIENT_DB = 0
REDIS_CLIENT_ARGS = (
    'host', 'port', 'db', 'password', 'socket_timeout', 'connection_pool',
    'charset', 'errors', 'decode_responses', 'unix_socket_path',
    'max_connections',
)


# memcached

MEMCACHED_CLIENT_ARGS = (
    'servers', 'behaviors', 'binary', 'username', 'password',
)


# clients

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


# session

class Session(object):
    def __init__(self, handler):
        if not handler or not isinstance(handler, RequestHandler):
            raise TypeError('Handler is not a RequestHandler')
        self._handler = handler
        self._settings = None
        self._client = None

    @property
    def settings(self):
        if not self._settings:
            if 'session' not in self._handler.settings:
                raise KeyError('Session configurations is not define.')
            settings = self._handler.settings.copy()
            self._settings = settings['session']
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
        fbuid = self._handler.get_argument('fbuid', None)
        sid = fbuid or self._handler.get_argument('uid', None)
        if not sid:
            raise ValueError('Session ID argument is not found.')
        return str(sid)

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


class SessionMixin(object):
    @property
    def session(self):
        if not hasattr(self, '_session'):
            setattr(self, '_session', Session(self))
        return getattr(self, '_session')

    def session_validate(self):
        uid = self.get_argument('uid', False)
        sid = self.get_argument('sid', False)
        fbuid = self.get_argument('fbuid', False)
        if not fbuid and not uid:
            raise KeyError('Argument UID "%s" is not found.' % uid)
        elif not sid:
            raise KeyError('Argument SID "%s" is not found.' % sid)
        elif self.session.is_empty:
            raise KeyError('Session ID "%s" has expired.' % sid)
        elif fbuid and self.session.get('fbuid') != fbuid:
            raise KeyError('Profile ID "%s" not macth.' % uid)
        elif not fbuid and self.session.get('uid') != uid:
            raise KeyError('Device ID "%s" not macth.' % uid)
        elif self.session.get('sid') != sid:
            raise KeyError('Session ID "%s" not macth.' % sid)
        return True

    def session_verify(self):
        try:
            return self.session_validate()
        except Exception:
            return False

    def _get_profile(self, fbuid, uid):
        return self.db.profiles.find_one({
            '_id': fbuid, 'devices': hash_uid(uid, fbuid)
        })

    def _get_device(self, uid):
        return self.db.devices.find_one({'_id': uid})

    def session_destroy(self):
        if self.session.is_empty:
            return

        uid = self.get_argument('uid', None)
        fbuid = self.get_argument('fbuid', None)
        device = self.get_argument('device', None)
        i = self.get_argument('i', None)
        self.validate_arguments(uid, device, i)

        if not IronMan.defense(i):
            raise ValueError('Iron Man (x)')

        update_datetime = datetime.datetime.utcnow()

        query = {'$set': {
            'sid': None,
            'modified': update_datetime
        }}

        if fbuid:
            try:
                self.db.profiles.update({'_id': fbuid}, query)
            except:
                raise ValueError('Profile Update (x)')
        else:
            try:
                self.db.devices.update({'_id': uid}, query)
            except:
                raise ValueError('Device Update (x)')

        session = self.session.data
        session['sid'] = None
        session['modified'] = update_datetime

        try:
            self.session.revoke()
        except:
            raise ValueError('Can\'t revoke the session data (x)')
        try:
            if self.settings.get('track', True):
                push_session_activity.delay(
                    activity='close', ip=self.remote_ip, **session
                )
        except Exception:
            pass

    def session_start(self):
        uid = self.get_argument('uid', None)
        fbuid = self.get_argument('fbuid', None)
        device = self.get_argument('device', None)
        lang = self.get_argument('lang', LANGUAGES_DEFAULT)
        i = self.get_argument('i', None)
        self.validate_arguments(uid, device, i)

        if not IronMan.defense(i):
            raise ValueError('Iron Man (x)')
        elif not self.session.is_empty:
            if self.session_verify():
                return self.session.data
            else:
                self.session.revoke()
        if fbuid:
            profile = self._get_profile(fbuid, uid)
            if not profile:
                raise ValueError('Facebook User ID (x)')
            profile['_id'] = uid
            profile['fbuid'] = fbuid
            profile['device'] = device
            profile['uid_fbuid'] = hash_uid(uid, fbuid)
            del profile['devices']
        else:
            profile = self._get_device(uid)
            if not profile:
                raise ValueError('Device ID (x)')

        sid = self.session.create_sid()
        update_datetime = datetime.datetime.utcnow()
        profile['sid'] = sid
        profile['remote_ip'] = self.remote_ip
        profile['last_login'] = update_datetime
        profile['modified'] = update_datetime

        query = {'$set': {
            'sid': sid,
            'modified': update_datetime,
            'last_login': update_datetime,
        }}

        if not profile.get('lang', False):
            profile['lang'] = query['$set']['lang'] = lang

        # if 'ai_session_enabled' not in profile:
        #     profile['ai_session_enabled'] = \
        #         query['$set']['ai_session_enabled'] = False
        #     profile['ai_session_balance'] = \
        #         query['$set']['ai_session_balance'] = profile.get('balance', 0)
        #     profile['ai_session_begin'] = \
        #         query['$set']['ai_session_begin'] = update_datetime
        #     profile['ai_session_finish'] = \
        #         query['$set']['ai_session_finish'] = update_datetime + \
        #         datetime.timedelta(hours=AI_SESSION_MAXIMUM_TIME)
        #     profile['ai_session_spins'] = \
        #         query['$set']['ai_session_spins'] = 0

        self.request.arguments['sid'] = [sid]
        device_session = DeviceSession(**profile).todict()
        self.session.update(**device_session)

        if fbuid:
            try:
                self.db.profiles.update({'_id': fbuid}, query)
            except:
                raise ValueError('Profile Update (x)')
        else:
            try:
                self.db.devices.update({'_id': uid}, query)
            except:
                raise ValueError('Device Update (x)')
        try:
            if self.settings.get('track', True):
                push_session_activity.delay(
                    activity='start', ip=self.remote_ip, **device_session
                )
        except Exception:
            pass
        return profile


class DeviceSession(object):
    # ai_session_enabled = None
    # ai_session_balance = None
    # ai_session_begin = None
    # ai_session_finish = None
    # ai_session_spins = None

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
    lang = None
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
    mini_game_id = 0
    mini_game_bet = 0
    mini_game_factor = 0
    mini_game_matrix = None

    # Helpers

    _DATETIME_VALUES = (
        #'ai_session_begin',
        #'ai_session_finish',
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
        result = dict()
        for key in dir(self):
            value = getattr(self, key)
            if not key.startswith('_') and not inspect.ismethod(value):
                if key in self._DATETIME_VALUES:
                    value = str_complex_type(value)
                result[key] = value
        return result


def session_verify(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.session_verify():
            return self.get_json_response_and_finish(
                e_id=-1, e_message='SESSION EXPIRED'
            )
        return method(self, *args, **kwargs)
    return wrapper
