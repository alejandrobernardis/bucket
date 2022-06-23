#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 14/May/2014 15:08

import datetime
from com.feedback.models.base import BaseDocument
from com.feedback.models.users import User
from mongoengine import EmbeddedDocument, StringField, IntField, BooleanField, \
    DateTimeField, ListField, ReferenceField, EmbeddedDocumentField


class Answer(EmbeddedDocument):
    username = StringField(max_length=256, required=True)
    reference = ReferenceField(User, required=True)
    description = StringField(max_length=1000)
    mode = IntField(1, 2, default=1, required=True)
    available = BooleanField(default=False)
    enabled = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.utcnow)
    modified = DateTimeField(default=datetime.datetime.utcnow)


class Evaluation(BaseDocument):
    activation_key = StringField(max_length=255, unique=True)
    client = StringField(max_length=256, required=True)
    provider = IntField(1, 3, default=1, required=True)
    reference = ReferenceField(User, required=True)
    description = StringField(max_length=1000)
    rate = IntField(1, 5, default=1, required=True)
    answers = ListField(EmbeddedDocumentField(Answer), default=list)
    policy = BooleanField(default=False)

    meta = {
        'db_alias': 'default',
        'collection': 'evaluations',
        'indexes': ['client', 'activation_key', ('-created', 'rate')]
    }


class EvaluationPending(BaseDocument):
    username = StringField(max_length=256, required=True)
    token = StringField(max_length=128, unique=True)
    activation_key = StringField(max_length=255, unique=True)
    public_key = StringField(max_length=255, unique=True)
    public_key_method = StringField(max_length=16)
    public_key_expires = DateTimeField(default=datetime.datetime.utcnow)
    private_key = StringField(max_length=16, unique=True)

    meta = {
        'db_alias': 'default',
        'collection': 'evaluations_pending',
        'indexes': ['username', 'token', 'activation_key', '-created']
    }

