#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 29/08/2013 08:13

from __future__ import absolute_import

import os
import sys
import settings
import datetime

_parent_path = os.path.split(settings.ROOT_PATH)[0]

for item in ('bin', 'lib',):
    sys.path.insert(0, os.path.join(_parent_path, item))

from celery import Celery
from celery.utils.log import get_task_logger
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.mongo_replica_set_client import MongoReplicaSetClient
from pymongo.database import Database


celery = Celery()
celery.config_from_object('celery_settings')
logger = get_task_logger(__name__)


def get_mongo_replica_set_client(collection=None, database=None):
    client = MongoReplicaSetClient(
        hosts_or_uri=settings.DATABASE_HURI,
        replicaset=settings.DATABASE_RSET,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        max_pool_size=settings.DATABASE_CONN,
        auto_start_request=settings.DATABASE_AREQ,
        use_greenlets=settings.DATABASE_UGLS
    )
    database = Database(client, database or settings.DATABASE_NAME)
    database.authenticate(settings.DATABASE_USER, settings.DATABASE_PASS)
    return database[collection]


def get_mongo_client_social(collection=None, database=None):
    client = MongoClient(
        host=settings.SOCIAL_DATABASE_HOST,
        port=settings.SOCIAL_DATABASE_PORT,
        max_pool_size=settings.SOCIAL_DATABASE_CONN,
        auto_start_request=settings.SOCIAL_DATABASE_AREQ,
        use_greenlets=settings.SOCIAL_DATABASE_UGLS
    )
    database = Database(client, database or 'test')
    database.authenticate(
        settings.SOCIAL_DATABASE_USER, settings.SOCIAL_DATABASE_PASS)
    return database[collection]


def get_mongo_client_track(collection=None, database=None):
    client = MongoClient(
        host=settings.TRACK_DATABASE_HOST,
        port=settings.TRACK_DATABASE_PORT,
        max_pool_size=settings.TRACK_DATABASE_CONN,
        auto_start_request=settings.TRACK_DATABASE_AREQ,
        use_greenlets=settings.TRACK_DATABASE_UGLS
    )
    database = Database(client, database or 't8')
    database.authenticate(
        settings.TRACK_DATABASE_USER, settings.TRACK_DATABASE_PASS)
    return database[collection]


def set_logiclow_track(query):
    if not isinstance(query, dict):
        raise TypeError('Is not a dictionary!~')
    Q = dict(
        track_enabled=True,
        track_available=True,
        track_created=datetime.datetime.utcnow(),
        track_modified=datetime.datetime.utcnow(),
    )
    Q.update(query)
    return Q


def set_logiclow_default(query):
    if not isinstance(query, dict):
        raise TypeError('Is not a dictionary!~')
    Q = dict(
        enabled=True,
        available=True,
        created=datetime.datetime.utcnow(),
        modified=datetime.datetime.utcnow(),
    )
    Q.update(query)
    return Q


################################################################################
# ACTIVITY
################################################################################


@celery.task(ignore_result=True)
def push_game_activity(**query):
    try:
        get_mongo_client_track(
            'activity.games', settings.DATABASE_TRACK_NAME
        ).insert(set_logiclow_track(query), w=0, j=False)
    except Exception:
        pass


@celery.task(ignore_result=True)
def push_social_activity(**query):
    try:
        get_mongo_client_track(
            'activity.social', settings.DATABASE_TRACK_NAME
        ).insert(set_logiclow_track(query), w=0, j=False)
    except Exception:
        pass


@celery.task(ignore_result=True)
def push_session_activity(**query):
    try:
        get_mongo_client_track(
            'activity.session', settings.DATABASE_TRACK_NAME
        ).insert(set_logiclow_track(query), w=0, j=False)
        logger.info('activity.session: ok')
    except Exception as e:
        logger.info('activity.session: %s' % e)


@celery.task(ignore_result=True)
def push_store_activity(**query):
    try:
        get_mongo_client_track(
            'activity.store', settings.DATABASE_TRACK_NAME
        ).insert(set_logiclow_track(query), w=0, j=False)
    except Exception:
        pass


################################################################################
# SHARING
################################################################################


@celery.task(ignore_result=True)
def push_social_actions(action, query, fbuid=None):
    try:
        client = get_mongo_client_social(action, settings.DATABASE_SOCIAL_NAME)
        if not fbuid:
            client.insert(set_logiclow_default(query))
        else:
            if isinstance(fbuid, basestring):
                fbuid = {'fbuid': fbuid}
            client.update(fbuid, query)
    except Exception:
        pass


################################################################################
# PROFILE
################################################################################


@celery.task(ignore_result=True)
def push_profile_update(fbuid, query):
    try:
        if isinstance(fbuid, basestring):
            fbuid = {'_id': fbuid}
        get_mongo_replica_set_client('profiles')\
            .update(fbuid, query, w=0, j=False)
    except Exception:
        pass


################################################################################
# NOTIFICATIONS
################################################################################


@celery.task(ignore_result=True)
def push_notification(**query):
    try:
        get_mongo_client_social(
            'notify.default', settings.DATABASE_NOTIFY_NAME
        ).insert(set_logiclow_track(query), w=0, j=False)
    except Exception:
        pass


################################################################################
# SOCIAL HELPERS
################################################################################


@celery.task(ignore_result=True)
def push_pull_notifications(action, fbuid, fbfriends, value=200, **kwargs):
    try:
        if not isinstance(fbfriends, (list, tuple)):
            return False
        client = get_mongo_client_social(action, settings.DATABASE_NOTIFY_NAME)
        for fbfriend in fbfriends:
            client.insert(set_logiclow_default(dict(
                fbuid=fbfriend, value=value, fbfriend=fbuid, **kwargs
            )), w=0, j=False)
    except Exception:
        pass


@celery.task(ignore_result=True)
def push_pull_notifications_set(action, recordset):
    try:
        if not isinstance(recordset, (list, tuple)):
            return False
        client = get_mongo_client_social(action, settings.DATABASE_NOTIFY_NAME)
        for record in recordset:
            client.insert(set_logiclow_default(record), w=0, j=False)
    except Exception:
        pass


@celery.task(ignore_result=True)
def delete_pull_notifications(action, query):
    try:
        client = get_mongo_client_social(action, settings.DATABASE_NOTIFY_NAME)
        client.remove(query, w=0, j=True, multi=True)
    except Exception:
        pass


@celery.task(ignore_result=True)
def delete_notification(action, notification):
    try:
        if not isinstance(notification, basestring):
            notification = ObjectId(notification)
        get_mongo_client_social(
            action, settings.DATABASE_NOTIFY_NAME
        ).remove({
            '_id': notification,
            'enabled': True,
            'available': True
        }, w=0, j=False)
    except Exception:
        pass


################################################################################


if __name__ == '__main__':
    celery.start()
