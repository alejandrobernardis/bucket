#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 20/Mar/2014 14:14

from addicted.verify.core.utils import hack_mongo_accents
from addicted.verify.forms.services import SearchForm
from addicted.verify.handlers.base import BaseHandler
from addicted.verify.models.users import User, PreRegister
from addicted.verify.security.roles import perms_admin
from mongoengine import Q


class CommonBaseHandler(BaseHandler):
    _form = None
    _template = None

    def render(self, **kwargs):
        if not kwargs:
            kwargs = {}
        if self._form and 'form' not in kwargs:
            kwargs['form'] = self._form()
        super(CommonBaseHandler, self).render(self._template, **kwargs)


class AdminUsersHandler(CommonBaseHandler):
    _form = SearchForm
    _template = 'admin/users.html'

    @perms_admin.strict()
    def get(self, *args, **kwargs):
        users = []
        form = self._form()
        try:
            paginator = self.paginate(
                int(self.get_argument('page', 1)),
                total=User.objects.count() or 1
            )
            users = User.paginate(
                Q(username__nin=[
                    'sysadmin',
                    'administrator',
                    'administrador'
                ])&Q(available=True),
                paginator.page_number,
                order_by=['last_name', 'first_name']
            )
            if not len(users):
                form._errors = {'errors': [
                    'No existen usuarios disponibles.'
                ]}
        except Exception as e:
            self.audit_push('Search (users error): %s' % e.message)
            form._errors = {'errors': [e.message.encode('utf-8')]}
            paginator = self.paginate(1, total=1)
        self.render(form=form, users=users, paginator=paginator)

    @perms_admin.strict()
    def post(self, *args, **kwargs):
        users = []
        form = self._form(self.request.arguments)
        if form.validate():
            try:
                like = u'.*{}.*'.format(hack_mongo_accents(form.q.data))\
                                .encode('utf-8')
                users = self.mongo.users.aggregate([
                    {
                        '$project': {
                            'id': '$_id',
                            'full_name': {
                                '$concat': [
                                    '$first_name', ' ', '$last_name'
                                ]
                            },
                            'available': '$available',
                            'enabled': '$enabled',
                            'email': '$email',
                            'username': '$username',
                            'permissions': '$permissions',
                            'first_name': '$first_name',
                            'last_name': '$last_name',
                            'last_login': '$last_login',
                            'phone_lada': '$phone_lada',
                            'phone_number': '$phone_number',
                        }
                    }, {
                        '$match': {
                            '$and': [
                                {'username': {
                                    '$nin': [
                                        'sysadmin',
                                        'administrator',
                                        'administrador'
                                    ],
                                }},
                                {'available': True}
                            ],
                            '$or': [
                                {'full_name': {
                                    '$regex': like,
                                    '$options': 'i'
                                }},
                                {'first_name': {
                                    '$regex': like,
                                    '$options': 'i'
                                }},
                                {'last_name': {
                                    '$regex': like,
                                    '$options': 'i'
                                }},
                                {'username': {
                                    '$regex': like,
                                    '$options': 'i'
                                }},
                                {'email': {
                                    '$regex': like,
                                    '$options': 'i'
                                }}
                            ]
                        }
                    }, {
                        '$sort': {
                            'last_name': 1,
                            'first_name': 1
                        }
                    }, {
                        '$limit': 50
                    }
                ])['result']
                if not len(users):
                    form._errors = {'errors': [
                        u'No se encontraron resultados.'
                    ]}
                else:
                    self.audit_push('Search (users success): %s' % like)
            except Exception as e:
                self.audit_push('Search (users error): %s' % e.message)
                form._errors = {'errors': [e.message.encode('utf-8')]}
        self.render(
            form=form, users=users, paginator=self.paginate(1, total=1)
        )


class AdminRegisterHandler(CommonBaseHandler):
    _form = SearchForm
    _template = 'admin/register.html'

    @perms_admin.strict()
    def get(self, *args, **kwargs):
        users = []
        form = self._form()
        try:
            paginator = self.paginate(
                int(self.get_argument('page', 1)),
                total=PreRegister.objects.count() or 1
            )
            users = PreRegister.paginate_wll(
                paginator.page_number,
                order_by=['last_name', 'first_name']
            )
            if not len(users):
                form._errors = {'errors': [
                    'No existen registros disponibles.'
                ]}
        except Exception as e:
            self.audit_push('Search (register error): %s' % e.message)
            form._errors = {'errors': [e.message.encode('utf-8')]}
            paginator = self.paginate(1, total=1)
        self.render(form=form, users=users, paginator=paginator)

    @perms_admin.strict()
    def post(self, *args, **kwargs):
        users = []
        form = self._form(self.request.arguments)
        if form.validate():
            try:
                like = u'.*{}.*'.format(hack_mongo_accents(form.q.data))\
                                .encode('utf-8')
                users = self.mongo.preregister.aggregate([
                    {
                        '$project': {
                            'id': '$_id',
                            'full_name': {
                                '$concat': [
                                    '$first_name', ' ', '$last_name'
                                ]
                            },
                            'available': '$available',
                            'enabled': '$enabled',
                            'email': '$email',
                            'company': '$company',
                            'first_name': '$first_name',
                            'last_name': '$last_name',
                            'created': '$created',
                            'phone_lada': '$phone_lada',
                            'phone_number': '$phone_number',
                            'activation_hash': '$activation_hash'
                        }
                    }, {
                        '$match': {
                            '$and': [
                                {'enabled': True},
                                {'available': True}
                            ],
                            '$or': [
                                {'company': {
                                    '$regex': like,
                                    '$options': 'i'
                                }},
                                {'full_name': {
                                    '$regex': like,
                                    '$options': 'i'
                                }},
                                {'first_name': {
                                    '$regex': like,
                                    '$options': 'i'
                                }},
                                {'last_name': {
                                    '$regex': like,
                                    '$options': 'i'
                                }},
                                {'email': {
                                    '$regex': like,
                                    '$options': 'i'
                                }}
                            ]
                        }
                    }, {
                        '$sort': {
                            'company': 1,
                            'last_name': 1,
                            'first_name': 1
                        }
                    }, {
                        '$limit': 50
                    }
                ])['result']
                if not len(users):
                    form._errors = {'errors': [
                        u'No se encontraron resultados.'
                    ]}
                else:
                    self.audit_push('Search (register success): %s' % like)
            except Exception as e:
                self.audit_push('Search (register error): %s' % e.message)
                form._errors = {'errors': [e.message.encode('utf-8')]}
        self.render(
            form=form, users=users, paginator=self.paginate(1, total=1)
        )


handlers_list = [
    (r'/a/users', AdminUsersHandler),
    (r'/a/register', AdminRegisterHandler),

]