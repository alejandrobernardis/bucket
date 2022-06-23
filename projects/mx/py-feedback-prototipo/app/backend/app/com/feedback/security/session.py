#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 04/Oct/2013 09:37

import copy
import uuid
from com.feedback.clients.key_value import KeyValueClientFactory
from com.feedback.core.exceptions import ConfigurationError
from com.feedback.models.users import User
from functools import wraps
from tornado.web import RequestHandler


SESSION_ID = 'asi'
SESSION_PREFIX = 'session'
SESSION_EXPIRES = 60 * 20


def verify_keys(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if args:
            key = args[0]
        elif kwargs and 'key' in kwargs:
            key = kwargs['key']
        else:
            raise ValueError('Key not defined')
        self.verify_key(key)
        return method(self, *args, **kwargs)
    return wrapper


def verify_session_status(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.validate_session():
            return self.goto_next_or_root()
        return method(self, *args, **kwargs)
    return wrapper


class Session(object):
    def __init__(self, handler):
        if not handler:
            raise ConfigurationError('Handler is undefined')
        elif not isinstance(handler, RequestHandler):
            raise ConfigurationError(
                'Handler is not instance of "RequestHandler"')
        self._handler = handler
        if 'session' not in self.handler.settings:
            raise ConfigurationError('Session is undefined')
        settings = copy.deepcopy(self.handler.settings.get('session'))
        if not settings:
            raise ConfigurationError('Settings empty')
        self._settings = settings
        self._client = KeyValueClientFactory.make(self.settings)

    @property
    def handler(self):
        return self._handler

    @property
    def settings(self):
        return self._settings

    @property
    def client(self):
        return self._client

    @property
    def data(self):
        return self.client.get(self.sid)

    @property
    def time_expires(self):
        return self.settings.get('expires', SESSION_EXPIRES)

    @property
    def is_empty(self):
        return not self.data

    @property
    def key(self):
        return self.data.keys()

    @property
    def sid(self):
        try:
            sid = self.handler.get_secure_cookie(SESSION_ID)
            if isinstance(sid, (tuple, list,)):
                sid = sid[0]
            return str(sid)
        except Exception:
            return None

    def verify_key(self, key):
        if key not in self.data:
            raise KeyError('Key "%s" not found' % key)

    @verify_keys
    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        data = self.data
        data[key] = value
        self._save(data)

    def update(self, **kwargs):
        data = self.data
        data.update(kwargs)
        self._save(data)

    @verify_keys
    def delete(self, key):
        data = self.data
        del data[key]
        self._save(data)

    def delete_multi(self, *args):
        data = self.data
        for key in args:
            if key not in data:
                raise KeyError('Key "%s" not found' % key)
            del data[key]
        self._save(data)

    def clear(self):
        self._save({})

    def revoke(self):
        self.client.delete(self.sid)

    def expires(self, expires):
        self._save(self.data, expires)

    def _save(self, value, expires=None):
        self.client.save(self.sid, value, expires or self.time_expires)

    def _make_sid(self):
        sid = str(uuid.uuid4())
        self.handler.set_secure_cookie(
            SESSION_ID, sid, 1, max_age=self.time_expires)
        return sid

    def start(self, value):
        sid = self._make_sid()
        if not value or not isinstance(value, dict):
            value = {}
        value['sid'] = sid
        self.client.save(sid, value, self.time_expires)
        return sid

    def destroy(self, sid):
        try:
            return self.client.delete(str(sid))
        except:
            return True


class SessionMixin(object):
    @property
    def session(self):
        session = getattr(self, '_session', None)
        if not isinstance(self, RequestHandler):
            raise TypeError('Class invalid, must be a tornado RequestHandler')
        elif not session or not isinstance(session, Session):
            session = Session(self)
            setattr(self, '_session', session)
        return session

    def validate_session(self):
        try:
            return self.verify_session()
        except Exception:
            return False

    def verify_session(self):
        session = self.session.data
        session_sid = session.get('sid')
        if not session_sid:
            raise KeyError('SID "%s" is not found.' % session_sid)
        elif self.session.sid != session_sid:
            raise ValueError(
                'SID "%s" not match "%s".' % (session_sid, self.session.sid))
        return True

    def start_session(self, user):
        if not self.validate_session():
            if not user or not isinstance(user, User):
                raise ValueError('User data undefined')
            if user.sid:
                self.session.destroy(user.sid)
            return self.session.start({
                'uid': str(user.id),
                'username': user.username,
                'company': user.company,
                'position': user.position,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone_lada': user.phone_lada,
                'phone_number': user.phone_number,
                'dispatch': user.dispatch,
                'permissions': dict(user.permissions)
            })
        return False

    def destroy_session(self):
        try:
            if self.validate_session():
                self.session.revoke()
            self.clear_cookie(SESSION_ID)
        except Exception:
            pass