#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: 1/9/13, 10:46 AM

from settings import DATABASE_MULTIPLE
from bson.objectid import ObjectId
from com.ak.models.base import ControlDocument
from mongoengine import StringField, DateTimeField, EmbeddedDocumentField, \
    EmbeddedDocument, ReferenceField, CASCADE, Q

#: models
class Image(ControlDocument):
    token = StringField(max_length=64, unique=True)
    alt = StringField(max_length=255)
    src = StringField(max_length=510)
    path = StringField(max_length=510, unique=True)

    @staticmethod
    def get_by_uid(value, enabled=True, available=True):
        try:
            _Q = Q(id=ObjectId(value))
            return Image._get_by__first(_Q, enabled, available)
        except:
            return None

class Track(EmbeddedDocument):
    category = StringField(max_length=128)
    action = StringField(max_length=128)
    label = StringField(max_length=128)
    value = StringField(max_length=128)

class Url(ControlDocument):
    token = StringField(max_length=64, unique=True)
    title = StringField(max_length=255)
    value = StringField(max_length=255, unique=True)
    track = EmbeddedDocumentField(Track)

    @staticmethod
    def get_by_value(value, enabled=True, available=True):
        try:
            _Q = Q(value=value)
            return Url._get_by__first(_Q, enabled, available)
        except:
            return None

class Event(ControlDocument):
    meta = {
        'db_alias': DATABASE_MULTIPLE['events']['alias'],
        'collection': 'events',
        'indexes': ['token']
    }

    #: fields
    token = StringField(max_length=64, unique=True)
    title = StringField(max_length=255)
    date = DateTimeField()
    place = StringField(max_length=255)
    phone = StringField(max_length=128)

    #: ref
    url = ReferenceField(Url, CASCADE)
    image = ReferenceField(Image, CASCADE)

    def get_literal_month(self, value=None):
        value = value or self.date.month
        months = ['-','ENE','FEB','MAR','ABR','MAY','JUN',
                      'JUL','AGO','SEP','OCT','NOV','DIC']
        return months[value]

    @staticmethod
    def get_by_uid(value, enabled=True, available=True):
        try:
            _Q = Q(id=ObjectId(value))
            return Event._get_by__first(_Q, enabled, available)
        except:
            return None

    @staticmethod
    def get_by_uid_woc(value, available=True):
        try:
            _Q = Q(id=ObjectId(value))&Q(available=available)
            return Event.objects(_Q).first()
        except:
            return None
