#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 15/Mar/2014 13:29

from __future__ import division
import os
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

for folder in ('../app', '../../../lib',):
    folder_path = os.path.abspath(os.path.join(ROOT_PATH, folder))
    if os.path.isdir(folder_path):
        sys.path.insert(0, folder_path)

import copy
import emails
import settings
import smtplib
from addicted.verify.core.utils import user_token, secret_key, random_password
from addicted.verify.core.regex import regex_email, regex_user, \
    regex_password, regex_phone_lada, regex_phone_number, regex_option
from addicted.verify.models.users import User
from addicted.verify.security.roles import perms_guest, perms_user, perms_admin
from email.mime.text import MIMEText
from mongoengine import register_connection
from optparse import OptionParser

opts = None

for key, value in settings.DATABASE.items():
    database = copy.deepcopy(value)
    register_connection(
        alias=key,
        name=database.get('name'),
        username=database.get('username'),
        password=database.get('password'),
        **database.get('settings', {})
    )


def options_parser():
    parser = OptionParser()
    parser.add_option('--username', dest='username', default=None, type='string')
    parser.add_option('--password', dest='password', default=None, type='string')
    parser.add_option('--email', dest='email', default=None, type='string')
    parser.add_option('--first-name', dest='first_name', default=None, type='string')
    parser.add_option('--last-name', dest='last_name', default=None, type='string')
    parser.add_option('--phone-lada', dest='phone_lada', default=None, type='string')
    parser.add_option('--phone-number', dest='phone_number', default=None, type='string')
    parser.add_option('--perms-admin', action='store_true', dest='perms_admin', default=False)
    parser.add_option('--perms-user', action='store_true', dest='perms_user', default=False)
    parser.add_option('--perms-guest', action='store_true', dest='perms_guest', default=False)
    parser.add_option('--enabled', action='store_true', dest='enabled', default=False)
    parser.add_option('--available', action='store_true', dest='available', default=False)
    parser.add_option('-i', action='store_true', dest='ignore', default=False)
    return parser.parse_args()


def verify_mongo_value(**kwargs):
    return User.objects(**kwargs).first()


def raw_username():
    if opts.username and regex_user.search(opts.username) \
            and not verify_mongo_value(username=opts.username):
        return True
    default = ''
    while True:
        default = 'user_%s' % user_token(opts.email or secret_key(), 6)
        if not verify_mongo_value(username=default):
            break
    username = raw_input('Nombre de usuario (%s): ' % default)
    try:
        if not username or not len(username):
            username = default
        elif not regex_user.search(username):
            raise ValueError(u'El usuario no es válido')
        elif verify_mongo_value(username=username):
            raise ValueError('El usuario ya fue registrado')
    except Exception as e:
        print '  (e): %s' % e.message.encode('utf-8')
        return raw_username()
    opts.username = username
    return True


def raw_password():
    if opts.password and regex_password.search(opts.password):
        return True
    default = random_password()
    password = raw_input(u'Contraseña (%s): '.encode('utf-8') % default)
    try:
        if not password or not len(password):
            password = default
        elif not regex_password.search(password):
            raise ValueError(u'La contraseña no es válida')
    except Exception as e:
        print '  (e): %s' % e.message.encode('utf-8')
        return raw_password()
    opts.password = password
    return True


def raw_email():
    if opts.email and not verify_mongo_value(email=opts.email):
        return True
    email = raw_input('Email: ')
    try:
        if not email or not len(email):
            raise ValueError('Por favor, define un email')
        elif not regex_email.search(email):
            raise ValueError(u'El email no es válido')
        elif verify_mongo_value(email=email):
            raise ValueError('El email ya se encuentra registrado')
    except Exception as e:
        print '  (e): %s' % e.message.encode('utf-8')
        return raw_email()
    opts.email = email
    return True


def raw_first_name():
    if opts.first_name:
        return True
    first_name = raw_input('Nombre(s): ')
    try:
        if not first_name or len(first_name) < 3:
            raise ValueError('Por favor, define un nombre')
    except Exception as e:
        print '  (e): %s' % e.message.encode('utf-8')
        return raw_first_name()
    opts.first_name = first_name
    return True


def raw_last_name():
    if opts.last_name:
        return True
    last_name = raw_input('Apellidos(s): ')
    try:
        if not last_name or len(last_name) < 3:
            raise ValueError('Por favor, define un apellido')
    except Exception as e:
        print '  (e): %s' % e.message.encode('utf-8')
        return raw_last_name()
    opts.last_name = last_name
    return True


