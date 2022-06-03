#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 26/Mar/2014 18:56

from addicted.verify.core.regex import bad_words
from wtforms.fields import TextField
from wtforms.validators import InputRequired, Length, NoneOf
from wtforms_tornado import Form


class SearchForm(Form):
    q = TextField('Buscar', [
        InputRequired(u'Por favor, defina un criterio de búsqueda.'),
        Length(min=4, message=u'El mínimo requerido es de 4 caracteres '
                              u'para el criterio de búsqueda.'),
        NoneOf(bad_words, message=u'Esta utilizando palabras no '
                                  u'permitidas para la búsqueda.')
    ], default='')
