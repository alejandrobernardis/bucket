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


for folder in ('../app', '../../../lib',):
    folder_path = os.path.abspath(os.path.join(ROOT_PATH, folder))
    if os.path.isdir(folder_path):
        sys.path.insert(0, folder_path)


import time
import copy
import settings
import traceback
import emails
import smtplib
from addicted.verify.core.utils import random_password

from addicted.verify.core.utils import trace_error
from addicted.verify.models.audits import *
from addicted.verify.models.users import *
from addicted.verify.security.roles import *
from email.mime.text import MIMEText
from mongoengine import register_connection


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
    PreRegister.drop_collection()


def users_create(users=None):
    if not isinstance(users, (tuple, list,)):
        raise TypeError(u'Users debe se una tupla o lista')
    User.drop_collection()
    for user in users:
        if not isinstance(users, (tuple, list,)):
            raise TypeError(u'User debe se una tupla o lista: '
                            u'[username, password, email, first_name, last_name'
                            u',phone_lada, phone_number, permissions]')
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
        try:
            u.save()
            v = User.objects(username=u.username).first()
            try:
                print v.username, password, v.email, v.permissions
            except Exception:
                print u'Verificación (%s):' % u.username, v
        except Exception:
            print 'User:', user
            print traceback.format_exc()


def users_send_mail(users=None, ignore=None):
    email_cfg = settings.EMAIL
    server = smtplib.SMTP(email_cfg.get('host'), email_cfg.get('port'))
    server.set_debuglevel(1)
    server.starttls()
    server.login(email_cfg.get('username'), email_cfg.get('password'))
    from_address = email_cfg.get('email')
    for item in users:
        if ignore and item[0] in ignore:
            continue
        try:
            body = emails.ACCESS % {
                'site_domain': settings.SITE_DOMAIN,
                'first_name': item[3].split(' ')[0],
                'email': item[2],
                'username': item[0],
                'password': item[1]
            }
            msg = MIMEText(body.encode('utf-8'))
            msg['Subject'] = 'Addicted / Socios / Datos de acceso'
            msg['From'] = 'Addicted <%s>' % from_address
            msg['To'] = item[2]
            server.sendmail(from_address, [item[2]], msg.as_string())
            print u'El envío de email fue exitoso: %s' % item[2]
            time.sleep(1)
        except Exception as e:
            trace_error(e.message.encode('utf-8'))
            raise ValueError(u'El envío de email falló: %s' % item[0])


users_list = (
    ('sysadmin', 'j!$.5IX47r=', 'sysadmin@kinetiq.com.mx',
     'Sysadmin', 'Kinetiq', '+5255', '15796498', perms_admin,),
    ('syssupport', 'Y$!3+S.Wz4=', 'support@kinetiq.com.mx',
     'Support', 'Kinetiq', '+5255', '15796498', perms_admin,),
    ('concierge', 'Y$33+GeR.z3', 'concierge@kinetiq.com.mx',
     'Concierge', 'Kinetiq', '+5255', '15796498', perms_user,),
    ('bernardisa', 'kqAM!x07nb+', 'alejandro.bernardis@kinetiq.com.mx',
     'Alejandro', 'Bernardis', '+5255', '15796498', perms_admin,),
    ('floresre', 'R3!nE$fL+0r3s', 'rene@kinetiq.com.mx',
     u'René', 'Flores', '+5255', '15796498', perms_admin,),
    ('floresos', 'O5!i#lF10r3$', 'ossiel@kinetiq.com.mx',
     'Ossiel', 'Flores', '+5255', '15796498', perms_admin,),
    ('denovaar', 'A#T!uRd03NN=', 'adenova@kinetiq.com.mx',
     'Arturo', 'De Nova', '+5255', '15796498', perms_admin,),
)


def run():
    if raw_input('- Reiniciar la base de datos  [y/N]--> ') == 'y':
        drop_collections()
    if raw_input('\n- Crear usuarios  [y/N]--> ') == 'y':
        users_create(users_list)
    if raw_input('\n- Enviar emails [y/N]--> ') == 'y':
        users_send_mail(users_list, ('sysadmin', 'syssupport', 'concierge',))


if __name__ == '__main__':
    run()