#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Asumi Kamikaze Inc.
# Copyright (c) 2012 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Sep 13, 2012 4:32:34 PM

import re
from com.ak.common.security import Password
from mongoengine import StringField

#: -- helpers ------------------------------------------------------------------

__all__ = ['PasswordField',]

#: -- fields -------------------------------------------------------------------

password_exp = re.compile(r'^sha1\$([A-Z0-9]+)', re.IGNORECASE)

class PasswordField(StringField):
    def __set__(self, instance, value):
        if value and not password_exp.search(str(value)):
            value = Password.generate(str(value))
        StringField.__set__(self, instance, value)
        
#: -----------------------------------------------------------------------------