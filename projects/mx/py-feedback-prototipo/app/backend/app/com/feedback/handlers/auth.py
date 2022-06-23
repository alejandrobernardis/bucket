#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 19/Feb/2014 18:19

import base64
import emails
import settings
from com.feedback.core.regex import regex_activation_key, \
    regex_activation_key_64, regex_object_id
from com.feedback.core.utils import safe_str_cmp, token_b64, token, \
    user_token
from com.feedback.forms.common import SignInForm, RequestForm, RecoveryForm, \
    RecoveryVerifyForm, RecoveryPasswordForm
from com.feedback.handlers.base import BaseHandler, CommonBaseHandler
from com.feedback.models.users import User, PreRegister
from com.feedback.security.password import SHA1PasswordHasher
from com.feedback.security.roles import perms_user
from com.feedback.security.session import verify_session_status
from bson import ObjectId
from tornado.escape import json_decode, json_encode
from tornadomail import send_mail


RECOVERY_ID = 'ari'


class SignInHandler(CommonBaseHandler):
    _form = SignInForm
    _template = 'auth/signin.html'

    @verify_session_status
    def get(self, *args, **kwargs):
        return self.render()

    @verify_session_status
    def post(self, *args, **kwargs):
        form = self._form(self.request.arguments)
        if form.validate():
            try:
                username = form.username.data
                user, auth = \
                    User.auth_login(username, form.password.data)
                message = u'Los datos de acceso son incorrectos.'
                if not user:
                    self.audit_push('Login (username not found): %s' % username)
                    raise ValueError(message)
                elif not auth:
                    self.audit_push('Login (password not match): %s' % username)
                    raise ValueError(message)
                sid = self.start_session(user)
                if sid:
                    user.set_last_login(data={
                        'set__sid': sid,
                        'set__remote_ip': self.remote_ip
                    })
                    self.log_push(
                        'Start session (sid): %s by (uid): %s' % (
                            sid, user.username
                        ), 'start_session'
                    )
                    return self.goto_next_or_root()
                else:
                    raise ValueError(message)
            except Exception as e:
                self.audit_push('Login (error): %s' % e.message)
                form._errors = {'errors': [e.message.encode('utf-8')]}
        self.render(form=form)


class SignOutHandler(BaseHandler):
    @perms_user.require()
    def get(self, *args, **kwargs):
        self.render('auth/signout.html')

    @perms_user.require()
    def post(self, *args, **kwargs):
        session = self.session.data
        self.destroy_session()
        self.log_push(
            'Close session (sid): %s by (uid): %s' % (
                session.get('sid'), session.get('username')
            ), 'start_session'
        )
        return self.redirect(self.get_login_url())


class RequestHandler(CommonBaseHandler):
    _form = RequestForm
    _template = 'auth/request.html'

    @verify_session_status
    def get(self, *args, **kwargs):
        self.render(thanks=False)

    @verify_session_status
    def post(self, *args, **kwargs):
        thanks = False
        form = self._form(self.request.arguments)
        if form.validate():
            try:
                message = u'El email no esta disponible, ya fue pre-registrado.'
                if User.objects(email=form.email.data).first():
                    self.audit_push('Register (user email exists): %s'
                                    % form.email.data)
                    raise ValueError(message)
                if PreRegister.objects(email=form.email.data).first():
                    self.audit_push('Register (pre-register email exists): %s'
                                    % form.email.data)
                    raise ValueError(message)
                try:
                    register = PreRegister()
                    register.company = form.company.data
                    register.position = form.position.data
                    register.provider = form.provider.data
                    register.first_name = form.first_name.data.strip()
                    register.last_name = form.last_name.data.strip()
                    register.email = form.email.data.strip()
                    register.phone_lada = form.phone_lada.data
                    register.phone_number = form.phone_number.data
                    register.enabled = True
                    register.available = True
                    register.policy = True
                    register.remote_ip = self.remote_ip
                    register.token = token(include_date=True)
                    register.activation_key = token_b64(include_date=True)
                    register.save()
                    self.audit_push(
                        'Register (new): %s, %s <%s>' % (
                            register.last_name,
                            register.first_name,
                            register.email
                        )
                    )
                except Exception:
                    raise ValueError(u'El pre-registro no pudo ser creado.')
                try:
                    # TODO: Migrate to Background Task.
                    send_mail(
                        emails.CONFIRMATION_SUBJECT,
                        emails.CONFIRMATION % {
                            'username': register.first_name.split(' ')[0],
                            'site_domain': self.settings.get('site_domain'),
                            'token': register.token,
                            'activation_key':
                            register.activation_key.replace('=', '%3D')
                        },
                        'Feedback by Figment <%s>' % self.settings.get('email'),
                        [register.email],
                        connection=self.application.email_client
                    )
                    self.audit_push(
                        'Register (send email): %s, %s <%s>' % (
                            register.last_name,
                            register.first_name,
                            register.email
                        )
                    )
                except Exception:
                    raise ValueError(u'El email de verificación de datos, '
                                     u'no pudo ser enviado.')
                thanks = True
            except Exception as e:
                self.audit_push('Register (error): %s' % e.message)
                form._errors = {'errors': [e.message.encode('utf-8')]}
        self.render(form=form, thanks=thanks)


