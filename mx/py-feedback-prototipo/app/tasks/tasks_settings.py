#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 28/Apr/2014 13:18


def log_failure(self, exc, task_id, args, kwargs, einfo):
    import logging
    logging.error("[%s] failed: %r" % (task_id, exc, ))


BROKER_URL = "amqp://celery:f1Gm3Nt2016SyS@localhost//"
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("tasks",)
CELERY_ENABLE_UTC = True
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
CELERY_DISABLE_RATE_LIMITS = False
CELERY_ANNOTATIONS = {
    'tasks.push__audits': {
        'on_failure': log_failure,
        'rate_limit': '1000/m'
    },
    'tasks.push__logs': {
        'on_failure': log_failure,
        'rate_limit': '1000/m'
    },
    'tasks.push__notifications': {
        'on_failure': log_failure,
        'rate_limit': '3/s'
    },
    'tasks.push__client_notification': {
        'on_failure': log_failure,
        'rate_limit': '3/s'
    },
    'tasks.push__delete_obsolete_data': {
        'on_failure': log_failure,
        'rate_limit': '90/m'
    },
    'tasks.push__unavailable_obsolete_data': {
        'on_failure': log_failure,
        'rate_limit': '500/m'
    }
}