def raw_phone_lada():
    if opts.phone_lada and regex_phone_lada.search(opts.phone_lada):
        return True
    phone_lada = raw_input('Lada: ')
    try:
        if not phone_lada or not len(phone_lada):
            raise ValueError('Por favor, define un lada')
        elif not regex_phone_lada.search(phone_lada):
            raise ValueError(u'El lada no es válido')
    except Exception as e:
        print '  (e): %s' % e.message.encode('utf-8')
        return raw_phone_lada()
    opts.phone_lada = phone_lada
    return True


def raw_phone_number():
    if opts.phone_number and regex_phone_number.search(opts.phone_number):
        return True
    phone_number = raw_input(u'Teléfono: '.encode('utf-8'))
    try:
        if not phone_number or not len(phone_number):
            raise ValueError(u'Por favor, define un número de teléfono')
        elif not regex_phone_number.search(phone_number):
            raise ValueError(u'El número de teléfono no es válido')
    except Exception as e:
        print '  (e): %s' % e.message.encode('utf-8')
        return raw_phone_number()
    opts.phone_number = phone_number
    return True


def raw_permissions():
    if (opts.perms_admin and opts.perms_user and opts.perms_guest) or \
            (not opts.perms_admin and not opts.perms_user and not opts.perms_guest):
        permissions = raw_input('Permisos (1 - Guest "default", 2 - User, 3 - Admin): ')
        try:
            if not permissions or not len(permissions) \
                    or not regex_option.search(permissions):
                raise ValueError(u'La opción "%s" no es válida' % permissions)
            opts.permissions = \
                (None, perms_guest, perms_user, perms_admin)[int(permissions)]
        except Exception as e:
            print '  (e): %s' % e.message.encode('utf-8')
            return raw_permissions()
    elif opts.perms_admin:
        opts.permissions = perms_admin
    elif opts.perms_user:
        opts.permissions = perms_user
    elif opts.perms_guest:
        opts.permissions = perms_guest
    return True


def validate():
    return raw_username() \
        and raw_password() and raw_email() \
        and raw_first_name() and raw_last_name() \
        and raw_phone_lada() and raw_phone_number() \
        and raw_permissions()


def run():
    global opts, args
    opts, args = options_parser()

    print u'--'

    if validate():
        u = User()
        u.username = str(opts.username).lower()
        u.password = opts.password
        u.email = str(opts.email).lower()
        u.first_name = str(opts.first_name).title()
        u.last_name = str(opts.last_name).title()
        u.phone_lada = opts.phone_lada
        u.phone_number = str(opts.phone_number).lower()
        u.enabled = opts.enabled
        u.available = opts.available
        u.policy = True
        u.permissions = opts.permissions

        if not opts.ignore:
            save_user = raw_input('\n---\n>>> Crear al usuario [y/N] --> ')
            if save_user != 'y':
                raise ValueError('Proceso cancelado')

        try:
            u.save()
            v = verify_mongo_value(username=u.username)

            try:
                print u'\n---\n+ Verificación:'
                print 'email:', v.email
                print 'username:', v.username
                print 'password:', opts.password

            except Exception:
                raise ValueError(u'La verificación del usuario "%s" falló')

            if not opts.ignore:
                send_email = raw_input('\n---\n>>> Enviar email [y/N] --> ')
                if send_email != 'y':
                    raise ValueError('Proceso cancelado')

            try:
                print '\n---\n+ Correo enviado...',
                email_cfg = settings.EMAIL

                server = smtplib.SMTP(
                    email_cfg.get('host'), email_cfg.get('port'))

                server.starttls()

                server.login(
                    email_cfg.get('username'), email_cfg.get('password'))

                from_address = email_cfg.get('email')

                body = emails.ACCESS % {
                    'site_domain': settings.SITE_DOMAIN,
                    'first_name': v.first_name.split(' ')[0],
                    'email': v.email,
                    'username': v.username,
                    'password': opts.password
                }

                msg = MIMEText(body.encode('utf-8'))
                msg['Subject'] = 'Addicted / Socios / Datos de acceso'
                msg['From'] = from_address
                msg['To'] = v.email

                server.sendmail(from_address, [v.email], msg.as_string())
                print server.quit()

            except Exception:
                raise ValueError(u'El envío de email falló')

        except Exception as e:
            raise ValueError(e.message.encode('utf-8'))


if __name__ == '__main__':
    try:
        run()
    except Exception as er:
        print ' - %s' % er.message.encode('utf-8')
    except KeyboardInterrupt:
        pass
