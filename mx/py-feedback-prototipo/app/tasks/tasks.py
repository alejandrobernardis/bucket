#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 28/Apr/2014 13:17

from __future__ import absolute_import

import os
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
_parent_path = os.path.split(ROOT_PATH)[0]

for folder in ('../lib', './backend/app'):
    folder_path = os.path.abspath(os.path.join(_parent_path, folder))
    if os.path.isdir(folder_path):
        sys.path.insert(0, folder_path)


# Celery Configuration

from celery import Celery
from celery.utils.log import get_task_logger

celery = Celery()
celery.config_from_object('tasks_settings')
logger = get_task_logger(__name__)


# DataBase Configuration

import copy
import smtplib
import datetime
import settings
from bson.objectid import ObjectId
from com.feedback.core.exceptions import ConfigurationError
from com.feedback.models.audits import Audit, Logs
from cStringIO import StringIO
from email import Charset
from email.generator import Generator
from email.header import Header
from email.mime.text import MIMEText
from mongoengine import register_connection
from pymongo import MongoClient, MongoReplicaSetClient
from pymongo.database import Database
from pymongo.common import validate


_database_cache = {}


for mek, mev in settings.DATABASE.items():
    medb = copy.deepcopy(mev)
    register_connection(
        alias=mek,
        name=medb.get('name'),
        username=medb.get('username'),
        password=medb.get('password'),
        **medb.get('settings', {})
    )


def get_database(name='default'):
    if name not in settings.DATABASE:
        raise ConfigurationError('Database %s not supported' % name)
    elif name not in _database_cache:
        config = copy.deepcopy(settings.DATABASE[name])
        db_name = config.get('name', 'test')
        db_settings = config.get('settings', {})
        for key, value in db_settings.items():
            try:
                validate(key, value)
            except Exception:
                if key not in ('hosts_or_uri', 'host', 'port', 'max_pool_size'):
                    del db_settings[key]
        if 'replicaset' not in db_settings:
            client = MongoClient(**db_settings)
        else:
            client = MongoReplicaSetClient(**db_settings)
        database = Database(client, db_name)
        db_username = config.get('username', False)
        db_password = config.get('password', False)
        if db_username and db_password:
            database.authenticate(db_username, db_password)
        _database_cache[name] = database
    return _database_cache[name]


def set_logiclow(value):
    if not isinstance(value, dict):
        raise TypeError('Invalid type, must be a dictionary.')
    query = dict(
        enabled=True,
        available=True,
        created=datetime.datetime.utcnow(),
        modified=datetime.datetime.utcnow(),
    )
    query.update(value)
    return query


def sync_send_mail(**kwargs):
    email_cfg = settings.EMAIL
    server = smtplib.SMTP(email_cfg.get('host'), email_cfg.get('port'))
    server.set_debuglevel(0)
    server.starttls()
    server.login(email_cfg.get('username'), email_cfg.get('password'))
    from_address = \
        kwargs.get('e_from', False) \
        or 'Feedback by Figment. <%s>' % email_cfg.get('email')
    to_address = kwargs.get('e_to', [])
    if isinstance(to_address, basestring):
        to_address = [to_address]
    elif not isinstance(to_address, (tuple, list,)):
        raise ValueError('Must be a tuple or list instance.')
    elif not to_address:
        raise ValueError('Email(s) not found.')
    Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')
    msg = MIMEText(kwargs.get('body'), 'plain', 'UTF-8')
    msg['Subject'] = Header(kwargs.get('subject'), 'utf-8')
    msg['From'] = Header(from_address, 'utf-8')
    msg['To'] = ', '.join(to_address)
    sio = StringIO()
    g = Generator(sio, False)
    g.flatten(msg)
    server.sendmail(from_address, to_address, sio.getvalue())
    logger.debug(
        'sync_send_mail -> %s %s' % (kwargs.get('subject'), to_address)
    )


# Tasks Configuration

