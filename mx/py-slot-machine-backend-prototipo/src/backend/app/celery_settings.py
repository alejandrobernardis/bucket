#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 11/09/2013 15:03


def log_failure(self, exc, task_id, args, kwargs, einfo):
    import logging
    logging.error("[%s] failed: %r" % (task_id, exc, ))


BROKER_URL = "amqp://celery:f1Gm3Nt2016SyS@localhost//"
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("celery_tasks",)
CELERY_ENABLE_UTC = True
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
CELERY_ANNOTATIONS = {'*': {'on_failure': log_failure, 'rate_limit': '1000/m'},}