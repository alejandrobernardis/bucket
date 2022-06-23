#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 20/Mar/2014 14:14

import re
import emails
import datetime
import json
from com.feedback.core.exceptions import FormError
from com.feedback.core.regex import regex_only_username
from com.feedback.core.utils import hack_mongo_accents, token, user_token, \
    activation_key, str_complex_type
from com.feedback.forms.common import NewUserForm
from com.feedback.forms.services import SearchForm
from com.feedback.handlers.base import CommonBaseHandler, BaseHandler
from com.feedback.models.evaluations import Evaluation
from com.feedback.models.users import User, PreRegister
from com.feedback.security.roles import perms_admin, perms_user, role_admin, \
    role_user
from mongoengine import Q
from tornadomail import send_mail


class AdminUsersHandler(CommonBaseHandler):
    _form = SearchForm
    _template = 'admin/users.html'

    def query_maker(self, like, paginator=None):
        query = ({
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
                'company': '$company',
                'position': '$position',
                'provider': '$provider',
                'executives': '$executives',
                'dispatch': '$dispatch',
                'remote_ip': '$remote_ip',
                'sid': '$sid'
            }
        }, {
            '$match': {
                '$and': [
                    {'username': {
                        '$nin': ['sysadmin', 'administrator', 'administrador'],
                    }},
                    {'available': True}
                ],
                '$or': [
                    {'full_name': {'$regex': like, '$options': 'i'}},
                    {'first_name': {'$regex': like, '$options': 'i'}},
                    {'last_name': {'$regex': like, '$options': 'i'}},
                    {'username': {'$regex': like, '$options': 'i'}},
                    {'email': {'$regex': like, '$options': 'i'}},
                    {'company': {'$regex': like, '$options': 'i'}},
                    {'position': {'$regex': like, '$options': 'i'}}
                ]
            }
        }, {'$sort': {'first_name': 1, 'last_name': 1, 'company': 1}})
        query_list = list(query)
        if paginator:
            query_list.append({
                '$skip': paginator.page_size * (paginator.page_number - 1)
            })
            query_list.append({'$limit': paginator.page_size})
        else:
            query_list.append({'$group': {'_id': None, 'total': {'$sum': 1}}})
        return query_list

    @perms_admin.strict()
    def get(self, *args, **kwargs):
        # TODO: NO APTO PARA VOLUMEN Y CONCURRENCIA.-
        form = self._form(self.request.arguments)
        users = []
        paginator = self.paginate(1, total=1)
        like = 'all'
        try:
            page = int(self.get_argument('page', 1))
            if form.validate():
                like = u'.*{}.*'.format(hack_mongo_accents(form.q.data))\
                                .encode('utf-8')
                query_count = self.query_maker(like)
                try:
                    total = self.mongo.users.aggregate(
                        query_count
                    )['result'][0].get('total')
                    if total > 0:
                        paginator = self.paginate(page, total=total)
                        query_list = self.query_maker(like, paginator)
                        users = self.mongo.users.aggregate(query_list)['result']
                except:
                    pass
            else:
                form._errors = []
                paginator = self.paginate(
                    page, total=User.objects(Q(available=True)).count() or 1
                )
                users = User.paginate(
                    Q(username__nin=[
                        'sysadmin', 'administrator', 'administrador'
                    ]) & Q(available=True),
                    paginator.page_number,
                    order_by=['first_name', 'last_name'],
                ).exclude('password')
            if not len(users):
                form._errors = {'errors': [u'No se encontraron resultados.']}
            else:
                self.audit_push('View / Search users (success): %s' % like)
        except Exception as e:
            self.audit_push('View / Search users (error): %s' % e.message)
            form._errors = {'errors': [e.message.encode('utf-8')]}
        self.render(form=form, users=users, paginator=paginator)


