#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 02/Dec/2013 16:17

BROKER_URL = 'amqp://celery:C3L3r1P455w0Rd@localhost//'
CELERY_RESULT_BACKEND = "amqp"
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
CELERY_IMPORTS = ('tasks',)
CELERY_ANNOTATIONS = {'*': {'rate_limit': '5000/m'}}
CELERY_IGNORE_RESULT = True