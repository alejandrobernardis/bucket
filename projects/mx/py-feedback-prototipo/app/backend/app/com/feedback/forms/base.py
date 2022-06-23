#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 22/May/2014 18:22

from wtforms.fields import Field, StringField
from wtforms.validators import Regexp, ValidationError


class NoneOfRegex(Regexp):
    def __init__(self, regex, flags=0, message=None):
        super(NoneOfRegex, self).__init__(regex, flags, message=message)

    def __call__(self, form, field, message=None):
        if self.regex.match(field.data or ''):
            if message is None:
                if self.message is None:
                    message = field.gettext(u'Esta utilizando palabras no '
                                            u'permitidas para la búsqueda.')
                else:
                    message = self.message
            raise ValidationError(message)


class ListField(Field):
    def _value(self):
        if self.data:
            return self.data
        else:
            return []

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist]
        else:
            self.data = []