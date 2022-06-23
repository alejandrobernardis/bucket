#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 04/Dec/2013 10:35

import copy
import datetime
from bson import ObjectId
from com.feedback.core.regex import regex_pass_sha1
from com.feedback.security.auth import Permission
from com.feedback.security.password import SHA1PasswordHasher
from mongoengine import Q, Document, StringField, BooleanField, \
    DateTimeField, DictField
from mongoengine.queryset.visitor import QCombination


class PasswordField(StringField):
    def __set__(self, instance, value):
        if value and not regex_pass_sha1.search(value):
            value = SHA1PasswordHasher().make(value)
        super(PasswordField, self).__set__(instance, value)


class PermissionField(DictField):
    def __set__(self, instance, value):
        if value and isinstance(value, Permission):
            value = value.to_object()
        super(PermissionField, self).__set__(instance, value)


class BaseDocument(Document):
    available = BooleanField(default=False)
    enabled = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.utcnow)
    modified = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'abstract': True,
        'allow_inheritance': True
    }

    def _datetime_update(self, key, value=None, data=None):
        try:
            if not value:
                value = datetime.datetime.utcnow()
            if not data:
                data = {}
            data['set__%s' % key] = value
            self.update(**data)
            self.reload()
            return True
        except Exception:
            return False

    def _modified_data(self, data, value=None):
        return self._datetime_update('modified', value, data)

    def set_update(self, data, value=None):
        if not isinstance(data, dict):
            raise TypeError('Data invalid, must be a dictionary')
        update = {}
        for k, v in data.items():
            if isinstance(v, (tuple, list, dict,)):
                v = copy.deepcopy(v)
            update['set__%s' % k] = v
        return self._modified_data(update, value)

    def set_modified(self, value=None):
        return self._datetime_update('modified', value)

    def set_available(self, value=True):
        return self._modified_data({'set__available': value})

    def set_enabled(self, value=True):
        return self._modified_data({'set__enabled': value})

    def set_logic_low(self):
        return self._modified_data({
            'set__available': False, 'set__enabled': False
        })

    def set_logic_high(self):
        return self._modified_data({
            'set__available': True, 'set__enabled': True
        })

    @classmethod
    def paginate_wll(cls, query, page=1, size=50, order_by='-created',
                     enabled=True, available=True):
        query = BaseDocument.logic_low(enabled, available) & query
        if not isinstance(order_by, list):
            order_by = [order_by]
        return cls.objects(query)\
            .skip(size*(page-1)).limit(size).order_by(*order_by)

    @classmethod
    def paginate(cls, query, page=1, size=50, order_by='-created'):
        if not isinstance(order_by, list):
            order_by = [order_by]
        return cls.objects(query)\
            .skip(size*(page-1)).limit(size).order_by(*order_by)

    def paginate_wll_(self, query, page=1, size=50, order_by='-created',
                      enabled=True, available=True):
        return BaseDocument.paginate_wll(
            query, page, size, order_by, enabled, available)

    def paginate_(self, query, page=1, size=50, order_by='-created'):
        return BaseDocument.paginate(query, page, size, order_by)

    @classmethod
    def get_by__first(cls, query, enabled=True, available=True):
        if not query or not isinstance(query, (Q, QCombination)):
            raise ValueError('Query not supported')
        query = BaseDocument.logic_low(enabled, available) & query
        return cls.objects(query).first()

    def get_by__first_(self, query, enabled=True, available=True):
        return BaseDocument.get_by__first(query, enabled, available)

    @classmethod
    def get_by_id(cls, value, enabled=True, available=True):
        if isinstance(value, basestring):
            value = ObjectId(value)
        return cls.get_by__first(Q(id=value), enabled, available)

    @staticmethod
    def logic_low(enabled=True, available=True, query=None):
        logic_low = Q(enabled=enabled) & Q(available=available)
        return logic_low if not query else logic_low & query

    def logic_low_(self, enabled=True, available=True, query=None):
        return BaseDocument.logic_low(enabled, available, query)

    @staticmethod
    def compare_date(date=None, date_min=-1, date_max=1):
        if not date:
            date = datetime.datetime.utcnow()
        value = datetime.date(date.year, date.month, date.day)
        return {
            'today': value,
            'min': value - datetime.timedelta(days=date_min),
            'max': value + datetime.timedelta(days=date_max),
        }

    def compare_date_(self, date=None, date_min=-1, date_max=1):
        return BaseDocument.compare_date(date, date_min, date_max)
