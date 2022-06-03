# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 02/Jun/2014 11:03


def helper_rate(value):
    try:
        return {
            1: 'Muy Mala',
            2: 'Mala',
            3: 'Regular',
            4: 'Bien',
            5: 'Muy Bien'
        }[int(value)]
    except:
        return 'No disponible'


def helper_rate_str(value):
    try:
        return {
            'muy mala': 1,
            'mala': 2,
            'regular': 3,
            'bien': 4,
            'muy bien': 5
        }[str(value).lower()]
    except:
        return -1


def helper_rate_label(value):
    try:
        return {
            1: 'danger',
            2: 'warning',
            3: 'default',
            4: 'primary',
            5: 'success',
        }[int(value)]
    except:
        return 'default'


def helper_dispatch(value):
    try:
        return {
            1: 'Cada semana',
            2: 'Cada 2 semanas',
            4: 'Cada 4 semanas'
        }[int(value)]
    except:
        return 'Cada 4 semanas'


def helper_dispatch_str(value):
    try:
        return {
            'cada semana': 1,
            'cada 2 semanas': 2,
            'cada 4 semanas': 4
        }[str(value).lower()]
    except:
        return -1

def helper_provider(value):
    try:
        return {
            1: 'Todos',
            2: 'Figment',
            3: 'Kinetiq'
        }[int(value)]
    except:
        return '-'


def helper_answer_mode(value):
    try:
        return {
            1: 'fa-envelope',
            2: 'fa-phone',
        }[int(value)]
    except:
        return 'fa-exclamation-triangle'