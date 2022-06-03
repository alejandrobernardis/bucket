# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 14/Jun/2014 10:16 AM

import os
from fabric.api import *

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
APP_PATH = os.path.abspath(os.path.join(ROOT_PATH, './app/backend/app'))
TASKS_PATH = os.path.abspath(os.path.join(ROOT_PATH, './app/tasks'))

def run_app():
    with lcd(APP_PATH):
        local('nohup /usr/bin/python2.7 -m main &')


def run_tasks(level='DEBUG'):
    with lcd(TASKS_PATH):
        local('nohup /usr/local/bin/celery -A tasks worker --loglevel=%s -c 1 &' % level)


def run_tails():
    local('tail -f %s/nohup.out %s/nohup.out' % (APP_PATH, TASKS_PATH))


def run_memcached():
    local('memcached -d -m 64')


def run_mongo():
    command = 'mongod --port 27017 --bind_ip 127.0.0.1 ' \
              '--dbpath /data/db/default/ ' \
              '--pidfilepath /data/db/default/default.pid ' \
              '--logpath /data/db/default/default.log ' \
              '--oplogSize 128 --logappend --fork --journal --smallfiles'
    local(command)


def run_rabbitmq():
    local('rabbitmq-server -detached')


def run_apps():
    run_app()
    run_tasks()


def run_dbs():
    run_memcached()
    run_mongo()
    run_rabbitmq()


def all():
    run_apps()
    run_dbs()
    
