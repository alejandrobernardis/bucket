#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 02/Dec/2013 16:59

from com.feedback.core.exceptions import ConfigurationError
from com.feedback.core.utils import purge_settings, import_module, \
    import_by_path


class KeyValueClient(object):
    def __init__(self, settings, serializer='pickle'):
        if not settings or not isinstance(settings, dict):
            raise ConfigurationError('Settings is undefined')
        self._settings = settings
        module = self.settings.get('serializer', serializer)
        try:
            self._serializer = import_module(module)
        except ImportError as e:
            raise ConfigurationError(
                'ImportError %s: %s' % (module, e.args[0]))
        if not hasattr(self.serializer, 'dumps') \
                or not hasattr(self.serializer, 'loads'):
            raise AttributeError(
                'Serializer "%s" does not define a "dumps/loads" attribute'
                % module)
        engine = self.settings.get('engine')
        if not engine:
            raise ValueError('Engine is undefined')
        try:
            self._engine = self._do_make_engine()
        except Exception:
            raise ValueError('Can\'t create the engine: %s' % engine)

    @property
    def engine(self):
        return self._engine

    @property
    def serializer(self):
        return self._serializer

    @property
    def settings(self):
        return self._settings

    def serialize(self, value):
        return self.serializer.dumps(value)

    def deserialize(self, value):
        return self.serializer.loads(value)

    def get(self, key):
        value = self._do_get(key)
        return self.deserialize(value) if value else {}

    def save(self, key, value, expires=None):
        value = self.serialize(value)
        expires = self.settings.get('expires', expires)
        self._do_save(key, value, expires)

    def delete(self, key):
        raise NotImplementedError()

    def _do_make_engine(self, *args, **kwargs):
        raise NotImplementedError()

    def _do_get(self, key):
        raise NotImplementedError()

    def _do_save(self, key, value, expires):
        raise NotImplementedError()

    def __repr__(self):
        return '<%s>' % self.__class__.__name__


class MemcachedClient(KeyValueClient):
    _arguments = ('servers', 'behaviors', 'binary', 'username', 'password',)

    def __init__(self, settings, serializer='pickle'):
        if settings and 'engine' not in settings:
            settings['engine'] = 'memcached'
        super(MemcachedClient, self).__init__(settings, serializer)

    def _do_make_engine(self, *args, **kwargs):
        path = 'pylibmc.Client'
        try:
            engine = import_by_path(path)
            return engine(**purge_settings(self.settings, self._arguments))
        except ImportError as e:
            raise ConfigurationError('ImportError %s: %s' % (path, e.args[0]))

    def _do_get(self, key):
        return self.engine.get(key)

    def _do_save(self, key, value, expires):
        self.engine.set(key, value, expires)

    def delete(self, key):
        return self.engine.delete(key)


class KeyValueClientFactory(object):
    @staticmethod
    def make(settings, **kwargs):
        if 'engine' not in settings:
            raise ConfigurationError('Engine is undefined')
        engine = settings.get('engine')
        if not engine:
            raise ValueError('Engine is empty')
        client = getattr(KeyValueClientFactory, '_%s_client' % engine)
        if not client:
            raise ValueError('Engine "%s" is not supported' % engine)
        return client(settings, **kwargs)

    @staticmethod
    def _memcached_client(settings, **kwargs):
        return MemcachedClient(settings, **kwargs)
