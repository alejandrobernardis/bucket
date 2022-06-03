#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 20/Feb/2014 10:12


from addicted.verify.models.base import BaseDocument
from mongoengine import StringField, ListField, ReferenceField, PULL


class Store(BaseDocument):
    name = StringField(max_length=128, required=True, unique=True)

    meta = {
        'db_alias': 'default',
        'collection': 'stores',
        'indexes': ['name']
    }


class StoreGroup(BaseDocument):
    name = StringField(max_length=128, required=True, unique=True)
    stores = ListField(ReferenceField(Store, reverse_delete_rule=PULL))

    meta = {
        'db_alias': 'default',
        'collection': 'stores_group',
        'indexes': ['name']
    }
