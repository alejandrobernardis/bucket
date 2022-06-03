#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: May 29, 2012, 8:36:01 AM

import datetime

from bson.objectid import ObjectId
from com.ak.tornado.models.base import ControlDocument, PasswordField
from com.ak.tornado.security import Password, Role, secret_key, activation_key
from mongoengine import StringField, IntField, URLField, EmailField,\
                        DateTimeField, BooleanField, Q, ReferenceField, CASCADE

#: -- helpers ------------------------------------------------------------------

__all__ = [
    "UserRole",
    "UserGender",
    "User",
]

#: -- models -------------------------------------------------------------------

class UserRole(ControlDocument):
    meta = {
        "collection": "user_roles",
        "indexes": ["name"]
    }

    #: fields
    name = StringField(max_length=64, unique=True)
    permissions = IntField(default=0)
    level = IntField(default=0)
    admin = BooleanField(default=False)
    read = BooleanField(default=False)
    write = BooleanField(default=False)

    #: methods
    def allow(self, value):
        return value >= self.permissions

    def get_role_object(self):
        role = Role.get_role(self.name)
        if not role:
            role = Role(self.name, self.write, self.admin, self.level)
        return role

    #: methods
    @staticmethod
    def _get_by__first(query, enabled=True, availabled=True):
        try:
            if not query:
                raise
            _Q = ControlDocument.get_status_query(enabled, availabled)&query
            return UserRole.objects(_Q).first()
        except:
            return None

    @staticmethod
    def get_by_id(value):
        try:
            _Q = Q(id=ObjectId(value))
            return UserRole._get_by__first(_Q)
        except:
            return None

    @staticmethod
    def get_by_name(value):
        _Q = Q(name=value)
        return UserRole._get_by__first(_Q)

    @staticmethod
    def get_by_permissions(value):
        _Q = Q(permissions=value)
        return UserRole._get_by__first(_Q)

    @staticmethod
    def get_all_by_permissions(value):
        _Q = ControlDocument.get_status_query()&Q(permissions=value)
        return UserRole.objects(_Q).all()

#: -----------------------------------------------------------------------------

class UserGender(ControlDocument):
    meta = {
        "collection": "user_genders",
        "indexes": ["uid"]
    }

    #: fields
    uid = IntField(unique=True)
    name = StringField(max_length=16)

    #: methods
    @staticmethod
    def _get_by__first(query, enabled=True, availabled=True):
        try:
            if not query:
                raise
            _Q = ControlDocument.get_status_query(enabled, availabled)&query
            return UserGender.objects(_Q).first()
        except:
            return None

    @staticmethod
    def get_by_id(value):
        try:
            _Q = Q(id=ObjectId(value))
            return UserGender._get_by__first(_Q)
        except:
            return None

    @staticmethod
    def get_by_uid(value):
        _Q = Q(uid=value)
        return UserGender._get_by__first(_Q)

    @staticmethod
    def get_by_name(value):
        _Q = Q(name=value)
        return UserGender._get_by__first(_Q)

#: -----------------------------------------------------------------------------

