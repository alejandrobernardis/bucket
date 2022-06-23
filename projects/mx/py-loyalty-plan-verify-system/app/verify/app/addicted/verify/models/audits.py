#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 20/Feb/2014 13:12


from addicted.verify.models.base import BaseDocument
from mongoengine import StringField


class Audit(BaseDocument):
    activity = StringField(max_length=255, required=True)
    message = StringField(max_length=500, required=True)
    session = StringField(max_length=128)
    remote_ip = StringField(max_length=64, required=True)
    user = StringField(max_length=32)

    meta = {
        'db_alias': 'default',
        'collection': 'audits',
    }


class Logs(BaseDocument):
    activity = StringField(max_length=255, required=True)
    message = StringField(max_length=500, required=True)
    session = StringField(max_length=255)
    remote_ip = StringField(max_length=64, required=True)
    user = StringField(max_length=32)

    meta = {
        'db_alias': 'default',
        'collection': 'logs',
    }