class RequestVerifyHandler(CommonBaseHandler):
    _form = RecoveryForm
    _template = 'auth/thanks.html'

    @verify_session_status
    def get(self, *args, **kwargs):
        if not args or len(args) != 2:
            return self.goto_root()
        secure_token = args[0]
        secure_key = args[1]
        if not regex_activation_key.search(secure_token) or \
                not regex_activation_key_64.search(secure_key):
            self.audit_push('Register (verify key error): %s - %s' % (
                secure_token, secure_key
            ))
            return self.goto_root()
        try:
            register = PreRegister.objects(
                token=secure_token,
                activation_key=secure_key,
            ).first()
            self.audit_push('Register (verify user): %s' % register.email)
        except Exception:
            self.audit_push('Register (verify pre-register error): %s - %s' % (
                secure_token, secure_key
            ))
            return self.goto_root()
        if not register:
            self.audit_push('Register (verify user not found): %s - %s' % (
                secure_token, secure_key
            ))
            return self.goto_root()
        hash_str = '%s$%s' % (secure_token, secure_key)
        hash_str = base64.urlsafe_b64encode(hash_str)
        try:
            register.set_update({
                'activation_hash':
                SHA1PasswordHasher().make(hash_str)
            })
            self.audit_push('Register (verify user update): %s'
                            % register.email)
        except Exception:
            self.audit_push('Register (verify user not update): %s'
                            % register.email)
            return self.goto_root()
        try:
            # TODO: Migrate to Background Task.
            send_mail(
                emails.ACTIVATION_SUBJECT,
                emails.ACTIVATION % {
                    'site_domain': self.settings.get('site_domain'),
                    'company': register.company,
                    'first_name': register.first_name,
                    'last_name': register.last_name,
                    'email': register.email,
                    'phone_lada': register.phone_lada,
                    'phone_number': register.phone_number,
                    'created': register.created,
                    'token': hash_str.replace('=', '%3D'),
                    'oid': str(register.id),
                },
                'Feedback by Figment <%s>' % self.settings.get('email'),
                settings.EMAIL_VERIFICATION_LIST,
                connection=self.application.email_client
            )
            self.audit_push('Register (verify send mail): %s'
                            % register.email)
        except Exception:
            self.audit_push('Register (verify send mail error): %s'
                            % register.email)
            return self.goto_root()
        self.render(firstname=register.first_name.split(' ')[0])