class AdminUsersNewHandler(CommonBaseHandler):
    _form = NewUserForm
    _template = 'admin/users/new.html'

    def get_executives_list(self):
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
        return [item for item in executives]

    def verify_username(self, form, username=None):
        # TODO: OJO!, ES UNA FUNCION RECURSIVA.-
        last_name = form.last_name.data.split(' ')[0]
        if not username:
            first_name = form.first_name.data.split(' ')[0]
            username = '%s.%s' % (last_name, first_name)
        response = re.sub(r'[^A-Za-z0-9\.]+', '', username)
        if not regex_only_username.search(response) or \
                User.objects(username=re.compile(response, re.I)).first():
            username = '%s.%s' % (last_name, user_token(form.email.data, 6))
            return self.verify_username(form, username[:64])
        return response.lower()

    @perms_admin.strict()
    def get(self, *args, **kwargs):
        form = self._form()
        try:
            executives = self.get_executives_list()
            self.audit_push('Executives list (error): %s' % len(executives))
        except Exception as e:
            executives = None
            self.audit_push('Executives list (error): %s' % e.message)
            form._errors = {'errors': [e.message.encode('utf-8')]}
        self.render(form=form, executives=executives, thanks=False)

    @perms_admin.strict()
    def post(self, *args, **kwargs):
        thanks = False
        form = self._form(self.request.arguments)
        if form.validate():
            try:
                if User.objects(email=form.email.data).first():
                    raise ValueError('El email ya fue utilizado.')
                user = User()
                user.company = form.company.data
                user.position = form.position.data
                user.provider = form.provider.data
                user.first_name = form.first_name.data
                user.last_name = form.last_name.data
                user.email = form.email.data
                user.phone_lada = form.phone_lada.data
                user.phone_number = form.phone_number.data
                user.policy = form.policy.data == 1
                user.enabled = False
                user.available = True
                level = form.permissions.data.lower()
                if level == role_admin.key:
                    perms = perms_admin
                    username = self.verify_username(form)
                elif level == role_user.key:
                    perms = perms_user
                    username = 'user_%s' % user_token(form.email.data, 6)
                else:
                    raise ValueError(
                        'El nivel "%s", no se puede asignar'
                        % form.permissions.data
                    )
                user.permissions = perms
                user.username = username
                user.executives = form.executives.data
                user.password = token(8)
                user.activation_key = activation_key(user.username, user.email)
                user.activation_key_expire = \
                    datetime.datetime.utcnow() + datetime.timedelta(days=365)
                user.save()
                send_mail(
                    emails.RECOVERY_PASSWORD_NEW_SUBJECT,
                    emails.RECOVERY_PASSWORD_NEW % {
                        'site_domain': self.settings.get('site_domain'),
                        'first_name': user.first_name.split(' ')[0],
                        'username': user.username,
                        'email': user.email,
                        'activation_key': user.activation_key,
                    },
                    'Feedback by Figment <%s>' % self.settings.get('email'),
                    [user.email],
                    connection=self.application.email_client
                )
                form = self._form()
                thanks = True
                self.audit_push('Create user (success): %s' % form.email.data)
            except Exception as e:
                self.audit_push('Create user (error): %s' % e.message)
                form._errors = {'errors': [e.message.encode('utf-8')]}
        try:
            executives = self.get_executives_list()
        except:
            executives = None
        self.render(form=form, executives=executives, thanks=thanks)


class AdminRegisterHandler(CommonBaseHandler):
    _form = SearchForm
    _template = 'admin/register.html'

    def query_maker(self, like, paginator=None):
        query = ({
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
                'first_name': '$first_name',
                'last_name': '$last_name',
                'phone_lada': '$phone_lada',
                'phone_number': '$phone_number',
                'company': '$company',
                'position': '$position',
                'provider': '$provider',
                'remote_ip': '$remote_ip',
                'activation_hash': '$activation_hash',
                'created': '$created'
            }
        }, {
            '$match': {
                '$and': [
                    {'enabled': True, 'available': True}
                ],
                '$or': [
                    {'full_name': {'$regex': like, '$options': 'i'}},
                    {'first_name': {'$regex': like, '$options': 'i'}},
                    {'last_name': {'$regex': like, '$options': 'i'}},
                    {'email': {'$regex': like, '$options': 'i'}},
                    {'company': {'$regex': like, '$options': 'i'}},
                    {'position': {'$regex': like, '$options': 'i'}}
                ]
            }
        }, {
            '$sort': {
                'created': 1,
                'first_name': 1,
                'last_name': 1,
                'company': 1
            }
        })
        query_list = list(query)
        if paginator:
            query_list.append({
                '$skip': paginator.page_size * (paginator.page_number - 1)
            })
            query_list.append({'$limit': paginator.page_size})
        else:
            query_list.append({'$group': {'_id': None, 'total': {'$sum': 1}}})
        return query_list

    @perms_admin.strict()
    def get(self, *args, **kwargs):
        # TODO: NO APTO PARA VOLUMEN Y CONCURRENCIA.-
        form = self._form(self.request.arguments)
        users = []
        paginator = self.paginate(1, total=1)
        like = 'all'
        try:
            page = int(self.get_argument('page', 1))
            if form.validate():
                like = u'.*{}.*'.format(hack_mongo_accents(form.q.data))\
                                .encode('utf-8')
                query_count = self.query_maker(like)
                try:
                    total = self.mongo.preregister.aggregate(
                        query_count
                    )['result'][0].get('total')
                    if total > 0:
                        paginator = self.paginate(page, total=total)
                        query_list = self.query_maker(like, paginator)
                        users = self.mongo.preregister.aggregate(
                            query_list
                        )['result']
                except:
                    pass
            else:
                form._errors = []
                paginator = self.paginate(
                    page, total=PreRegister.objects(
                        Q(enabled=True) & Q(available=True)
                    ).count() or 1
                )
                users = PreRegister.paginate_wll(
                    None,
                    paginator.page_number,
                    order_by=['created', 'first_name', 'last_name'],
                )
            if not len(users):
                form._errors = {'errors': [u'No se encontraron resultados.']}
            else:
                self.audit_push('View / Search register (success): %s' % like)
        except Exception as e:
            self.audit_push('View / Search register (error): %s' % e.message)
            form._errors = {'errors': [e.message.encode('utf-8')]}
        self.render(form=form, users=users, paginator=paginator)


