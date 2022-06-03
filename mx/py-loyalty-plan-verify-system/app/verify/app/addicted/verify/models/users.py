#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 05/Dec/2013 23:06

import datetime
from bson import ObjectId
from addicted.verify.core.utils import secret_key, activation_key, safe_str_cmp
from addicted.verify.models.base import BaseDocument, PasswordField, \
    PermissionField
from addicted.verify.models.stores import Store
from addicted.verify.security.password import SHA1PasswordHasher
from mongoengine import Q, StringField, BooleanField, DateTimeField, \
    EmailField, ReferenceField


class User(BaseDocument):
    store = ReferenceField(Store)
    email = EmailField(max_length=255, required=True, unique=True)
    username = StringField(max_length=32, required=True, unique=True)
    password = PasswordField(max_length=128, required=True)
    fbuid = StringField(max_length=128)
    permissions = PermissionField()
    secret_question = StringField(max_length=255)
    secret_answer = StringField(max_length=255)
    activation_key = StringField(max_length=64)
    activation_key_expire = DateTimeField()
    first_name = StringField(max_length=128)
    last_name = StringField(max_length=128)
    phone_lada = StringField(max_length=32)
    phone_number = StringField(max_length=128)
    policy = BooleanField(default=False)
    last_login = DateTimeField(default=datetime.datetime.utcnow)
    remote_ip = StringField(max_length=64)

    meta = {
        'db_alias': 'default',
        'collection': 'users',
        'indexes': ['email', 'username']
    }

    def set_last_login(self, value=None):
        return self._datetime_update('last_login', value)

    def _password_update(self, value=None, data=None):
        if not value:
            value = secret_key(8)
        elif not data:
            data = {}
        data['set__password'] = SHA1PasswordHasher().make(value)
        return value, self._modified_data(data)

    def set_password(self, value=None):
        return self._password_update(value)

    def set_activation_key(self, expires=1):
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=expires)
        return self._modified_data({
            'set__enabled': False,
            'set__activation_key': activation_key(self.username, self.email),
            'set__activation_key_expire': expires,
        })

    def set_activation_key_password(self, key, value=None):
        if not self.verify_activation_key(key):
            raise ValueError('Activation key not valid')
        return self._password_update(value, {
            'set__enabled': True,
            'set__activation_key': None,
            'set__activation_key_expire': None,
        })

    def validate_activation_key(self, key):
        if not self.verify_activation_key(key):
            raise ValueError('Activation key not valid')
        return self._modified_data({
            'set__enabled': True,
            'set__activation_key': None,
            'set__activation_key_expire': None,
        })

    def verify_activation_key(self, key):
        if not self.activation_key \
                or not isinstance(key, basestring) \
                or not safe_str_cmp(key, self.activation_key) \
                or not self.activation_key_expire \
                or self.activation_key_expire < datetime.datetime.utcnow():
            return False
        return True

    def validate_secret_answer(self, value):
        if value and isinstance(value, basestring):
            return safe_str_cmp(value, self.secret_answer)
        return False

    @staticmethod
    def auth_login(username, password):
        if not username and not isinstance(username, basestring) \
                or not password and not isinstance(password, basestring):
            raise ValueError('Username or password not valid')
        query = Q(username=username) | Q(email=username)
        user = User.objects(User.logic_low(query=query)).first()
        auth = False if not user else \
            SHA1PasswordHasher().verify(password, user.password)
        return user, auth

    @staticmethod
    def auth_verify(username):
        if not username and not isinstance(username, basestring):
            raise ValueError('Username not valid')
        query = Q(username=username) | Q(email=username)
        return User.objects(User.logic_low(query=query)).first()

    @staticmethod
    def get_by_complexity(value, enabled=True, available=True):
        query = Q(username=value) | Q(email=value) | Q(fbuid=value) |\
            Q(activation_key=value)
        try:
            query = Q(id=ObjectId(value)) | query
        except Exception:
            pass
        return User.get_by__first(query, enabled, available)

    @staticmethod
    def get_by_id(value, enabled=True, available=True):
        return User.get_by__first(Q(id=ObjectId(value)), enabled, available)

    @staticmethod
    def get_by_username(value, enabled=True, available=True):
        return User.get_by__first(Q(username=value), enabled, available)

    @staticmethod
    def get_by_email(value, enabled=True, available=True):
        return User.get_by__first(Q(email=value), enabled, available)

    @staticmethod
    def get_by_fbuid(value, enabled=True, available=True):
        return User.get_by__first(Q(fbuid=value), enabled, available)

    @staticmethod
    def get_by_activation_key(value, enabled=True, available=True):
        return User.get_by__first(Q(activation_key=value), enabled, available)


class PreRegister(BaseDocument):
    company = StringField(max_length=128, required=True)
    first_name = StringField(max_length=128)
    last_name = StringField(max_length=128)
    email = EmailField(max_length=255, required=True, unique=True)
    phone_lada = StringField(max_length=32)
    phone_number = StringField(max_length=128)
    policy = BooleanField(default=False)
    remote_ip = StringField(max_length=64)
    token = StringField(max_length=128, unique=True)
    activation_key = StringField(max_length=255, unique=True)
    activation_hash = StringField(max_length=255)

    meta = {
        'db_alias': 'default',
        'collection': 'preregister',
        'indexes': ['email']
    }