class RequestVerifyAllowDenyHandler(CommonBaseHandler):
    _form = RequestForm
    _template = 'auth/allow_or_deny.html'

    def get(self, *args, **kwargs):
        if not args or len(args) != 3:
            return self.goto_root()
        try:
            action = args[0]
            if action not in ('allow', 'deny',):
                raise ValueError('Register (allow/deny action error): %s '
                                 % action)
            oid = args[1]
            if not regex_object_id.search(oid):
                raise ValueError('Register (allow/deny Object ID error): %s'
                                 % oid)
            secure_hash = args[2]
            if not regex_activation_key_64.search(secure_hash):
                raise ValueError('Register (allow/deny key error): %s'
                                 % secure_hash)
            register = \
                PreRegister.objects(id=ObjectId(oid), enabled=True).first()
            if not register:
                raise ValueError('Register (allow/deny user not found): %s'
                                 % oid)
            elif not register.token \
                    or not register.activation_key \
                    or not register.activation_hash:
                raise ValueError('Register (allow/deny user activated): %s'
                                 % oid)
            elif not SHA1PasswordHasher()\
                    .verify(secure_hash, register.activation_hash):
                raise ValueError('Register (allow/deny hash not match): %s'
                                 % oid)
            getattr(self, '_%s' % action, None)(data=register)
            self.audit_push('Register (%s) %s, %s <%s> by ip: %s' % (
                action, register.last_name, register.first_name,
                register.email, self.remote_ip
            ))
        except Exception as e:
            self.audit_push(e.message)
            return self.goto_root()

    def _allow(self, **kwargs):
        data = kwargs.get('data')
        try:
            user = User()
            user.company = data.company
            user.position = data.position
            user.provider = data.provider
            user.first_name = data.first_name
            user.last_name = data.last_name
            user.email = data.email
            user.phone_lada = data.phone_lada
            user.phone_number = data.phone_number
            user.policy = data.policy
            user.enabled = True
            user.available = True
            user.permissions = perms_user
            user.username = 'user_%s' % user_token(data.email, 6)
            password = token(8)
            user.password = password
            user.save()
            self._deny_helper(data=data)
        except Exception:
            raise ValueError('Register (allow/deny can\'t create user): %s'
                             % data.get('_id'))
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
            self.audit_push('Register (allow/deny send email): %s' % user.email)
            return self.render(data=user)
        except Exception:
            raise ValueError('Register (allow/deny send mail error): %s'
                             % user.email)

    def _deny(self, **kwargs):
        data = kwargs.get('data')
        self._deny_helper(data)
        return self.render(data=data)

    def _deny_helper(self, data):
        try:
            data.set_update({
                'enabled': False,
                'available': False,
                'token': '',
                'activation_key': '',
                'activation_hash': ''
            })
        except Exception:
            raise ValueError('Register (allow/deny can\'t create user): %s'
                             % data.get('_id'))


class RecoveryHandler(CommonBaseHandler):
    _form = RecoveryForm
    _template = 'auth/recovery.html'

    @verify_session_status
    def get(self, *args, **kwargs):
        self.render()

    @verify_session_status
    def post(self, *args, **kwargs):
        form = self._form(self.request.arguments)
        if form.validate():
            try:
                email = form.email.data
                user = User.objects(email=email, available=True).first()
                if not user:
                    self.audit_push('Email not found: %s' % email)
                    raise ValueError(u'Los datos son incorrectos.')
                try:
                    user.set_activation_key()
                    self.audit_push(
                        'Password recovery (start): %s (key): %s'
                        % (user.username, user.activation_key)
                    )
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
                    self.audit_push(
                        'Password recovery (send email): %s (key): %s'
                        % (user.username, user.activation_key)
                    )
                    return self.redirect('/auth/recovery/verify')
                except Exception:
                    user.set_enabled()
                    raise ValueError(u'Los pasos para la recuperación de su '
                                     u'contraseña, no han podido ser enviados.')
            except Exception as e:
                self.audit_push('Password recovery (error): %s' % e.message)
                form._errors = {'errors': [e.message.encode('utf-8')]}
        self.render(form=form)


