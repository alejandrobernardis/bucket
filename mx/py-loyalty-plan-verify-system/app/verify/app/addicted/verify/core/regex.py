#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 03/Dec/2013 20:08

import re

regex_uid = re.compile(
    r'(?i)(?<![a-z0-9])[0-f]{32}(?![a-z0-9])'
)

regex_sid = re.compile(
    r'(?i)(?<![a-z0-9])[0-f]{8}(?:-[0-f]{4}){3}-[0-f]{12}(?![a-z0-9])'
)

regex_fbuid = re.compile(
    r'^[\d]+$'
)

regex_pass_sha1 = re.compile(
    r'^sha1\$(.+)$'
)

regex_activation_key = re.compile(
    r'^/?[a-f0-9]{32}$',
    re.IGNORECASE
)

regex_activation_key_64 = re.compile(
    r'^/?[a-z0-9%=]+$',
    re.IGNORECASE
)

regex_object_id = re.compile(
    r'^/?[a-f0-9]{24}$',
    re.IGNORECASE
)

regex_username = re.compile(
    r'^[a-z0-9@\.-_]{8,255}$',
    re.IGNORECASE
)

regex_password = re.compile(
    r'^[A-Za-z0-9!@#$=+\.\-_]{8,32}$',
    re.IGNORECASE
)

regex_query = re.compile(
    r'^[\w\s\-#]+$',
    re.UNICODE
)

regex_query_audit = re.compile(
    r'@?((gmai|yaho|hotm|outl|prod|msn|face|terr|goog)'
    r'(l|o|ail|ook|igy|book|a|le)?)(\.\w+)?',
    re.IGNORECASE
)

regex_normalize_email = re.compile(
    r'@.+',
    re.IGNORECASE
)

regex_phone_lada = re.compile(
    r'^\+?[0-9]+(\s[0-9]+)*$',
    re.IGNORECASE
)

regex_phone_number = re.compile(
    r'^[0-9\s]+(\sext\.?\s[0-9]+)?$',
    re.IGNORECASE
)

bad_words = [
    'root', 'admin', 'sysadmin', 'user', 'where', 'select', 'insert',
    'script', 'etc', 'delete', 'remove', 'update', 'make', 'rm', 'sudo',
    'administrator', 'system', 'inject', 'join', 'inner'
]

regex_email = re.compile(
    r'^[a-z0-9\._%\-+]+@[a-z0-9\._%\-]+\.[a-z.]{2,6}$', re.I
)

regex_user = re.compile(
    r'^[a-z0-9_]', re.I
)

regex_option = re.compile(
    r'^(1|2|3)$', re.I
)