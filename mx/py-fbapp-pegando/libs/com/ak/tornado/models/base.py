#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: May 29, 2012, 8:39:52 AM

import re, datetime

from bson.objectid import ObjectId
from com.ak.tornado.security import Password
from com.ak.tornado.utils import is_primitive, datetime_to_str
from mongoengine import Document, StringField, DateTimeField, BooleanField, Q

#: -- helpers ------------------------------------------------------------------

__all__ = [
    "PasswordField",
    "DateCompare",
    "ControlDocument",
]

#: -- fields -------------------------------------------------------------------

password_exp = re.compile(r"^sha1\$([A-Z0-9]+)", re.IGNORECASE)

class PasswordField(StringField):
    def __set__(self, instance, value):
        if value and not password_exp.search(str(value)):
            value = Password.generate(str(value))
        StringField.__set__(self, instance, value)

#: -- DateCompare --------------------------------------------------------------

class DateCompare(object):
    def __init__(self, date=None, date_min=-1, date_max=1):
        self.date = date or datetime.datetime.now()

        compare_min = datetime.datetime(self.date.year, self.date.month,
                                        self.date.day, 23, 59, 59)

        self.min = datetime.timedelta(days=date_min) + compare_min

        compare_max = datetime.datetime(self.date.year, self.date.month,
                                        self.date.day, 0, 0, 0)

        self.max = datetime.timedelta(days=date_max) + compare_max

#: -- models -------------------------------------------------------------------

class ControlDocument(Document):
    meta = {
        "abstract": True
    }

    #: fields
    availabled = BooleanField(default=False)
    enabled = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.now())
    modified = DateTimeField(default=datetime.datetime.now())

    #: methods
    def get_date_compare(self, date=None, date_min=-1, date_max=1):
        return DateCompare(date, date_min, date_max)

    def _datetime_update(self, key, value=None, update_data=None):
        try:
            if not value:
                value = datetime.datetime.now()
            if not update_data:
                update_data = dict()
            update_data["set__"+key] = value
            self.update(**update_data)
            self.reload()
            return True
        except:
            return False

    def set_modified(self, value=None):
        return self._datetime_update("modified", value)

    def set_modified_with_data(self, update_data, value=None):
        return self._datetime_update("modified", value, update_data)

    def _status_update(self, key, value=False):
        try:
            update_data = dict()
            update_data["set__"+key] = value
            return self.set_modified_with_data(update_data)
        except:
            return False

    def set_availabled(self, value=False):
        return self._status_update("availabled", value)

    def set_enabled(self, value=False):
        return self._status_update("enabled", value)

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
                elif isinstance(value, datetime.datetime) or \
                     isinstance(value, datetime.date):
                    value = datetime_to_str(value)
                else:
                    value = value.to_object()
            except Exception:
                value = None
            if not field_name in ignore:
                data[field_name] = value
        return data

    def _get_status_query(self, enabled=True, availabled=True):
        return ControlDocument.get_status_query(enabled, availabled)

    @staticmethod
    def get_status_query(enabled=True, availabled=True):
        return Q(enabled=enabled)&Q(availabled=availabled)

#: -----------------------------------------------------------------------------

