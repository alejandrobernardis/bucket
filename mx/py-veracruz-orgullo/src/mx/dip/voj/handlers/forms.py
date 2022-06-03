#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: 1/8/13, 2:28 PM

import re
from com.ak.common.forms import BaseForm
from com.ak.common.utils import regex_email_str
from wtforms import TextField, BooleanField, IntegerField, validators

#: === === === === === === === === === === === === === === === === === === === ===

_validator_required = validators.Required()
_validator_optional = validators.Optional()
_validator_regex_email = validators.Regexp(regex_email_str, re.IGNORECASE)
_validator_length_1_to_32 = validators.Length(1, 32)
_validator_length_1_to_64 = validators.Length(1, 64)
_validator_length_1_to_128 = validators.Length(1, 128)
_validator_length_1_to_255 = validators.Length(1, 255)
_validator_length_1_to_510 = validators.Length(1, 510)
_validator_length_2_to_96 = validators.Length(2, 96)
_validator_length_10_to_128 = validators.Length(10, 128)

#: === === === === === === === === === === === === === === === === === === === ===

class RegisterDelete(BaseForm):
    uid = TextField('uid',[
        _validator_required,
        _validator_length_1_to_32
    ])

    token = TextField('token',[
        _validator_required,
        _validator_length_1_to_64
    ])

class RegisterUpdate(RegisterDelete):
    first_name = TextField('first_name', [
        _validator_required,
        _validator_length_2_to_96
    ])

    last_name = TextField('last_name', [
        _validator_required,
        _validator_length_2_to_96
    ])

    email = TextField('email', [
        _validator_required,
        _validator_regex_email
    ])

    birthday = TextField('birthday', [
        _validator_required,
        validators.Regexp(r'(\d+/\d+/\d+)', re.IGNORECASE)
    ])

    country = IntegerField('country', [
        _validator_optional,
        validators.NumberRange(0, 238)
    ])

    city = TextField('city', [
        _validator_optional,
        _validator_length_2_to_96
    ])

    news = BooleanField('news')

class Register(RegisterUpdate):
    fbuid = IntegerField('fbuid', [
        _validator_optional
    ])

    fbusername = TextField('fbusername', [
        _validator_optional,
        _validator_length_1_to_32
    ])

    terms = BooleanField('terms', [
        _validator_required
    ])

    policy = BooleanField('policy', [
        _validator_required
    ])

#: === === === === === === === === === === === === === === === === === === === ===

class EventDelete(RegisterDelete):
    pass

class EventAdd(EventDelete):
    date = TextField('date', [
        _validator_required,
        validators.Regexp(r'(\d+/\d+/\d+)', re.IGNORECASE)
    ])

    title = TextField('title', [
        _validator_required,
        _validator_length_1_to_255
    ])

    place = TextField('place', [
        _validator_required,
        _validator_length_1_to_255
    ])

    phone = TextField('phone', [
        _validator_optional,
        _validator_length_10_to_128
    ])

    track_category = TextField('track category', [
        _validator_optional,
        _validator_length_1_to_128
    ])

    track_action = TextField('track action', [
        _validator_optional,
        _validator_length_1_to_128
    ])

    track_label = TextField('track label', [
        _validator_optional,
        _validator_length_1_to_128
    ])

    url_title = TextField('url title', [
        _validator_optional,
        _validator_length_1_to_255
    ])

    url_value = TextField('url value', [
        _validator_optional,
        _validator_length_1_to_255
    ])

    image_alt = TextField('image alt', [
        _validator_optional,
        _validator_length_1_to_255
    ])

    image_src = TextField('image src', [
        _validator_optional,
        _validator_length_1_to_510
    ])

    enabled = BooleanField('enabled',
        default=False)

class EventUpdate(EventAdd):
    url_id = TextField('url id',[
        _validator_optional,
        _validator_length_1_to_64
    ])

    image_id = TextField('image id',[
        _validator_optional,
        _validator_length_1_to_64
    ])

class EventsDeploy(BaseForm):
    year = TextField('year',[
        _validator_optional,
        validators.Regexp(re.compile(r'0|\d{4}'))
    ])

    month = IntegerField('month',[
        _validator_optional,
        validators.NumberRange(0,12)
    ])