class AdminEvaluationsHandler(CommonBaseHandler):
    _form = SearchForm
    _template = 'admin/evaluations.html'

    def query_maker(self, form):
        # TODO: DEFINIR UN ESQUEMA MAS EFICIENTE.-
        q = form.q.data.lower()
        try:
            if q not in ('pendientes', 'todo'):
                raise
            query = Q(answers=[]) | Q(answers=None)
        except:
            try:
                status = {
                    'activo': True,
                    'inactivo': False
                }[q]
                query = Q(enabled=status)
            except:
                try:
                    provider = {
                        'todos': 1,
                        'figment': 2,
                        'kinetiq': 3
                    }[q]
                    query = Q(provider=provider)
                except:
                    try:
                        rate = {
                            'muy mala': 1,
                            'mala': 2,
                            'regular': 3,
                            'bien': 4,
                            'muy bien': 5,
                        }[q]
                        query = Q(rate=rate)
                    except:
                        try:
                            mode = {
                                'email': 1,
                                'phone': 2,
                                'telefono': 2,
                                u'teléfono': 2,
                            }[q]
                            query = Q(answers__mode=mode)
                        except:
                            like = ur'.*{}.*'.format(hack_mongo_accents(q))\
                                             .encode('utf-8')
                            like = re.compile(like, re.I)
                            query = \
                                Q(client=like) \
                                | Q(answers__username=like) \
                                | Q(activation_key=like)

        return query & Q(available=True)

    @perms_admin.strict()
    def get(self, *args, **kwargs):
        # TODO: NO APTO PARA VOLUMEN Y CONCURRENCIA.-
        evaluations = []
        form = self._form(self.request.arguments)
        paginator = self.paginate(1, total=1)
        try:
            query = Q(available=True)
            if self.get_argument('q', False):
                if not form.validate():
                    raise FormError()
                query = self.query_maker(form)
            paginator = self.paginate(
                int(self.get_argument('page', 1)),
                total=Evaluation.objects(query).count() or 1
            )
            evaluations = Evaluation.paginate(
                query, paginator.page_number, order_by=['-created', 'rate'],
            )
            if not len(evaluations):
                raise ValueError(u'No se encontraron resultados.')
            self.audit_push('Search evaluations (success): %s' % form.q.data)
        except FormError:
            pass
        except Exception as e:
            self.audit_push('Search evaluations (error): %s' % e.message)
            form._errors = {'errors': [e.message.encode('utf-8')]}
        self.render(form=form, evaluations=evaluations, paginator=paginator)


# TODO: buscar un esquema de cache para optimizar la búsqueda de usuarios.
class AdminUsersAutocompleteHandler(BaseHandler):
    def query_maker(self, like, paginator=None):
        query = ({
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
                'first_name': '$first_name',
                'last_name': '$last_name',
                'company': '$company'
            }
        }, {
            '$match': {
                '$and': [
                    {'username': {
                        '$nin': ['sysadmin', 'administrator', 'administrador'],
                    }},
                    {'available': True}
                ],
                '$or': [
                    {'full_name': {'$regex': like, '$options': 'i'}},
                    {'first_name': {'$regex': like, '$options': 'i'}},
                    {'last_name': {'$regex': like, '$options': 'i'}}
                    # {'username': {'$regex': like, '$options': 'i'}},
                    # {'email': {'$regex': like, '$options': 'i'}}
                ]
            }
        }, {
            '$sort': {
                'first_name': 1, 
                'last_name': 1
            }
        }, {
            '$limit': 100
        })
        return list(query)

    @perms_admin.strict()
    def get(self, *args, **kwargs):
        form = SearchForm(self.request.arguments)
        users = []
        try:
            if form.validate():
                like = u'.*{}.*'.format(hack_mongo_accents(form.q.data))\
                                .encode('utf-8')
                query_list = self.query_maker(like)
                users = self.mongo.users.aggregate(query_list)['result']
            if len(users):
                self.audit_push(
                    'View / Autocomplete users (success): %s' % like)
        except Exception as e:
            self.audit_push(
                'View / Autocomplete users (error): %s' % e.message)
        self.finish(json.dumps(users, default=str_complex_type))


handlers_list = [
    (r'/a/users', AdminUsersHandler),
    (r'/a/users/new', AdminUsersNewHandler),
    (r'/a/users/autocomplete', AdminUsersAutocompleteHandler),
    (r'/a/register', AdminRegisterHandler),
    (r'/a/evaluations', AdminEvaluationsHandler)
]