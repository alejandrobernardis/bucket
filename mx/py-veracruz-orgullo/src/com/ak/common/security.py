#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Asumi Kamikaze Inc.
# Copyright (c) 2012 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Sep 5, 2012 1:16:14 AM

import hmac
import string
from com.ak.common.utils import safe_str_cmp 
from datetime import datetime
from hashlib import md5, sha1
from random import choice

#: -- helpers ------------------------------------------------------------------

__all__ = ['secret_key','activation_key','toke', 'Password']

#: -- secret_key ---------------------------------------------------------------

def secret_key(length=32):
    h = '%s%s%s%s' % (
      datetime.utcnow().strftime('%Y%m%d%H%M%S%f'),
      string.letters, 
      string.digits, 
      string.punctuation)
    return ''.join([choice(h) for _ in range(length)])

#: -- activation_key -----------------------------------------------------------

def activation_key(username, email):
    h = md5()
    h.update('%s%s%s' % (username, email, secret_key(64)))
    return unicode(h.hexdigest())

#: -- token --------------------------------------------------------------------

def token(length=32, include_string='', include_date=True):
    h = md5()
    h.update(secret_key(length) + include_string)
    h = unicode(h.hexdigest())
    t = ''.join([choice(h) for _ in range(length)])
    if include_date and length > 16:
        d = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        t = t[0:length-len(d)] + d
    return t

#: -- Password -----------------------------------------------------------------

class Password(object):
    
    @staticmethod
    def _hash(method, salt, password):
        _encoding = 'utf-8'
        _hash_funcs = {'sha1': sha1, 'md5': md5}
        if method == 'plain':
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
            raise ValueError('Requested salt of length <= 0')
        h = string.letters + string.digits
        return ''.join(choice(h) for _ in xrange(length))
    
    @staticmethod
    def generate(password, method='sha1', salt_length=8):
        salt = method != 'plain' and Password.gen_salt(salt_length) or ''
        h = Password._hash(method, salt, password)
        if h is None:
            raise TypeError('Invalid method %r' % method)
        return '%s$%s$%s' % (method, salt, h)
    
    @staticmethod
    def check(password, password_hash):
        if password_hash.count('$') < 2:
            return False
        method, salt, hashval = password_hash.split('$', 2)
        return safe_str_cmp(Password._hash(method, salt, password), hashval)
    