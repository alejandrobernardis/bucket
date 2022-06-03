#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: May 8, 2012, 2:15:17 PM

import functools
import hmac
import string
import urllib, urlparse

from com.ak.tornado.utils import safe_str_cmp
from datetime import datetime
from hashlib import md5, sha1
from random import choice
from tornado.web import HTTPError

#: -- helpers ------------------------------------------------------------------

__all__ = [
    "secret_key",
    "activation_key",
    "token",
    "Password",
    "Role",
    "authenticated_plus",
    "roles",
]

#: -- secret_key ---------------------------------------------------------------

def secret_key(length=32):
    h = "%s%s%s%s" % (
      datetime.utcnow().strftime("%Y%m%d%H%M%S%f"),
      string.letters,
      string.digits,
      string.punctuation)
    return "".join([choice(h) for _ in range(length)])

#: -- activation_key -----------------------------------------------------------

def activation_key(username, email):
    h = md5()
    h.update("%s%s%s" % (username, email, secret_key(64)))
    return unicode(h.hexdigest())

#: -- token --------------------------------------------------------------------

def token(length=32):
    h = md5()
    h.update(secret_key(length))
    h = unicode(h.hexdigest())
    d = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return "".join([choice(h) for _ in range(length-len(d))])+d

#: -- Password -----------------------------------------------------------------

class Password(object):

    @staticmethod
    def _hash(method, salt, password):
        _encoding = "utf-8"
        _hash_funcs = {"sha1": sha1, "md5": md5}
        if method == "plain":
            return password
        elif method not in _hash_funcs:
            return None
        elif salt:
            if isinstance(salt, unicode):
                salt = salt.encode(_encoding)
            h = hmac.new(salt, None, _hash_funcs[method])
        else:
            h = _hash_funcs[method]()
        if isinstance(password, unicode):
            password = password.encode(_encoding)
        h.update(password)
        return h.hexdigest()

    @staticmethod
    def gen_salt(length):
        if length <= 0:
            raise ValueError("Requested salt of length <= 0")
        h = string.letters + string.digits
        return "".join(choice(h) for _ in xrange(length))

    @staticmethod
    def generate(password, method="sha1", salt_length=8):
        salt = method != "plain" and Password.gen_salt(salt_length) or ""
        h = Password._hash(method, salt, password)
        if h is None:
            raise TypeError("Invalid method %r" % method)
        return "%s$%s$%s" % (method, salt, h)

    @staticmethod
    def check(password, password_hash):
        if password_hash.count("$") < 2:
            return False
        method, salt, hashval = password_hash.split("$", 2)
        return safe_str_cmp(Password._hash(method, salt, password), hashval)

#: -- Roles --------------------------------------------------------------------

class Role(object):
    #: perms

    __perms_read  = 1 << 0
    __perms_write = 1 << 16
    __perms_admin = 1 << 32

    #: methods

    def __init__(self, name, write=False, admin=False, level=0):

        if not hasattr(Role, "_roles"):
            Role._roles = dict()

        self._name = name
        self._level = level

        self._perms = self.__perms_read

        if write:
            self._perms = self._perms\
                        | self.__perms_write

        if admin:
            self._perms = self._perms\
                        | self.__perms_write\
                        | self.__perms_admin

        if level != 0:
            self._perms = self._perms\
                        | level

        if not Role._roles.has_key(name):
            Role._roles[name] = self

    @property
    def name(self):
        return self._name if hasattr(self, "_name") else None

    @property
    def permissions(self):
        return self._perms if hasattr(self, "_perms") else -1

    @property
    def is_admin(self):
        return self.permissions >= self.__perms_admin

    @property
    def is_writer(self):
        return self.permissions >= self.__perms_write

    @property
    def is_reader(self):
        return self.permissions >= self.__perms_read

    @staticmethod
    def get_roles():
        return Role._roles.copy()

    @staticmethod
    def get_role(key=None):
        if key and Role._roles.has_key(key):
            return Role._roles.get(key)
        return None

    @staticmethod
    def get_role_by_value(rid=None):
        if rid and Role._roles:
            for r in Role._roles.items():
                if r[1].permissions == rid:
                    return r[1]
        return None

    @staticmethod
    def get_admin_value():
        return Role.__perms_admin

    @staticmethod
    def get_writer_value():
        return Role.__perms_write

    @staticmethod
    def get_reader_value():
        return Role.__perms_read

    def __repr__(self):
        return str(dict(name=self.name,
                        permissions=self.permissions))

#: -- wrappers -----------------------------------------------------------------

def authenticated_plus(*roles):
    def wrap(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if self.request.method in ("GET", "POST", "HEAD"):
                if not self.current_user:
                    url = self.get_login_url()
                    if "?" not in url:
                        if urlparse.urlsplit(url).scheme:
                            next_url = self.request.full_url()
                        else:
                            next_url = self.request.uri
                        url += "?" + urllib.urlencode(dict(next=next_url))
                    self.redirect(url)
                    return
                else:
                    user = self.get_user_value("role")
                    perms = Role.get_role_by_value(user).name
                    if perms in roles:
                        return method(self, *args, **kwargs)
            raise HTTPError(403)
        return wrapper
    return wrap

def roles(*roles):
    def wrap(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if self.current_user:
                user = self.get_user_value("role")
                perms = Role.get_role_by_value(user).name
                if perms in roles:
                    return method(self, *args, **kwargs)
            raise HTTPError(403)
        return wrapper
    return wrap

