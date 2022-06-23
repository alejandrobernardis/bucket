#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 26/Mar/2014 13:45

import emails
import datetime
from addicted.verify.core.utils import token, user_token
from addicted.verify.handlers.base import BaseHandler
from addicted.verify.models.audits import Audit
from addicted.verify.models.users import User, PreRegister
from addicted.verify.security.roles import perms_admin, perms_guest, \
    perms_user, role_admin, role_user, role_guest
from bson.objectid import ObjectId
from tornadomail import send_mail


class UserChangeStatusHandler(BaseHandler):
    @perms_admin.strict()
    def post(self, *args, **kwargs):
        try:
            user = User.objects(id=ObjectId(args[0])).first()
            user.set_enabled(not user.enabled)
            self.audit_push('Status service (change success): %s'
                            % user.username)
            return self.get_json_response_and_finish(
                response={'status': user.enabled}
            )
        except Exception as e:
            self.audit_push('Status service (change error): %s, %s'
                            % (args[0], e.message))
            return self.get_except_json_response_and_finish(e.message)


class UserChangeLevelHandler(BaseHandler):
    @perms_admin.strict()
    def post(self, *args, **kwargs):
        try:
            level = self.get_argument('level', '').encode('utf-8')
            if not level:
                raise ValueError('Por favor, defina el nivel que desea asignar')
            perms = {
                role_admin.key: perms_admin,
                role_user.key: perms_user,
                role_guest.key: perms_guest
            }
            if level not in perms.keys():
                raise ValueError('El nivel "%s", no se puede asignar' % level)
            user = User.objects(id=ObjectId(args[0])).first()
            if not user:
                raise ValueError('Usuario no disponible')
            elif level in user.permissions.keys():
                raise ValueError('El usuario ya dispone del nivel: %s' % level)
            user.set_update({'permissions': perms[level].to_object()})
            self.audit_push('Level service (change success): %s'
                            % user.username)
            return self.get_json_response_and_finish(
                response={'level': level.title()}
            )
        except Exception as e:
            self.audit_push('Level service (change error): %s, %s'
                            % (args[0], e.message))
            return self.get_except_json_response_and_finish(e.message)


class UserDeleteHandler(BaseHandler):
    @perms_admin.strict()
    def post(self, *args, **kwargs):
        try:
            user = User.objects(id=ObjectId(args[0])).first()
            if not user:
                raise ValueError('Usuario no disponible')
            user.set_logic_low()
            self.audit_push('Delete service (success): %s' % user.username)
            return self.get_json_response_and_finish()
        except Exception as e:
            self.audit_push('Delete service (error): %s, %s'
                            % (args[0], e.message))
            return self.get_except_json_response_and_finish(e.message)


class UserChangePasswordHandler(BaseHandler):
    @perms_admin.strict()
    def post(self, *args, **kwargs):
        try:
            user = User.objects(id=ObjectId(args[0])).first()
            if not user:
                raise ValueError('Usuario no disponible')
            try:
                user.set_activation_key()
            except Exception:
                raise ValueError(
                    u'La clave de validación no pudo ser generada.')
            try:
                send_mail(
                    u'Addicted / Socios / Recuperación de Contraseña',
                    emails.RECOVERY_PASSWORD % {
                        'username': user.first_name.split(' ')[0],
                        'activation_key': user.activation_key,
                        'site_domain': self.settings.get('site_domain'),
                    },
                    self.settings.get('email'),
                    [user.email],
                    connection=self.application.email_client
                )
                self.audit_push('Password service (change success): %s'
                                % user.username)
                return self.get_json_response_and_finish()
            except Exception:
                user.set_enabled()
                raise ValueError(u'Los pasos para la recuperación de su '
                                 u'contraseña, no han podido ser enviados.')
        except Exception as e:
            self.audit_push('Password service (change error): %s, %s'
                            % (args[0], e.message))
            return self.get_except_json_response_and_finish(e.message)


