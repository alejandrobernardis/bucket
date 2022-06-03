#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Asumi Kamikaze Inc.
# Copyright (c) 2012 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Sep 13, 2012 4:24:58 PM

import datetime
from settings import DATABASE_MULTIPLE
from bson.objectid import ObjectId
from com.ak.models.base import ControlDocument
from com.ak.models.fields import PasswordField
from com.ak.common.security import Password, secret_key, activation_key
from com.ak.common.utils import safe_str_cmp
from mongoengine import StringField, EmailField, DateTimeField, IntField, \
    BooleanField, ReferenceField, CASCADE, Q
from mx.dip.voj.models.countries import Country

#: -- helpers ------------------------------------------------------------------

__all__ = ['User']

#: -- models -------------------------------------------------------------------

class User(ControlDocument):
    meta = {
        'db_alias': DATABASE_MULTIPLE['users']['alias'],
        'collection': 'users',
        'indexes': ['token','facebook_uid','email','username']
    }
    
    #: fields
    token = StringField(max_length=64, unique=True)
    facebook_uid = StringField(max_length=128, unique=True)
    email = EmailField(max_length=255, required=True, unique=True)
    username = StringField(max_length=32, required=True, unique=True)
    password = PasswordField(max_length=128, required=True)
    secret_question = StringField(max_length=255)
    secret_answer = StringField(max_length=255)
    activation_key = StringField(max_length=64)
    activation_key_expire = DateTimeField()
    last_login = DateTimeField(default=datetime.datetime.now())
    remote_ip = StringField(max_length=64)
    role_id = IntField(min_value=1, required=True)
    role_name = StringField(max_length=32, required=True)
    
    #: =========================================================================

    first_name = StringField(max_length=64)
    middle_name = StringField(max_length=64)
    last_name = StringField(max_length=64)
    birthday = DateTimeField()
    city = StringField(max_length=64)
    terms = BooleanField(default=False)
    policy = BooleanField(default=False)
    news = BooleanField(default=False)

    country = ReferenceField(Country, CASCADE)
    
    def is_facebook(self):
        return ('fb__' not in self.facebook_uid)

    def get_country_id(self):
        return self.country.pid

    def get_country_name(self):
        return self.country.name

    #: =========================================================================
    
    #: methods
    def _set_new_password(self, password=None, update_data=None):
        try:
            if not password:
                password = secret_key(8)
            if not update_data:
                update_data = dict()
            update_data['set__password'] = password
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
            if not self.activation_key\
                or not safe_str_cmp(key, self.activation_key)\
                or not self.activation_key_expire\
                or self.activation_key_expire < datetime.datetime.today():
                raise
            update_data = dict(
                set__enabled=True,
                set__activation_key=None,
                set__activation_key_expire=None)
            return self.set_modified_with_data(update_data)
        except:
            return False
        
    def do_validate_secret_answer(self, value):
        try:
            if value:
                return safe_str_cmp(value, self.secret_answer)
            raise
        except:
            return False
        
    def set_last_login(self, value=None):
        return self._datetime_update('last_login', value)
    
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
    def get_complex(uid, enabled=True, available=True):
        try:
            _Q = Q(facebook_uid=uid)|Q(username=uid)|\
                 Q(email=uid)|Q(token=uid)|Q(activation_key=uid)
            try:
                _QUID = ObjectId(uid)
                _Q = Q(id=_QUID)|_Q
            except: 
                pass
            return User._get_by__first(_Q, enabled, available)
        except:
            return None
    
    @staticmethod
    def get_by_uid(value, enabled=True, available=True):
        try:
            _Q = Q(id=ObjectId(value))
            return User._get_by__first(_Q, enabled, available)
        except: 
            return None
    
    @staticmethod
    def get_by_token(value, enabled=True, available=True):
        _Q = Q(token=value)
        return User._get_by__first(_Q, enabled, available)
    
    @staticmethod
    def get_by_facebook_uid(value, enabled=True, available=True):
        _Q = Q(facebook_uid=value)
        return User._get_by__first(_Q, enabled, available)

    @staticmethod
    def get_by_username(value, enabled=True, available=True):
        _Q = Q(username=value)
        return User._get_by__first(_Q, enabled, available)
    
    @staticmethod
    def get_by_email(value, enabled=True, available=True): 
        _Q = Q(email=value)
        return User._get_by__first(_Q, enabled, available)
    
    @staticmethod
    def get_by_activation_key(value, enabled=True, available=True):
        if value: 
            _Q = Q(activation_key=value)
            return User._get_by__first(_Q, enabled, available)
        return None
    
#: -----------------------------------------------------------------------------
