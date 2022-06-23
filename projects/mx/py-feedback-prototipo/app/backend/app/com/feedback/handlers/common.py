#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 27/Dec/2013 02:06

import emails
from com.feedback.core.utils import token_b64
from com.feedback.forms.common import ProfileForm, RecoveryPasswordForm, \
    ChangePasswordForm, EvaluationForm
from com.feedback.forms.services import SearchForm
from com.feedback.handlers.base import CommonBaseHandler
from com.feedback.ui_modules.utils import helper_rate
from com.feedback.models.users import User
from com.feedback.models.evaluations import Evaluation
from com.feedback.security.roles import perms_user
from mongoengine import Q
from tasks import push__notifications


class MainHandler(CommonBaseHandler):
    _form = None
    _template = 'common/main.html'

    @perms_user.require()
    def get(self, *args, **kwargs):
        if self.identity.is_admin:
            return self.redirect('/a/evaluations')
        else:
            return self.redirect('/evaluations')


class ProfileHandler(CommonBaseHandler):
    _form = ProfileForm
    _template = 'common/profile.html'

    @perms_user.require()
    def get(self, *args, **kwargs):
        self.render(thanks=self.get_argument('t', False))


class ProfileUpdateHandler(CommonBaseHandler):
    _form = ProfileForm
    _template = 'common/profile.html'

    @perms_user.require()
    def get(self, *args, **kwargs):
        self.render(thanks=False)

    @perms_user.require()
    def post(self, *args, **kwargs):
        thanks = False
        form = self._form(self.request.arguments)
        if form.validate():
            try:
                username = self.session.get('username')
                user = User.get_by_username(username)
                if not user:
                    self.audit_push(
                        'Update profile (username not found): %s' % username)
                    raise ValueError(u'El usuario no existe: %s ' % username)
                try:
                    update = {
                        'company': form.company.data,
                        'position': form.position.data,
                        'first_name': form.first_name.data,
                        'last_name': form.last_name.data,
                        'phone_lada': form.phone_lada.data,
                        'phone_number': form.phone_number.data,
                        'dispatch': form.dispatch.data
                    }
                    user.set_update(update)
                    self.session.update(**update)
                    self.audit_push(
                        'Update profile (success): %s' % username)
                    return self.redirect('/profile?t=1')
                except Exception:
                    self.audit_push(
                        'Update profile (error): %s' % username)
                    raise ValueError(u'Los datos no pudieron ser actulizados.')
            except Exception as e:
                self.audit_push('Update profile (error): %s' % e.message)
                form._errors = {'errors': [e.message.encode('utf-8')]}
        self.render(form=form, thanks=thanks)


class ProfilePasswordHandler(CommonBaseHandler):
    _form = ChangePasswordForm
    _template = 'common/profile.html'

    @perms_user.require()
    def get(self, *args, **kwargs):
        self.render(thanks=False)

    @perms_user.require()
    def post(self, *args, **kwargs):
        thanks = False
        form = self._form(self.request.arguments)
        if form.validate():
            try:
                username = self.session.get('username')
                user, auth = User.auth_login(username, form.password.data)
                if not user:
                    self.audit_push(
                        'Update password (username not found): %s' % username)
                    raise ValueError(u'El usuario no existe: %s ' % username)
                elif not auth:
                    self.audit_push(
                        'Update password (wrong password): %s' % username)
                    raise ValueError(u'La contraseña actual no es correcta')
                try:
                    user.set_password(form.password_new.data)
                    self.audit_push(
                        'Update password (success): %s' % username)
                    return self.redirect('/profile?t=1')
                except Exception:
                    self.audit_push(
                        'Update password (error): %s' % username)
                    raise ValueError(u'Los datos no pudieron ser actulizados.')
            except Exception as e:
                self.audit_push('Update password (error): %s' % e.message)
                form._errors = {'errors': [e.message.encode('utf-8')]}
        self.render(form=form, thanks=thanks)


