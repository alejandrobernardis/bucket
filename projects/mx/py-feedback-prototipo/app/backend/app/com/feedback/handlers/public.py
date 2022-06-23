#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 24/May/2014 02:38

import json
import base64
import datetime

import emails
from com.feedback.core.regex import regex_activation_key_64
from com.feedback.core.utils import str_complex_type, safe_str_cmp, \
    SuperObject, mexico_time_zone, secret_key
from com.feedback.forms.common import EvaluationForm
from com.feedback.handlers.base import CommonBaseHandler, BaseHandler
from com.feedback.models.evaluations import Evaluation, EvaluationPending
from com.feedback.models.users import User
from com.feedback.security.password import SHA256PasswordHasher
from com.feedback.ui_modules.utils import helper_rate
from mongoengine import Q
from tasks import push__notifications, push__delete_obsolete_data


SESSION_ID = 'evaid'


class PublicEvaluationHandlers(CommonBaseHandler):
    _form = EvaluationForm
    _template = 'public/evaluation.html'

    def _get_cookie_object(self):
        cookie = self.get_secure_cookie(SESSION_ID)
        if not cookie:
            return False
        return SuperObject(**json.loads(cookie))

    def get(self, *args, **kwargs):
        username = str(args[0]).strip()
        activation_key = str(args[1]).strip()
        try:
            cookie = self._get_cookie_object()
            if not cookie:
                raise ValueError('Cookie not found.')
            if not safe_str_cmp(activation_key, cookie.activation_key):
                raise ValueError('Activation key does not match.')
            elif not safe_str_cmp(username, cookie.username):
                raise ValueError('Username does not match.')
            evaluation = EvaluationPending.get_by__first(
                Q(activation_key=activation_key)
                & Q(username=username)
                & Q(private_key=cookie.private_key)
            )
            if not evaluation:
                raise ValueError('Evaluation not available.')
            user = User.get_by_username(username)
            if not user:
                raise ValueError('User not available.')
            cookie.first_name = user.first_name.split(' ')[0]
            cookie.tz_mexico = mexico_time_zone(evaluation.public_key_expires)
            self.set_secure_cookie(SESSION_ID, json.dumps(
                cookie.todict(), default=str_complex_type
            ), 1, max_age=600)
            self.audit_push('Evaluation (form view success): %s => %s'
                            % (username, activation_key), user=username)
            return self.render(thanks=False, cookie=cookie)
        except Exception as e:
            self.audit_push('Evaluation (form view error): %s' % e.message,
                            user=username)
            return self.goto_root()

    def post(self, *args, **kwargs):
        thanks = False
        form = self._form(self.request.arguments)
        if form.validate():
            username = str(args[0]).strip()
            activation_key = str(args[1]).strip()
            try:
                cookie = self._get_cookie_object()
                if not cookie:
                    raise ValueError(u'La sesión ha caducado.')
                user = User.get_by_username(username)
                if not user:
                    raise ValueError(u'Usuario no disponible.')
                evaluation = EvaluationPending.get_by__first(
                    Q(activation_key=activation_key)
                    & Q(username=username)
                    & Q(private_key=cookie.private_key)
                )
                if not evaluation:
                    raise ValueError(u'La evaluación no esta disponible.')
                ev = Evaluation()
                ev.client = username
                ev.reference = user
                ev.description = form.comments.data
                ev.rate = form.rate.data
                ev.policy = form.policy.data == 1
                ev.provider = user.provider
                ev.activation_key = activation_key
                ev.enabled = True
                ev.available = True
                ev.save()
                push__notifications.delay(
                    user.executives,
                    emails.NOTIFICATION_SUBJECT % helper_rate(ev.rate),
                    emails.NOTIFICATION % {
                        'client': '%s %s' % (user.first_name, user.last_name),
                        'rate': helper_rate(ev.rate),
                        'comments': ev.description,
                        'activation_key': ev.activation_key,
                        'site_domain': self.settings.get('site_domain')
                    }
                )
                self.audit_push('Evaluation (form complete success): %s => %s'
                                % (username, activation_key), user=username)
                if not evaluation.set_logic_low():
                    self.audit_push('Evaluation (form complete error): '
                                    'can\'t delete %s => %s'
                                    % (username, activation_key), user=username)
                push__delete_obsolete_data.delay(**{'_id': evaluation.id})
                self.clear_cookie(SESSION_ID)
                thanks = True
            except Exception as e:
                self.audit_push('Evaluation (form complete error): %s'
                                % e.message, user=username)
                form._errors = {'errors': [e.message.encode('utf-8')]}
        self.render(form=form, thanks=thanks, cookie=self._get_cookie_object())


class PublicEvaluationVerifyHandlers(BaseHandler):
    def get(self, *args, **kwargs):
        public_key = str(args[0]).strip()
        try:
            if not regex_activation_key_64.search(public_key):
                raise ValueError('Public key is incorrect.')
            public_key = base64.b64decode(public_key)
            verify = EvaluationPending.get_by__first(Q(public_key=public_key))
            if not verify \
                    or verify.public_key_expires < datetime.datetime.utcnow():
                raise ValueError('Public key does not exist or expired.')
            public_key = SHA256PasswordHasher().verify(
                verify.token, '%s%s' % (
                    verify.public_key_method,
                    base64.decodestring(public_key.replace('|', '\n'))
                )
            )
            if not public_key:
                raise ValueError('Public key is invalid.')
            verify.set_update({'private_key': secret_key(16)})
            verify.token = ''
            self.clear_cookie(SESSION_ID)
            self.set_secure_cookie(SESSION_ID, json.dumps({
                'username': verify.username,
                'activation_key': verify.activation_key,
                'private_key': verify.private_key
            }, default=str_complex_type), 1, max_age=600)
            self.audit_push(
                'Evaluation (verify success): %s => %s'
                % (verify.username, public_key), user=verify.username
            )
            return self.redirect(
                '/p/evaluation/view/{}/{}'.format(
                    verify.username, verify.activation_key
                )
            )
        except Exception as e:
            self.audit_push('Evaluation (verify error): %s => %s'
                            % (e.message, public_key))
            return self.goto_root()


class LegalPrivacy(CommonBaseHandler):
    _form = EvaluationForm
    _template = 'public/privacy.html'

    def get(self, *args, **kwargs):
        self.render()


class ContactUsPrivacy(CommonBaseHandler):
    _form = EvaluationForm
    _template = 'public/contact-us.html'

    def get(self, *args, **kwargs):
        self.render()


handlers_list = [
    (r'/p/evaluation/view/([a-zA-Z0-9_\.]+)/([a-zA-Z0-9%=]+)',
     PublicEvaluationHandlers),
    (r'/p/evaluation/verify/([a-zA-Z0-9%=]+)',
     PublicEvaluationVerifyHandlers),
    (r'/legal/privacy', LegalPrivacy),
    (r'/contact-us', ContactUsPrivacy)
]