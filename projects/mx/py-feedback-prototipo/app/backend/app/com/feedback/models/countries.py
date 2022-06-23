#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 09/Dec/2013 09:44

from com.feedback.models.base import BaseDocument
from mongoengine import Q, StringField, IntField


class Country(BaseDocument):
    name = StringField(max_length=128)
    iso_alpha_2 = StringField(max_length=2)
    iso_alpha_3 = StringField(max_length=3)
    iso_number = IntField()

    meta = {
        'db_alias': 'default',
        'collection': 'countries',
    }

    @staticmethod
    def get_by_name(value, enabled=True, available=True):
        return Country.get_by__first(Q(name=value), enabled, available)

    @staticmethod
    def get_by_alpha2(value, enabled=True, available=True):
        return Country.get_by__first(Q(iso_alpha_2=value), enabled, available)

    @staticmethod
    def get_by_alpha3(value, enabled=True, available=True):
        return Country.get_by__first(Q(iso_alpha_3=value), enabled, available)

    @staticmethod
    def get_by_number(value, enabled=True, available=True):
        return Country.get_by__first(Q(number=value), enabled, available)
