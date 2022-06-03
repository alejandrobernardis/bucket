#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 23/Feb/2014 15:49

from addicted.verify.core.regex import regex_query, regex_query_audit, bad_words
from wtforms.fields import TextField, RadioField
from wtforms.validators import InputRequired, Length, Regexp, NoneOf, \
    ValidationError
from wtforms_tornado import Form


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


class SearchForm(Form):
    q = TextField('Buscar', [
        InputRequired(u'Por favor, defina un criterio de búsqueda.'),
        Length(min=4, message=u'El mínimo requerido es de 4 caracteres '
                              u'para el criterio de búsqueda.'),
        Regexp(regex_query, message=u'Para el criterio de búsqueda solo se '
                                       u'permiten los siguientes caracteres: '
                                       u'A-Z, a-z, 0-9, #, -, _'),
        NoneOfRegex(regex_query_audit, message=u'Esta utilizando palabras no '
                                               u'permitidas para la búsqueda.'),
        NoneOf(bad_words, message=u'Esta utilizando palabras no '
                                  u'permitidas para la búsqueda.')
    ], default='')

    filter = RadioField('Filtro', [
        InputRequired(u'Por favor, seleccione un filtro para la búsqueda.')
    ], choices=[
        ('all', ''),
        ('first_name', ''),
        ('last_name', ''),
        ('email', ''),
        ('address', ''),
        ('phone', ''),
        ('card', ''),
    ], default='all')