class UserViewActivityHandler(BaseHandler):
    @perms_admin.strict()
    def post(self, *args, **kwargs):
        try:
            username = self.get_argument('username', '').encode('utf-8')
            if not username:
                raise ValueError('El usuario no esta disponible.')
            date = datetime.datetime.utcnow() - datetime.timedelta(days=30)
            data = Audit.objects(
                user=username, created__gte=date
            ).order_by('-created')
            if not len(data):
                raise ValueError('No se encontraron resultados.')
            self.audit_push('Activity service (view success): %s' % username)
            return self.get_mongoengine_json_response_and_finish(data)
        except Exception as e:
            self.audit_push('Activity service (view error): %s, %s'
                            % (args[0], e.message))
            return self.get_except_json_response_and_finish(e.message)


class RegisterAllowHandler(BaseHandler):
    @perms_admin.strict()
    def post(self, *args, **kwargs):
        try:
            register = PreRegister.objects(
                id=ObjectId(args[0]), enabled=True
            ).first()
            if not register or User.objects(email=register.email).first():
                raise ValueError('Usuario no disponible')
            try:
                user = User()
                user.first_name = register.first_name
                user.last_name = register.last_name
                user.email = register.email
                user.phone_lada = register.phone_lada
                user.phone_number = register.phone_number
                user.policy = register.policy
                user.enabled = True
                user.available = True
                user.permissions = perms_user
                user.username = 'user_%s' % user_token(register.email, 6)
                password = token(8)
                user.password = password
                user.save()
            except Exception:
                raise ValueError('El usuario no puedo ser creado: %s' %
                                 register.id)
            try:
                send_mail(
                    u'Addicted / Socios / Datos de acceso',
                    emails.ACCESS % {
                        'site_domain': self.settings.get('site_domain'),
                        'first_name': user.first_name.split(' ')[0],
                        'email': user.email,
                        'username': user.username,
                        'password': password
                    },
                    self.settings.get('email'),
                    [user.email],
                    connection=self.application.email_client
                )
            except Exception:
                raise ValueError('El correo no pudo ser enviado a: %s'
                                 % user.email)
            try:
                register.set_update({
                    'enabled': False,
                    'available': False,
                    'token': '',
                    'activation_key': '',
                    'activation_hash': ''
                })
            except Exception:
                pass
            self.audit_push('Register service (allow success): %s'
                            % user.username)
            return self.get_json_response_and_finish()
        except Exception as e:
            self.audit_push('Register service (allow error): %s, %s'
                            % (args[0], e.message))
            return self.get_except_json_response_and_finish(e.message)


class RegisterDenyHandler(BaseHandler):
    @perms_admin.strict()
    def post(self, *args, **kwargs):
        try:
            user = PreRegister.objects(id=ObjectId(args[0])).first()
            if not user:
                raise ValueError('Usuario no disponible')
            user.set_logic_low()
            self.audit_push('Register service (deny success): %s'
                            % user.username)
            return self.get_json_response_and_finish()
        except Exception as e:
            self.audit_push('Register service (deny error): %s, %s'
                            % (args[0], e.message))
            return self.get_except_json_response_and_finish(e.message)


handlers_list = [
    (r'/s/user/change/level/([a-f0-9]{24})/?', UserChangeLevelHandler),
    (r'/s/user/change/password/([a-f0-9]{24})/?', UserChangePasswordHandler),
    (r'/s/user/change/status/([a-f0-9]{24})/?', UserChangeStatusHandler),
    (r'/s/user/delete/([a-f0-9]{24})/?', UserDeleteHandler),
    (r'/s/user/view/activity/([a-f0-9]{24})/?', UserViewActivityHandler),
    (r'/s/register/allow/([a-f0-9]{24})/?', RegisterAllowHandler),
    (r'/s/register/deny/([a-f0-9]{24})/?', RegisterDenyHandler),
]