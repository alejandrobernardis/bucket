#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: 1/9/13, 7:58 AM

from settings import DATABASE_MULTIPLE
from com.ak.models.base import ControlDocument
from mongoengine import StringField, IntField

#: models
class Country(ControlDocument):
    meta = {
        'db_alias': DATABASE_MULTIPLE['users']['alias'],
        'collection': 'countries',
        'indexes': ['pid']
    }

    pid = IntField(unique=True)
    name = StringField(max_length=128)

    @staticmethod
    def get_by_id(pid):
        try:
            ref = Country.objects(pid=pid).first()
            if not ref:
                raise
            return ref
        except:
            return None