#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 04/Oct/2013 09:42

import string
import random
from addicted.verify.core.exceptions import ConfigurationError
from addicted.verify.core.utils import safe_str_cmp, import_by_path
from functools import wraps


SEPARATOR = '$'
MAXIMUM_PASSWORD_LENGTH = 4096
MINIMUM_PASSWORD_LENGTH = 8
MAXIMUM_SALT_LENGTH = 64


def validate_password(length):
    def inner(fn):
        @wraps(fn)
        def wrapper(self, password, *args, **kwargs):
            password_len = len(password)
            if password_len < length or password_len > MAXIMUM_PASSWORD_LENGTH:
                raise ValueError(
                    'Invalid password, must be greater than or equal to %s'
                    % length
                )
            return fn(self, password, *args, **kwargs)
        return wrapper
    return inner


class PasswordHasher(object):
    _library = None
    _algorithm = None

    @validate_password(MINIMUM_PASSWORD_LENGTH)
    def make(self, password, unsalted=False):
        if isinstance(unsalted, basestring):
            salt = unsalted
        elif not unsalted:
            salt = self._salt()
        algorithm = self._hasher()
        if salt:
            module = import_by_path('hmac.new')
            hasher = module(salt.encode(), None, algorithm)
        else:
            hasher = algorithm()
        hasher.update(password.encode())
        return "%s%s%s%s%s" % (
            self._algorithm, SEPARATOR, salt, SEPARATOR, hasher.hexdigest())

    def verify(self, password, password_hash):
        if password_hash.count(SEPARATOR) < 2:
            return False
        salt = password_hash.split(SEPARATOR)
        return safe_str_cmp(self.make(password, salt[1]), password_hash)

    def _hasher(self):
        if not self._library or not self._algorithm:
            raise ValueError('Library and/or Algorithm are undefined')
        path = '%s.%s' % (self._library, self._algorithm)
        try:
            return import_by_path(path)
        except ImportError as e:
            raise ConfigurationError('ImportError %s: %s' % (path, e.args[0]))

    def _salt(self):
        h = string.ascii_letters + string.digits
        return ''.join([random.choice(h) for _ in xrange(MAXIMUM_SALT_LENGTH)])


class SHA1PasswordHasher(PasswordHasher):
    _library = 'hashlib'
    _algorithm = 'sha1'


class MD5PasswordHasher(PasswordHasher):
    _library = 'hashlib'
    _algorithm = 'md5'