class User(ControlDocument):
    meta = {
        "collection": "users",
        "indexes": ["token", "facebook_uid", "username"]
    }

    #: reference
    #role = ReferenceField(UserRole, CASCADE)
    #gender = ReferenceField(UserGender, CASCADE)

    #: fields
    token = StringField(max_length=64, unique=True)
    facebook_uid = StringField(max_length=128, unique=True)
    username = StringField(max_length=32, required=True, unique=True)
    password = PasswordField(max_length=128, required=True)
    email = EmailField(max_length=255, required=True, unique=True)
    first_name = StringField(max_length=64)
    middle_name = StringField(max_length=64)
    last_name = StringField(max_length=64)
    birthday = DateTimeField()
    avatar = URLField()
    secret_question = StringField(max_length=255)
    secret_answer = StringField(max_length=255)
    activation_key = StringField(max_length=64)
    activation_key_expire = DateTimeField()
    notes = StringField(max_length=500)
    location = StringField(max_length=128)
    terms = BooleanField(default=False)
    policy = BooleanField(default=False)
    news = BooleanField(default=False)
    remote_ip = StringField(max_length=64)
    last_login = DateTimeField(default=datetime.datetime.now())

    #: methods
    def _set_new_password(self, password=None, update_data=None):
        try:
            if not password:
                password = secret_key(8)
            if not update_data:
                update_data = dict()
            update_data["set__password"] = password
            return self.set_modified_with_data(update_data)
        except:
            return False

    def set_new_password(self, password=None):
        return self._set_new_password(password)

    def set_activation_key(self, expire_days=1):
        try:
            key = activation_key(self.username, self.email)
            key_expire = datetime.datetime.now()\
                       + datetime.timedelta(days=expire_days)
            update_data = dict(
                set__enabled=False,
                set__activation_key=key,
                set__activation_key_expire=key_expire)
            return self.set_modified_with_data(update_data)
        except:
            return False

    def set_activation_key_password(self, password=None):
        update_data = dict(set__enabled=True)
        return self._set_new_password(password, update_data)

    def do_validate_activation_key(self, key):
        try:
            if not self.activation_key \
                or not self.activation_key_expire \
                or self.activation_key_expire < datetime.datetime.today():
                raise
            update_data = dict(
                set__enabled=True,
                set__activation_key=None,
                set__activation_key_expire=None)
            return self.set_modified_with_data(update_data)
        except:
            return False

    def set_last_login(self, value=None):
        return self._datetime_update("last_login", value)

    #: -- auth -----------------------------------------------------------------

    @staticmethod
    def do_auth_login(username, password):
        try:
            user = User.objects(ControlDocument.get_status_query()&
                                Q(username=username)|Q(email=username)).first()
            auth = Password.check(password, user.password) if user else False
            return user, auth
        except:
            return None, False

    @staticmethod
    def do_auth_forgot_password(username):
        try:
            return User.objects(ControlDocument.get_status_query()&
                                Q(username=username)|Q(email=username)).first()
        except:
            return None

    #: -- query's --------------------------------------------------------------

    @staticmethod
    def get_complex(uid, enabled=True, availabled=True):
        try:
            _Q = Q(facebook_uid=uid)|Q(username=uid)|Q(email=uid)|\
                 Q(token=uid)|Q(activation_key=uid)
            try:
                _QUID = ObjectId(uid)
                _Q = Q(id=_QUID)|_Q
            except: pass
            _Q = ControlDocument.get_status_query(enabled, availabled)&_Q
            return User.objects(_Q).first()
        except:
            return None

    @staticmethod
    def _get_by__first(query, enabled=True, availabled=True):
        try:
            if not query:
                raise
            _Q = ControlDocument.get_status_query(enabled, availabled)&query
            return User.objects(_Q).first()
        except:
            return None

    @staticmethod
    def get_by_uid(value, enabled=True, availabled=True):
        try:
            _Q = Q(id=ObjectId(value))
            return User._get_by__first(_Q, enabled, availabled)
        except:
            return None

    @staticmethod
    def get_by_token(value, enabled=True, availabled=True):
        _Q = Q(token=value)
        return User._get_by__first(_Q, enabled, availabled)

    @staticmethod
    def get_by_facebook_uid(value, enabled=True, availabled=True):
        _Q = Q(facebook_uid=value)
        return User._get_by__first(_Q, enabled, availabled)

    @staticmethod
    def get_by_username(value, enabled=True, availabled=True):
        _Q = Q(username=value)
        return User._get_by__first(_Q, enabled, availabled)

    @staticmethod
    def get_by_email(value, enabled=True, availabled=True):
        _Q = Q(email=value)
        return User._get_by__first(_Q, enabled, availabled)

    @staticmethod
    def get_by_activation_key(value, enabled=True, availabled=True):
        _Q = Q(activation_key=value)
        return User._get_by__first(_Q, enabled, availabled)

    @staticmethod
    def get_by_role(value, enabled=True, availabled=True):
        _Q = Q(activation_key=value)
        return User._get_by__first(_Q, enabled, availabled)

#: -----------------------------------------------------------------------------

