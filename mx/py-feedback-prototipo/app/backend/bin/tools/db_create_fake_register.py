#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 20/Feb/2014 23:28

import os
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


for folder in ('../../app', '../../../../lib',):
    folder_path = os.path.abspath(os.path.join(ROOT_PATH, folder))
    if os.path.isdir(folder_path):
        sys.path.insert(0, folder_path)

import time
import settings
from com.feedback.core.utils import *
from com.feedback.models.users import *
from com.feedback.security.password import SHA1PasswordHasher
from mongoengine import register_connection
from random import choice


for key, value in settings.DATABASE.items():
    database = copy.deepcopy(value)
    register_connection(
        alias=key,
        name=database.get('name'),
        username=database.get('username'),
        password=database.get('password'),
        **database.get('settings', {})
    )


def users_create(users=None):
    if not isinstance(users, (tuple, list,)):
        raise TypeError(u'Users debe ser una tupla o lista')
    PreRegister.drop_collection()
    for user in users:
        if not isinstance(user, dict):
            raise TypeError(u'User debe ser un dict')
        u = PreRegister()
        u.email = user.get('email')
        u.first_name = user.get('first_name')
        u.last_name = user.get('last_name')
        u.phone_lada = user.get('phone_lada')
        u.phone_number = user.get('phone_number')
        u.enabled = True
        u.available = True
        u.policy = True
        u.company = user.get('company')
        u.position = user.get('position')
        u.provider = user.get('provider')
        u.token = user.get('token')
        u.activation_key = user.get('activation_key')
        u.remote_ip = user.get('remote_ip')
        if 'activation_hash' in user:
            u.activation_hash = user.get('activation_hash')
        try:
            u.save()
            v = PreRegister.objects(email=u.email).first()
            try:
                print v.first_name, v.last_name, v.email
            except Exception as e:
                print u'Verificación (%s):' % u.email, e.message
        except Exception:
            print 'User:', user
            print traceback.format_exc()
        time.sleep(.5)


users_list = []


for i in xrange(100, 110):
    _token = token(8)
    _activation_key = token_b64()

    _obj = {
        "first_name": "Nombre",
        "last_name": "Apellido",
        "email": "client_%s@client.com.mx" % i,
        "phone_lada": "+000",
        "phone_number": "0000 0000",
        "policy": True,
        "company": "Empresa",
        "position": "Cargo",
        "provider": choice([1, 2, 3]),
        "remote_ip": "127.0.0.1",
        "token": _token,
        "activation_key": _activation_key
    }

    if choice([True, False]):
        _obj["activation_hash"] = \
            SHA1PasswordHasher().make('%s:%s' % (_token, _activation_key))

    users_list.append(_obj)


def run():
    ignore = raw_input('- Ignorar alertas [y/N]--> ') == 'y'
    if ignore or raw_input('\n- Crear usuarios  [y/N]--> ') == 'y':
        users_create(users_list)


if __name__ == '__main__':
    run()