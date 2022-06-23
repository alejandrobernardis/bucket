#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 26/Mar/2014 13:45

import base64
import datetime

import emails
from bson.objectid import ObjectId
from com.feedback.core.utils import token, user_token, mexico_time_zone, \
    secret_key, activation_key_b64
from com.feedback.handlers.base import BaseHandler
from com.feedback.models.audits import Audit
from com.feedback.models.users import User, PreRegister
from com.feedback.models.evaluations import EvaluationPending, Evaluation, \
    Answer
from com.feedback.security.roles import perms_admin, perms_user, role_admin, \
    role_user
from com.feedback.security.password import SHA256PasswordHasher
from com.feedback.ui_modules.utils import helper_rate
from mongoengine import Q
from tornadomail import send_mail
from tasks import push__client_notification, push__unavailable_obsolete_data


class UserChangeStatusHandler(BaseHandler):
    @perms_admin.strict()
    def post(self, *args, **kwargs):
        try:
            user = User.objects(id=ObjectId(args[0])).first()
            user.set_enabled(not user.enabled)
            self.audit_push('Status service (change success): %s'
                            % user.username)
            try:
                self.application.session_client().delete(user.sid)
                self.audit_push('Status service (session delete success): %s'
                                % user.username)
            except:
                self.audit_push('Status service (session delete error): %s'
                                % user.username)
            return self.get_json_response_and_finish(
                response={'token': str(user.id), 'status': user.enabled}
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
                role_user.key: perms_user
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


class UserChangeDispatchHandler(BaseHandler):
    @perms_admin.strict()
    def post(self, *args, **kwargs):
        try:
            level = self.get_argument('level', '').encode('utf-8')
            if not level:
                raise ValueError(u'Por favor, defina el ciclo de envío que '
                                 u'desea asignar')
            perms = {
                'cada semana': 1,
                'cada 2 semanas': 2,
                'cada 4 semanas': 3
            }
            if level.lower() not in perms.keys():
                raise ValueError('El nivel "%s", no se puede asignar' % level)
            user = User.objects(id=ObjectId(args[0])).first()
            if not user:
                raise ValueError('Usuario no disponible')
            elif level == user.dispatch:
                raise ValueError('El usuario ya dispone del ciclo: %s' % level)
            user.set_update({'dispatch': perms[level.lower()]})
            self.audit_push('Dispatch service (change success): %s'
                            % user.username)
            return self.get_json_response_and_finish(
                response={'dispatch': level.lower()}
            )
        except Exception as e:
            self.audit_push('Dispatch service (change error): %s, %s'
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
            push__unavailable_obsolete_data.delay(**{'client': user.username})
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
                # TODO: Migrate to Background Task.
                send_mail(
                    emails.RECOVERY_PASSWORD_SUBJECT,
                    emails.RECOVERY_PASSWORD % {
                        'username': user.first_name.split(' ')[0],
                        'activation_key': user.activation_key,
                        'site_domain': self.settings.get('site_domain'),
                    },
                    'Feedback by Figment <%s>' % self.settings.get('email'),
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
            ).order_by('-created').limit(1000)
            if not len(data):
                raise ValueError('No se encontraron resultados.')
            self.audit_push('Activity service (view success): %s' % username)
            return self.get_mongoengine_json_response_and_finish(data)
        except Exception as e:
            self.audit_push('Activity service (view error): %s, %s'
                            % (args[0], e.message))
            return self.get_except_json_response_and_finish(e.message)


class UserListExecutivesHandler(BaseHandler):
    @perms_admin.strict()
    def post(self, *args, **kwargs):
        try:
            executives = self.mongo.users.find({
                'permissions.admin': True,
                'username': {
                    '$nin': [
                        'sysadmin',
                        'administrator',
                        'administrador'
                    ]
                },
                'enabled': True,
                'available': True
            }, {
                '_id': 1,
                'first_name': 1,
                'last_name': 1,
                'username': 1,
                'email': 1,
                'company': 1
            }).limit(500).sort([('first_name', 1), ('last_name', 1)])
            if not executives:
                raise ValueError('No se encontraron resultados.')
            self.audit_push('List executives service (list success)')
            return self.get_mongo_json_response_and_finish(executives)
        except Exception as e:
            self.audit_push('List executives service (list error): %s'
                            % e.message)
            return self.get_except_json_response_and_finish(e.message)


class UserChangeExecutivesHandler(BaseHandler):
    @perms_admin.strict()
    def post(self, *args, **kwargs):
        try:
            try:
                executives = self.request.arguments['executives[]'] or []
            except:
                executives = []
            user = User.objects(id=ObjectId(args[0])).first()
            user.set_update({'executives': executives})
            self.audit_push('List executives service (list success): %s'
                            % ','.join(executives))
            return self.get_json_response_and_finish(response={
                'executives': executives, 'token': args[0]
            })
        except Exception as e:
            self.audit_push('List executives service (list error): %s'
                            % e.message)
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
                user.company = register.company
                user.position = register.position
                user.provider = register.provider
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
                # TODO: Migrate to Background Task.
                send_mail(
                    emails.ACCESS_SUBJECT,
                    emails.ACCESS % {
                        'site_domain': self.settings.get('site_domain'),
                        'first_name': user.first_name.split(' ')[0],
                        'email': user.email,
                        'username': user.username,
                        'password': password
                    },
                    'Feedback by Figment <%s>' % self.settings.get('email'),
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


class EvaluationChangeStatusHandler(BaseHandler):
    @perms_admin.strict()
    def post(self, *args, **kwargs):
        try:
            evaluation = Evaluation.objects(id=ObjectId(args[0])).first()
            evaluation.set_enabled(not evaluation.enabled)
            self.audit_push('Evaluation service (change success): %s'
                            % args[0])
            return self.get_json_response_and_finish(
                response={
                    'token': str(evaluation.id),
                    'status': evaluation.enabled
                }
            )
        except Exception as e:
            self.audit_push('Evaluation service (change error): %s, %s'
                            % (args[0], e.message))
            return self.get_except_json_response_and_finish(e.message)


class EvaluationAnswerModeHandler(BaseHandler):
    @perms_admin.strict()
    def post(self, *args, **kwargs):
        try:
            user = User.get_by_id(self.current_user.get('uid'))
            if not user:
                raise ValueError(u'Usuario no disponible.')
            answer = self.get_argument('answer', False)
            if not answer:
                raise ValueError(u'Por favor, escriba su respuesta.')
            evaluation = Evaluation.objects(id=ObjectId(args[1])).first()
            if not evaluation:
                raise ValueError(u'Evaluación no disponible.')
            client = User.get_by_username(evaluation.client)
            if not user:
                raise ValueError(u'Cliente no disponible.')
            a = Answer()
            a.username = user.username
            a.reference = user
            a.description = answer
            a.enabled = True
            a.available = True
            a.mode = {'message': 1, 'call': 2}[args[0].lower()]
            evaluation.set_update({'answers': [a]})
            self.audit_push(
                'Evaluation/Answer service (success): %s => %s via %s'
                % (user.username, evaluation.client, args[0].lower())
            )
            push__client_notification.delay(
                '%s %s <%s>' % (
                    client.first_name, client.last_name, client.email
                ),
                emails.NOTIFICATION_ANSWER_SUBJECT,
                emails.NOTIFICATION_ANSWER % {
                    'first_name': client.first_name.split(' ')[0],
                    'first_name_user': user.first_name.split(' ')[0],
                    'rate': helper_rate(evaluation.rate),
                    'comments': evaluation.description,
                    'answer': a.description,
                    'site_domain': self.settings.get('site_domain'),
                    'activation_key': evaluation.activation_key,
                    'phone': '%s %s' % (user.phone_lada, user.phone_number),
                    'email': user.email
                },
                '%s %s <%s>' % (
                    user.first_name, user.last_name, self.settings.get('email')
                )
            )
            return self.get_json_response_and_finish(response={
                'token': args[1],
                'answer': {
                    'username': a.username,
                    'description': a.description,
                    'mode': a.mode,
                    'created': mexico_time_zone(a.created),
                    'full_name': '%s %s' % (user.first_name, user.last_name)
                }
            })
        except Exception as e:
            self.audit_push('Evaluation/Answer service (error): %s, %s'
                            % (args[0], e.message))
            return self.get_except_json_response_and_finish(e.message)


class EvaluationSendHandler(BaseHandler):
    @perms_admin.strict()
    def post(self, *args, **kwargs):
        try:
            user = User.get_by_id(args[0])
            if not user:
                raise ValueError('Usuario no disponible')
            ep = EvaluationPending.get_by__first(Q(username=user.username))
            expires = datetime.datetime.utcnow() + datetime.timedelta(days=7)
            if not ep:
                ep = EvaluationPending()
                ep.username = user.username
                _token = secret_key()
                ep.token = _token
                ep.activation_key = \
                    activation_key_b64(user.username, user.email)
                _password = SHA256PasswordHasher().make(_token)
                _separator = _password.find('$', 1)
                ep.public_key = base64.encodestring(_password[_separator:]) \
                                      .replace('\n', '|')
                ep.public_key_method = _password[0:_separator]
                ep.public_key_expires = expires
                ep.private_key = secret_key(16)
                ep.enabled = True
                ep.available = True
                ep.save()
            else:
                ep.set_update({'public_key_expires': expires})
            public = base64.b64encode(ep.public_key)
            push__client_notification.delay(
                '%s %s <%s>' % (
                    user.first_name, user.last_name, user.email
                ),
                emails.NOTIFICATION_EVALUATION_SUBJECT,
                emails.NOTIFICATION_EVALUATION % {
                    'first_name': user.first_name.split(' ')[0],
                    'site_domain': self.settings.get('site_domain'),
                    'activation_key': public,
                }
            )
            return self.get_json_response_and_finish(response={
                'key': ep.activation_key,
                'public': public,
                'expires': mexico_time_zone(ep.public_key_expires)
            })
        except Exception as e:
            self.audit_push('Evaluation/Answer service (error): %s, %s'
                            % (args[0], e.message))
            return self.get_except_json_response_and_finish(e.message)


handlers_list = [
    # User
    (r'/s/user/change/level/([a-f0-9]{24})', UserChangeLevelHandler),
    (r'/s/user/change/password/([a-f0-9]{24})', UserChangePasswordHandler),
    (r'/s/user/change/status/([a-f0-9]{24})', UserChangeStatusHandler),
    (r'/s/user/change/dispatch/([a-f0-9]{24})', UserChangeDispatchHandler),
    (r'/s/user/delete/([a-f0-9]{24})/?', UserDeleteHandler),
    (r'/s/user/view/activity/([a-f0-9]{24})', UserViewActivityHandler),
    (r'/s/user/list/executives/([a-f0-9]{24})', UserListExecutivesHandler),
    (r'/s/user/change/executives/([a-f0-9]{24})',
     UserChangeExecutivesHandler),
    # Register
    (r'/s/register/allow/([a-f0-9]{24})', RegisterAllowHandler),
    (r'/s/register/deny/([a-f0-9]{24})', RegisterDenyHandler),
    # Evaluations
    (r'/s/evaluation/change/status/([a-f0-9]{24})',
     EvaluationChangeStatusHandler),
    (r'/s/evaluation/answer/(call|message)/([a-f0-9]{24})',
     EvaluationAnswerModeHandler),
    (r'/s/evaluation/send/([a-f0-9]{24})', EvaluationSendHandler)
]