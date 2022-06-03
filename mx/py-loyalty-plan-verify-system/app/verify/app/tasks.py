#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 02/Dec/2013 16:16

from __future__ import absolute_import

import os
import sys
import settings

_parent_path = os.path.split(settings.ROOT_PATH)[0]

for folder in ('../../bin', '../../lib',):
    folder_path = os.path.join(_parent_path, folder)
    if os.path.isdir(folder_path):
        sys.path.insert(0, folder_path)

from celery import Celery

celery = Celery()
celery.config_from_object('tasks_settings')


@celery.task(ignore_result=True)
def default_task():
    print 'Default Task...'