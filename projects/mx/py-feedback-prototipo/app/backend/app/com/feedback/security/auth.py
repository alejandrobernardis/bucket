#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 04/Oct/2013 09:37

import urllib
import urlparse
from functools import wraps
from tornado.web import RequestHandler, HTTPError


STRICT_MODE = 'strict'
REQUIRED_MODE = 'required'
HTTP_ERROR = 404


def is_permissions(method):
    @wraps(method)
    def wrapper(self, other, *args, **kwargs):
        if not isinstance(other, Permission):
            raise TypeError('Value invalid, must be a Permission')
        return method(self, other, *args, **kwargs)
    return wrapper


def is_role(method):
    @wraps(method)
    def wrapper(self, other, *args, **kwargs):
        if not isinstance(other, Role):
            raise TypeError('Value invalid, must be a Role')
        return method(self, other, *args, **kwargs)
    return wrapper


class Role(object):
    def __init__(self, key, value=None):
        if not isinstance(key, basestring):
            raise TypeError('Key invalid, must be a string')
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    def _hash(self, other=None):
        if not isinstance(other, Role):
            other = self
        value = '%s$%s$%s' % (other.__class__.__name__, other.key, other.value)
        return hash(value)

    __hash__ = _hash

    @is_role
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __repr__(self):
        return '<%s key="%s" value="%s">' % \
               (self.__class__.__name__, self.key, self.value)

    def __str__(self):
        return '<%s="%s">' % (self.key, self.value)


PERMS_ADMIN = Role('admin', True)


class Permission(object):
    def __init__(self, *roles):
        if not roles:
            raise ValueError('List of roles not defined')
        self._roles = set(roles)

    def require(self, http_error=HTTP_ERROR, **kwargs):
        return AuthContext(self, REQUIRED_MODE, http_error, **kwargs)

    def strict(self, http_error=HTTP_ERROR, **kwargs):
        return AuthContext(self, STRICT_MODE, http_error, **kwargs)

    @property
    def roles(self):
        return self._roles

    @is_permissions
    def union(self, other):
        permissions = self.roles.union(other.roles)
        return Permission(*permissions)

    @is_permissions
    def intersection(self, other):
        permissions = self.roles.intersection(other.roles)
        return Permission(*permissions)

    @is_permissions
    def difference(self, other):
        permissions = self.roles.difference(other.roles)
        return Permission(*permissions)

    @is_permissions
    def symmetric_difference(self, other):
        permissions = self.roles.symmetric_difference(other.roles)
        return Permission(*permissions)

    def __repr__(self):
        return '<%s roles="%s">' % \
               (self.__class__.__name__, self.roles)

    def __str__(self):
        return '%s=Roles(%d)' % \
               (self.__class__.__name__, len(self.roles))

    def to_object(self):
        result = {}
        for item in self.roles:
            result[item.key] = item.value
        return result


class Identity(object):
    def __init__(self, user, *args):
        if not isinstance(user, dict):
            raise ValueError('User invalid, must be a dictionary')
        data = []
        for key, value in user.get('permissions', {'guest': True}).items():
            data.append(Role(key, value))
        self._user = user
        self._roles = set(data)
        self.add_roles(*args)

    @property
    def user(self):
        return self._user

    @property
    def roles(self):
        return self._roles

    @property
    def is_active(self):
        return self._user.get('enabled', False) \
            and self._user.get('available', False)

    @property
    def is_admin(self):
        return PERMS_ADMIN in self

    @is_role
    def add_role(self, other):
        try:
            self._roles.add(other)
        except Exception:
            raise ValueError('Role not supported: %s' % other)

    def add_roles(self, *args):
        for item in args:
            self.add_role(item)

    @is_role
    def remove_role(self, other):
        try:
            self._roles.remove(other)
        except Exception:
            raise ValueError('Role not found: %s' % other)

    def remove_roles(self, *args):
        for item in args:
            self.remove_role(item)

    @is_role
    def __contains__(self, item):
        try:
            return item in self._roles
        except Exception:
            return False

    def __repr__(self):
        return '<%s roles="%s">' % (self.__class__.__name__, self._roles)

    def __str__(self):
        return '%s=%d' % (self.__class__.__name__, len(self._roles))


class IdentityMixin(object):
    @property
    def identity(self):
        if not isinstance(self, RequestHandler):
            raise TypeError('Class invalid, must be a tornado RequestHandler')
        elif not hasattr(self, '_identity'):
            try:
                current_user = getattr(self, 'current_user')
                setattr(self, '_identity', Identity(current_user))
            except Exception:
                raise ValueError('Current user not defined')
        return getattr(self, '_identity')


class AuthContext(object):
    def __init__(self, permissions, mode, http_error, **kwargs):
        if not isinstance(permissions, Permission):
            raise TypeError('Permissions invalids, must be a Permission')
        elif not isinstance(mode, basestring):
            raise TypeError('Mode invalid, must be a string')
        mode = mode.lower()
        if mode not in (REQUIRED_MODE, STRICT_MODE,):
            raise ValueError('Mode not supported: %s' % mode)
        self._permissions = permissions
        self._mode = mode
        self._http_error = http_error or HTTP_ERROR
        self._options = kwargs or {}

    def validate(self, **kwargs):
        options = {}
        options.update(kwargs or {})
        options.update(self._options)
        handler = options.get('handler')
        if not isinstance(handler, RequestHandler):
            raise HTTPError(
                self._http_error,
                'Handler invalid, must be a tornado RequestHandler'
            )
        method = handler.request.method
        if method not in ('GET', 'POST',):
            raise HTTPError(
                self._http_error, 'Method not supported: %s' % method)
        elif not handler.current_user:
            url = handler.get_login_url()
            if '?' not in url:
                if urlparse.urlsplit(url).scheme:
                    url = handler.request.full_url()
                else:
                    next_url = {'next': handler.request.uri}
                    url = '%s?%s' % (url, urllib.urlencode(next_url))
            return handler.redirect(url)
        validator = options.get('validator')
        if hasattr(validator, 'context_validator'):
            validator = getattr(validator, 'context_validator')
        if validator and not options.get('ignore_context_validator'):
            return validator(context=self)
        elif not hasattr(handler, 'identity'):
            raise HTTPError(self._http_error, 'Identity not supported')
        roles = self._permissions.roles
        auth = getattr(handler, 'identity').roles.intersection(roles)
        if (self._mode == REQUIRED_MODE and not auth) \
                or (self._mode == STRICT_MODE and auth != roles):
            raise HTTPError(self._http_error)
        return True

    def __call__(self, method):
        context = self

        @wraps(method)
        def wrapper(ref, *args, **kwargs):
            if context.validate(handler=ref):
                return method(ref, *args, **kwargs)
        return wrapper

    def __enter__(self):
        self.validate()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False