class RecoveryVerifyHandler(CommonBaseHandler):
    _form = RecoveryVerifyForm
    _template = 'auth/verify.html'

    def activation_key_verify(self, key):
        message = u'La clave de verificación es incorrecta.'
        if not key or not regex_activation_key.search(key):
            self.audit_push('Password recovery (key undefined): %s' % key)
            raise ValueError(message)
        key = key.replace('/', '')
        user = User.objects(activation_key=key).first()
        if not user or not user.verify_activation_key(key):
            self.audit_push('Password recovery (user not found): %s' % key)
            raise ValueError(message)
        secure_key = token_b64(64, True)
        # TODO: Agregar a la base `secure_key` y comprobarlo posteriormente.
        self.set_secure_cookie(
            RECOVERY_ID, json_encode({
                'key': key,
                'secure_key': secure_key
            }), 1, max_age=60*10
        )
        self.audit_push('Password recovery (verify): %s' % user.username)
        return self.redirect('/auth/recovery/password/%s' % secure_key)

    @verify_session_status
    def get(self, *args, **kwargs):
        form = self._form()
        try:
            if args and args[0]:
                self.activation_key_verify(args[0])
                return
        except Exception as e:
            self.audit_push('Password recovery (verify error): %s' % e.message)
            form._errors = {'errors': [e.message.encode('utf-8')]}
        self.render(form=form)

    @verify_session_status
    def post(self, *args, **kwargs):
        form = self._form(self.request.arguments)
        if form.validate():
            try:
                self.activation_key_verify(form.activation_key.data)
                return
            except Exception as e:
                self.audit_push('Password recovery (verify error): %s'
                                % e.message)
                form._errors = {'errors': [e.message.encode('utf-8')]}
        self.render(form=form)


class RecoveryPasswordHandler(CommonBaseHandler):
    _form = RecoveryPasswordForm
    _template = 'auth/password.html'

    def verify_keys(self, secure_key):
        try:
            keys = json_decode(self.get_secure_cookie(RECOVERY_ID))
            key = keys.get('key')
            secure_key = secure_key.replace('/', '')
            user = User.objects(activation_key=key).first()
            if not keys or 'secure_key' not in keys or 'key' not in keys \
                    or not regex_activation_key.search(key) \
                    or not safe_str_cmp(keys.get('secure_key'), secure_key) \
                    or not user:
                self.audit_push('Password recovery (change error): %s'
                                % secure_key)
                raise ValueError('Validation Error')
            return user, key, secure_key
        except Exception as e:
            self.audit_push('Password recovery (change error): %s' % e.message)
            return self.redirect(self.get_login_url())

    @verify_session_status
    def get(self, *args, **kwargs):
        if args and args[0] and self.verify_keys(args[0]):
            self.render()

    @verify_session_status
    def post(self, *args, **kwargs):
        form = self._form(self.request.arguments)
        if form.validate():
            try:
                if args and args[0]:
                    user, key, secure_key = self.verify_keys(args[0])
                    user.set_activation_key_password(key, form.password.data)
                    self.clear_cookie(RECOVERY_ID)
                    self.audit_push(
                        'Password recovery (complete): %s' % user.username)
                return self.redirect(self.get_login_url())
            except Exception as e:
                self.audit_push(
                    'Password recovery (change error): %s' % e.message)
                form._errors = {'errors': [e.message.encode('utf-8')]}
        self.render(form=form)


handlers_list = [
    (r'/auth/signin', SignInHandler),
    (r'/auth/signout', SignOutHandler),
    (r'/auth/request', RequestHandler),
    (r'/auth/request/verify/([a-f0-9]{32})/([a-zA-Z0-9%=]+)',
     RequestVerifyHandler),
    (r'/auth/request/thanks', RequestHandler),
    (r'/auth/request/(allow|deny)/([a-z0-9]+)/([a-zA-Z0-9%=]+)',
     RequestVerifyAllowDenyHandler),
    (r'/auth/recovery', RecoveryHandler),
    (r'/auth/recovery/verify(/[a-f0-9]{32})?', RecoveryVerifyHandler),
    (r'/auth/recovery/password/([a-zA-Z0-9=]+)', RecoveryPasswordHandler)
]