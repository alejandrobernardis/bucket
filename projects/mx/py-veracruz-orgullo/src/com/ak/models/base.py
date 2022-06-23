#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Asumi Kamikaze Inc.
# Copyright (c) 2012 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Sep 13, 2012 4:24:12 PM

from bson.objectid import ObjectId
from com.ak.common.utils import is_primitive, datetime_to_str
from datetime import date, datetime, timedelta
from mongoengine import Document, DateTimeField, BooleanField,EmbeddedDocument, Q

#: -- helpers ------------------------------------------------------------------

__all__ = ['DateCompare', 'ControlDocument']

#: -- DateCompare --------------------------------------------------------------

class DateCompare(object):
    def __init__(self, date=None, date_min=-1, date_max=1):
        self.date = date or datetime.now()
        compare_min = datetime(self.date.year, self.date.month, self.date.day, 
                               23, 59, 59)
        self.min = timedelta(days=date_min) + compare_min
        compare_max = datetime(self.date.year, self.date.month, self.date.day, 
                               0, 0, 0)
        self.max = timedelta(days=date_max) + compare_max

#: -- ControlDocument ----------------------------------------------------------

class ControlDocument(Document):
    meta = {
        'abstract': True
    }

    #: fields
    available = BooleanField(default=False)
    enabled = BooleanField(default=False)
    created = DateTimeField(default=datetime.now())
    modified = DateTimeField(default=datetime.now())

    #: methods
    def get_date_compare(self, date=None, date_min=-1, date_max=1):
        return DateCompare(date, date_min, date_max)

    def _datetime_update(self, key, value=None, update_data=None):
        try:
            if not value:
                value = datetime.now()
            if not update_data:
                update_data = dict()
            update_data['set__'+key] = value
            self.update(**update_data)
            self.reload()
            return True
        except:
            return False

    def set_modified(self, value=None):
        return self._datetime_update('modified', value)

    def set_modified_with_data(self, update_data, value=None):
        return self._datetime_update('modified', value, update_data)

    def _status_update(self, key, value=False):
        try:
            update_data = dict()
            update_data['set__'+key] = value
            return self.set_modified_with_data(update_data)
        except:
            return False

    def set_available(self, value=True):
        return self._status_update('available', value)

    def set_enabled(self, value=True):
        return self._status_update('enabled', value)

    def set_logic_low(self):
        update_data = dict(set__available=False, set__enabled=False)
        return self.set_modified_with_data(update_data)

    def set_logic_high(self):
        update_data = dict(set__available=True, set__enabled=True)
        return self.set_modified_with_data(update_data)

    def to_object(self, ignore=[]):
        data = {}
        for field_name, _ in self._fields.items():
            value = getattr(self, field_name, None)
            try:
                if not value:
                    raise
                elif is_primitive(value):
                    value = value
                elif isinstance(value, ObjectId):
                    value = value.__str__()
                elif isinstance(value, datetime) or \
                     isinstance(value, date):
                    value = datetime_to_str(value)
                elif issubclass(value.__class__, EmbeddedDocument):
                    embedd = {}
                    for a in value:
                        if not a in ignore:
                            embedd[a] = value[a]
                    value = embedd
                else:
                    value = value.to_object(ignore)
            except:
                value = None
            if not field_name in ignore:
                data[field_name] = value
        return data
    
    #: pagination
    def _do_paginate(self, cls, query=None, page_number=1, page_size=50, 
                    order_by="-created"):
        return ControlDocument.do_paginate(cls, query, page_number, page_size, 
                                           order_by)
    
    @classmethod    
    def do_paginate(cls, query=None, page_number=1, page_size=50, 
                    order_by="-created"):
        try:
            return cls.objects(query)\
                      .skip(page_size*(page_number-1))\
                      .limit(page_size)\
                      .order_by(order_by)
        except:
            return None

    #: get first
    @classmethod
    def _get_by__first(cls, query, enabled=True, available=True):
        try:
            if not query: 
                raise
            _Q = ControlDocument.get_status_query(enabled, available)&query
            return cls.objects(_Q).first()
        except:
            return None
    
    #: status
    def _get_status_query(self, enabled=True, available=True):
        return ControlDocument.get_status_query(enabled, available)

    @staticmethod
    def get_status_query(enabled=True, available=True):
        return Q(enabled=enabled)&Q(available=available)
    