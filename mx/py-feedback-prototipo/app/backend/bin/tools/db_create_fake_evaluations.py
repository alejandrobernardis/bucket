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


import copy
import settings
import traceback
from com.feedback.core.utils import random_password, token_b64
from com.feedback.models.audits import *
from com.feedback.models.evaluations import *
from com.feedback.models.users import *
from com.feedback.security.roles import *
from mongoengine import register_connection
from random import choice

USER_REFERENCE = []
CLIENT_REFERENCE = []
SYSADMIN_OID = None

for key, value in settings.DATABASE.items():
    database = copy.deepcopy(value)
    register_connection(
        alias=key,
        name=database.get('name'),
        username=database.get('username'),
        password=database.get('password'),
        **database.get('settings', {})
    )


def drop_collections():
    Audit.drop_collection()
    Logs.drop_collection()
    User.drop_collection()
    Evaluation.drop_collection()
    EvaluationPending.drop_collection()


def users_create(users=None):
    global SYSADMIN_OID
    if not isinstance(users, (tuple, list,)):
        raise TypeError(u'Users debe se una tupla o lista')
    for user in users:
        if not isinstance(user, (tuple, list,)):
            raise TypeError(u'User debe se una tupla o lista')
        u = User()
        u.username = user[0]
        password = user[1] or random_password(8)
        u.password = password
        u.email = user[2]
        u.first_name = user[3]
        u.last_name = user[4]
        u.phone_lada = user[5]
        u.phone_number = user[6]
        u.enabled = True
        u.available = True
        u.policy = True
        u.permissions = user[7]
        u.company = user[8]
        u.position = '--'
        u.provider = choice([1, 2, 3])
        u.dispatch = choice([1, 2, 4])
        u.sid = ''

        if SYSADMIN_OID and str(user[0]).startswith('client'):
            u.executives = [SYSADMIN_OID]

        try:
            u.save()
            v = User.objects(username=u.username).first()
            try:
                if v.username == 'bernardisa':
                    SYSADMIN_OID = str(v.id)
                if not str(v.username).startswith('client'):
                    USER_REFERENCE.append(v)
                else:
                    CLIENT_REFERENCE.append(v)
                print v.username, password, v.email, v.permissions
            except Exception:
                print u'Verificación (%s):' % u.username, v
        except Exception:
            print 'User:', user
            print traceback.format_exc()


def evaluations_create(evaluations=100):
    for evaluation in xrange(evaluations):
        user = choice(USER_REFERENCE)
        client = choice(CLIENT_REFERENCE)
        c = Evaluation(enabled=True, available=True)
        c.client = client.username
        c.reference = client
        c.description = 'Lorem ipsum dolor sit amet, consectetur adipiscing ' \
                        'elit. Ut non metus vel lacus iaculis venenatis. Viv' \
                        'amus quis lacus eros.\nDonec in imperdiet nisi. Nunc' \
                        ' est orci, sodales vel leo in, varius iaculis neque' \
                        '. Curabitur ut enim eget quam vehicula euismod quis' \
                        ' ac nulla. Maecenas eget mollis erat. Sed ac ornare' \
                        ' massa, ac tempor nisl.\nVestibulum posuere malesuad' \
                        'a orci vitae suscipit. Vivamus et feugiat est.'
        c.rate = choice([1, 2, 3, 4, 5])
        c.provider = client.provider

        if False:  # choice([True, False]):
            a = Answer()
            a.username = user.username
            a.reference = user
            a.description = 'Lorem ipsum dolor sit amet, consectetur adipisci' \
                            'ng elit. Ut non metus vel lacus iaculis venenati' \
                            's. Vivamus quis lacus eros.\nDonec in imperdiet ' \
                            'nisi.'
            a.mode = choice([1, 2])
            c.answers = [a]
        else:
            c.answers = []

        c.activation_key = token_b64()
        c.policy = True
        c.save()
        print c.client, c.answers


users_list = [
    ('sysadmin', 'j!$.5IX47r=', 'sysadmin@figment.com.mx',
     'Sysadmin', 'Figment', '+52 1 55', '1579 6498', perms_admin, 'Figment'),
    ('syssupport', 'Y$!3+S.Wz4=', 'support@figment.com.mx',
     'Support', 'Figment', '+52 1 55', '1579 6498', perms_admin, 'Figment'),
    ('bernardisa', 'kqAM!x07nb+', 'alejandro.bernardis@figment.com.mx',
     'Alejandro', 'Bernardis', '+52 1 55', '1579 6498', perms_admin,
     'Figment'),
    ('floresre', 'R3!nE$fL+0r3s', 'rene@figment.com.mx',
     u'René', 'Flores', '+52 1 55', '1579 6498', perms_admin, 'Figment'),
    ('floresos', 'O5!i#lF10r3$', 'ossiel@figment.com.mx',
    'Ossiel', 'Flores', '+52 1 55', '1579 6498', perms_admin, 'Figment'),
    ('ellsteinr', 'E5ll!i#lT3!r3n$', 'ricardo@figment.com.mx',
     'Ricardo', 'Ellstein', '+52 1 55', '1579 6498', perms_admin, 'Figment')
]


for i in xrange(100, 200):
    users_list.append(
        (
            'client_%s' % i,
            'client_%s' % i,
            'client_%s@yopmail.com' % i,
            'Nombre',
            'Apellido',
            '+000',
            '00 00 00 00 00',
            perms_user,
            'Empresa'
        )
    )


def run():
    ignore = raw_input('- Ignorar alertas [y/N]--> ') == 'y'
    if ignore or raw_input('- Reiniciar la base de datos  [y/N]--> ') == 'y':
        drop_collections()
    if ignore or raw_input('\n- Crear usuarios  [y/N]--> ') == 'y':
        users_create(users_list)
    if ignore or raw_input('\n- Crear comentarios  [y/N]--> ') == 'y':
        evaluations_create(101)


if __name__ == '__main__':
    run()