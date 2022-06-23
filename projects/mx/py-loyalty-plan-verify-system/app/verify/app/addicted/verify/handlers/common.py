#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 27/Dec/2013 02:06

from addicted.verify.forms.auth import ProfileForm, RecoveryPasswordForm, \
    ChangePasswordForm
from addicted.verify.forms.common import SearchForm
from addicted.verify.handlers.base import BaseHandler
from addicted.verify.models.concierge import ConciergeUser, ConciergeContact, \
    ConciergeCard
from addicted.verify.models.users import User
from addicted.verify.security.roles import perms_user
from sqlalchemy import and_, or_
from sqlalchemy.sql.functions import concat


class CommonBaseHandler(BaseHandler):
    _form = None
    _template = None

    def render(self, **kwargs):
        if not kwargs:
            kwargs = {}
        if 'form' not in kwargs:
            kwargs['form'] = self._form()
        super(CommonBaseHandler, self).render(self._template, **kwargs)


class MainHandler(CommonBaseHandler):
    _form = SearchForm
    _template = 'common/main.html'

    def sql_filter(self, value, criteria=None):
        filters = []
        filter_map = {
            'first_name': ConciergeUser.firstname,
            'last_name': ConciergeUser.lastname,
            'email': ConciergeUser.email,
            'phone': (
                ConciergeContact.telephone,
                ConciergeContact.mobile
            ),
            'address': ConciergeContact.street,
            'card': ConciergeCard.number
        }
        if not criteria or criteria == 'all':
            criteria = filter_map.keys()
            filters.append(
                concat(
                    ConciergeUser.firstname, ' ', ConciergeUser.lastname
                ).like(value)
            )
        elif not isinstance(criteria, (tuple, list,)):
            criteria = [criteria]
        for key in criteria:
            if key in filter_map:
                key_value = filter_map[key]
                if isinstance(key_value, (tuple, list,)):
                    for item in key_value:
                        filters.append(item.like(value))
                else:
                    filters.append(key_value.like(value))
        return filters

    def sql_query_maker(self, value, criteria=None, limit=100, skip=0):
        try:
            return self.sql_db.query(
                ConciergeCard.number,
                ConciergeUser.firstname,
                ConciergeUser.lastname,
                ConciergeUser.email,
                ConciergeContact.birthday,
                ConciergeContact.telephone,
                ConciergeContact.mobile,
                ConciergeContact.street,
                ConciergeContact.colonia,
                ConciergeContact.municipio,
                ConciergeContact.estado
            ).select_from(
                ConciergeUser
            ).join(
                ConciergeContact
            ).join(
                ConciergeCard
            ).filter(
                and_(
                    ConciergeUser.active == 1,
                    ConciergeUser.access_level == 4,
                    ConciergeCard.active == 1,
                    or_(*self.sql_filter(value, criteria))
                )
            ).limit(limit).offset(skip)
        except Exception:
            return None

    @perms_user.require()
    def get(self, *args, **kwargs):
        self.render(recordset=[])

    @perms_user.require()
    def post(self, *args, **kwargs):
        recordset = []
        form = self._form(self.request.arguments)
        if form.validate():
            try:
                recordset_result = self.sql_query_maker(
                    u'%{}%'.format(form.q.data),
                    form.filter.data
                )
                recordset = recordset_result.all()
                if not len(recordset):
                    form._errors = {'errors': [
                        u'No se encontraron resultados.'
                    ]}
            except Exception as e:
                self.audit_push('Search (error): %s' % e.message)
                form._errors = {'errors': [e.message.encode('utf-8')]}
        self.audit_push('Q(%s : %s)' % (form.q.data, form.filter.data))
        self.render(form=form, recordset=recordset)


class ProfileHandler(CommonBaseHandler):
    _form = ProfileForm
    _template = 'common/profile.html'

    @perms_user.require()
    def get(self, *args, **kwargs):
        self.render()


class ProfileUpdateHandler(CommonBaseHandler):
    _form = ProfileForm
    _template = 'common/profile.html'

    @perms_user.require()
    def get(self, *args, **kwargs):
        self.render()

    @perms_user.require()
    def post(self, *args, **kwargs):
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
                        'first_name': form.first_name.data,
                        'last_name': form.last_name.data,
                        'phone_lada': form.phone_lada.data,
                        'phone_number': form.phone_number.data
                    }
                    user.set_update(update)
                    self.session.update(**update)
                    self.audit_push(
                        'Update profile (success): %s' % username)
                    return self.redirect('/profile')
                except Exception:
                    self.audit_push(
                        'Update profile (error): %s' % username)
                    raise ValueError(u'Los datos no pudieron ser actulizados.')
            except Exception as e:
                self.audit_push('Update profile (error): %s' % e.message)
                form._errors = {'errors': [e.message.encode('utf-8')]}
        self.render(form=form)


class ProfilePasswordHandler(CommonBaseHandler):
    _form = ChangePasswordForm
    _template = 'common/profile.html'

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
                    return self.redirect('/profile')
                except Exception:
                    self.audit_push(
                        'Update password (error): %s' % username)
                    raise ValueError(u'Los datos no pudieron ser actulizados.')
            except Exception as e:
                self.audit_push('Update password (error): %s' % e.message)
                form._errors = {'errors': [e.message.encode('utf-8')]}
        self.render(form=form)


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


handlers_list = [
    (r'/', MainHandler),
    (r'/profile', ProfileHandler),
    (r'/profile/update', ProfileUpdateHandler),
    (r'/profile/password', ProfilePasswordHandler),
    (r'/profile/terminate', ProfileTerminateHandler),

]