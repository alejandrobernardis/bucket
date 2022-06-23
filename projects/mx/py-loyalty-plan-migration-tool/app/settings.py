#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 29/Jan/2014 15:38

import os

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
REPORT_PATH = os.path.join(ROOT_PATH, 'report')
ASSETS_PATH = os.path.abspath(os.path.join(ROOT_PATH, '../assets'))
VERBOSE = True
DB_MX_COM_LUXURYHALLREWARDS = 'luxuryhallrewards'
DB_MX_COM_LUXURYONE = 'mx_com_luxuryone_concierge'

DATABASES = {
    DB_MX_COM_LUXURYHALLREWARDS: {
        'host': 'localhost', # 'localhost'
        'user': 'root',
        'password': '',
        'database': 'luxuryhallrewards',
        'raise_on_warnings': True
    },
    DB_MX_COM_LUXURYONE: {
        'host': 'localhost', # 'localhost'
        'user': 'root',
        'password': '',
        'database': 'mx_com_luxuryone_concierge',
        'raise_on_warnings': True
    }
}