class ProfileTerminateHandler(CommonBaseHandler):
    _form = RecoveryPasswordForm
    _template = 'common/terminate.html'

    @perms_user.require()
    def get(self, *args, **kwargs):
        self.render()

    @perms_user.require()
    def post(self, *args, **kwargs):
        form = self._form(self.request.arguments)
        if form.validate():
            try:
                username = self.session.get('username')
                user, auth = User.auth_login(username, form.password.data)
                if user:
                    if not auth:
                        self.audit_push(
                            'Terminate account (wrong password): %s' % username)
                        raise ValueError(u'La contraseña no es correcta.')
                    else:
                        user.set_logic_low()
                        self.audit_push(
                            'Terminate account (success): %s' % username)
                else:
                    self.audit_push(
                        'Terminate account (username not found): %s' % username)
                self.destroy_session()
                return self.goto_root()
            except Exception as e:
                self.audit_push('Terminate account (error): %s' % e.message)
                form._errors = {'errors': [e.message.encode('utf-8')]}
        self.render(form=form)


class EvaluationsHandler(CommonBaseHandler):
    _form = SearchForm
    _template = 'common/evaluations.html'

    @perms_user.strict()
    def get(self, *args, **kwargs):
        evaluations = []
        form = self._form()
        try:
            username = self.session.get('username')
            client = Q(client=username)
            paginator = self.paginate(
                int(self.get_argument('page', 1)),
                total=Evaluation.objects(client).count() or 1
            )
            evaluations = Evaluation.paginate_wll(
                client, paginator.page_number, order_by=['-created']
            )
            if not len(evaluations):
                form._errors = {'errors': [
                    'No existen comentarios disponibles.'
                ]}
        except Exception as e:
            self.audit_push('Evaluations (error): %s' % e.message)
            form._errors = {'errors': [e.message.encode('utf-8')]}
            paginator = self.paginate(1, total=1)
        self.render(form=form, evaluations=evaluations, paginator=paginator)


class EvaluationsNewHandler(CommonBaseHandler):
    _form = EvaluationForm
    _template = 'common/evaluations/new.html'

    @perms_user.require()
    def get(self, *args, **kwargs):
        self.render(thanks=False)

    @perms_user.require()
    def post(self, *args, **kwargs):
        thanks = False
        form = self._form(self.request.arguments)
        if form.validate():
            try:
                username = self.session.get('username')
                user = User.get_by_username(username)
                if not user:
                    self.audit_push('Evaluation (error): %s => %s'
                                    % username, form.rate.data)
                    raise ValueError(u'El usuario no existe: %s ' % username)
                evaluation = Evaluation()
                evaluation.client = user.username
                evaluation.reference = user
                evaluation.description = form.comments.data
                evaluation.rate = form.rate.data
                evaluation.policy = form.policy.data == 1
                evaluation.provider = user.provider
                evaluation.activation_key = token_b64(include_date=True)
                evaluation.enabled = True
                evaluation.available = True
                evaluation.save()
                push__notifications.delay(
                    user.executives,
                    emails.NOTIFICATION_SUBJECT % helper_rate(evaluation.rate),
                    emails.NOTIFICATION % {
                        'client': '%s %s' % (user.first_name, user.last_name),
                        'rate': helper_rate(evaluation.rate),
                        'comments': evaluation.description,
                        'activation_key': evaluation.activation_key,
                        'site_domain': self.settings.get('site_domain')
                    }
                )
                thanks = True
                form = self._form()
            except Exception as e:
                self.audit_push('Update password (error): %s' % e.message)
                form._errors = {'errors': [e.message.encode('utf-8')]}
        self.render(form=form, thanks=thanks)


handlers_list = [
    (r'/', MainHandler),
    (r'/profile', ProfileHandler),
    (r'/profile/update', ProfileUpdateHandler),
    (r'/profile/password', ProfilePasswordHandler),
    (r'/profile/terminate', ProfileTerminateHandler),
    (r'/evaluations', EvaluationsHandler),
    (r'/evaluations/new', EvaluationsNewHandler),
    (r'/evaluations/new/([a-zA-Z0-9%=]+)', EvaluationsNewHandler)
]