@celery.task(ignore_result=True)
def push__audits(**kwargs):
    try:
        obj = Audit(enabled=True, available=True)
        obj.activity = kwargs.get('activity')
        obj.message = kwargs.get('message')
        obj.session = kwargs.get('session')
        obj.user = kwargs.get('user')
        obj.remote_ip = kwargs.get('remote_ip')
        obj.save(write_concern={'w': 0, 'j': False, 'fsync': False})
        logger.debug('push__audits -> %s' % obj.to_json())
        return True
    except Exception as e:
        logger.error('push__audits -> %s' % e.message.encode('utf-8'))


@celery.task(ignore_result=True)
def push__logs(**kwargs):
    try:
        obj = Logs(enabled=True, available=True)
        obj.activity = kwargs.get('activity')
        obj.message = kwargs.get('message')
        obj.session = kwargs.get('session')
        obj.user = kwargs.get('user')
        obj.remote_ip = kwargs.get('remote_ip')
        obj.save(write_concern={'w': 0, 'j': False, 'fsync': False})
        logger.debug('push__logs -> %s' % obj.to_json())
        return True
    except Exception as e:
        logger.error('push__logs -> %s' % e.message.encode('utf-8'))


@celery.task(ignore_result=True)
def push__notifications(e_to, subject, body, e_from=None, **kwargs):
    try:
        if isinstance(e_to, basestring):
            e_to = [e_to]
        elif not isinstance(e_to, (tuple, list,)):
            raise ValueError('Email list, not supported.')
        recordset = get_database().users.find({
            '_id': {'$in': [ObjectId(item) for item in e_to]}, 
            'enabled': True,
            'available': True
        }, {'email': 1})
        if not recordset:
            raise ValueError('Emails list, is empty.')
        emails = [item.get('email') for item in recordset if 'email' in item]
        sync_send_mail(
            e_from=e_from, e_to=emails, subject=subject, body=body, **kwargs)
        logger.debug('push__notifications -> %s' % emails)
        return True
    except Exception as e:
        logger.error('push__notifications -> %s' % e.message.encode('utf-8'))


@celery.task(ignore_result=True)
def push__client_notification(e_to, subject, body, e_from=None, **kwargs):
    try:
        if not isinstance(e_to, basestring):
            raise ValueError('Invalid email, must be a basestring.')
        sync_send_mail(
            e_from=e_from, e_to=e_to, subject=subject, body=body, **kwargs)
        logger.debug('push__client_notification -> %s' % e_to)
        return True
    except Exception as e:
        logger.error(
            'push__client_notification -> %s' % e.message.encode('utf-8')
        )


@celery.task(ignore_result=True)
def push__delete_obsolete_data(**kwargs):
    try:
        _id = kwargs.get('_id', False)
        if not _id:
            raise ValueError('Client not found.')
        elif not isinstance(_id, basestring):
            _id = ObjectId(_id)
        bulk = get_database().evaluations_pending.initialize_unordered_bulk_op()
        bulk.find({'_id': _id}).remove_one()
        bulk.execute()
        logger.debug('push__delete_obsolete_data -> %s' % _id)
        return True
    except Exception as e:
        logger.error(
            'push__delete_obsolete_data -> %s' % e.message.encode('utf-8')
        )


@celery.task(ignore_result=True)
def push__unavailable_obsolete_data(**kwargs):
    try:
        client = kwargs.get('client', False)
        if not client:
            raise ValueError('Client not found.')
        bulk = get_database().evaluations.initialize_ordered_bulk_op()
        bulk.find({
            'client': client,
            'available': True
        }).update(
            {'$set': {'available': False}}
        )
        bulk.execute()
        logger.debug('push__unavailable_obsolete_data -> %s' % client)
        return True
    except Exception as e:
        logger.error(
            'push__unavailable_obsolete_data -> %s' % e.message.encode('utf-8')
        )


# Initialize

if __name__ == '__main__':
    celery.start()