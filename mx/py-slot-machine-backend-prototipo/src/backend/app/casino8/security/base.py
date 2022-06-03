#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 21/06/2013 09:27

import base64
import datetime
import string
import hashlib
from random import choice


# all

__all__ = [
    'secret_key',
    'secret_key_b64',
    'activation_key',
    'activation_key_b64',
    'token',
    'token_b64'
]


# secret_key

def secret_key(length=64):
    h = '%s-%s-%s-%s' % (
        datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f'),
        string.ascii_letters, string.digits, string.punctuation)
    return ''.join([choice(h) for _ in range(length)])


def secret_key_b64(length=64):
    return base64.b64encode(secret_key(length).encode())


# activation_key

def activation_key(username, email):
    h = hashlib.md5()
    h.update(('%s-%s-%s' % (username, email, secret_key())).encode())
    return h.hexdigest()


def activation_key_b64(username, email):
    return base64.b64encode(activation_key(username, email).encode())


# token

def token(length=32, include_date=False):
    h = hashlib.md5()
    h.update(secret_key(length).encode())
    v = ''.join([choice(h.hexdigest()) for _ in range(length)])
    if include_date:
        d = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        v = v[0:length - len(d)] + d
    return v


def token_b64(length=32, include_date=False):
    return base64.b64encode(token(length, include_date).encode())