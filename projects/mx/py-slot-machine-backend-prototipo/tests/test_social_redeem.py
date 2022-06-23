#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 26/09/2013 10:09

import os
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

for item in ('../src/backend/app',):
    sys.path.insert(0, os.path.abspath(os.path.join(ROOT_PATH, item)))


import json
import string
import settings
import random
from datetime import datetime
from hashlib import md5
from random import choice
from urllib import urlencode
from urllib2 import urlopen, Request
from casino8.common.utils import str_complex_type
from pymongo.connection import MongoClient
from pymongo.database import Database


device = 'IPAD'
iron_man = 'I028005008006011105005122002116002068117024012119004003024006111' \
           '0030060290760930850680900440870810390530470860450250860820760580' \
           '06122090023095010096|B7878F5B-D38D-6F69-3A51-01403B82FFF8'
DATABASE_HOST = u'localhost'

# --- HELPERS ------------------------------------------------------------------


def get_mongo_client(collection=None, database=None):
    client = MongoClient(
        replicaset=settings.DATABASE_RSET,
        host=DATABASE_HOST,
        port=settings.DATABASE_PORT,
        max_pool_size=settings.DATABASE_CONN,
        auto_start_request=settings.DATABASE_AREQ,
        use_greenlets=settings.DATABASE_UGLS
    )
    database = Database(client, database or settings.DATABASE_NAME)
    return database[collection]


def get_request(action='', **kwargs):
    if not kwargs:
        kwargs = {}
    kwargs.update(device=device, i=iron_man)
    return Request('http://localhost/%s' % action, data=urlencode(kwargs))


def secret_key(length=32):
    h = '%s%s%s%s' % (
        datetime.utcnow().strftime('%Y%m%d%H%M%S%f'),
        string.letters,
        string.digits,
        string.punctuation)
    return ''.join([choice(h) for _ in range(length)])


def token(length=32, include_date=True):
    h = md5()
    h.update(secret_key(length))
    h = unicode(h.hexdigest())
    t = ''.join([choice(h) for _ in range(length)])
    if include_date and length > 16:
        d = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        t = d + '_' + t[0:length-(len(d)+1)]
    return t


def printer(obj):
    print json.dumps(obj, indent=4, default=str_complex_type)


# --- METHODS ------------------------------------------------------------------

FBUID = "100000163692553"
FBUID_BASE = 1469798240
FACTOR = 11
DEVICES = []
NOTIFICATIONS = {}


def response(req):
    try:
        data = urlopen(req)
        if not data:
            raise ValueError('Data not found')
        return json.loads(data.read())
    except BaseException, E:
        print '[%s] %s' % (req.get_full_url(), E)
    return None


def get_devices_w_facebook():
    req = get_request('do/device/config', fbuid=FBUID)
    try:
        data = response(req)
        profile = data['response']['profile']
        DEVICES.append(profile)
        print profile

    except BaseException, E:
        print '[%s] %s' % (req.get_full_url(), E)

    print '='*80


def fakes():
    datetime_now = datetime.utcnow()

    query = {
        "fbfriend": 0,
        "fbuid": FBUID,
        "enabled": True,
        "available": True,
        "created": datetime_now,
        "modified": datetime_now,
        "value": 200
    }

    for y in ('send.gift', 'request.gift', 'share.bonus'):
        db = get_mongo_client(y, settings.DATABASE_NOTIFY_NAME)
        for x in xrange(1, 21):
            query_insert = query.copy()
            #query_insert["fbfriend"] = str(FBUID_BASE + x)
            query_insert["fbfriend"] = random.choice(
                ['885200371', '1161647266', '1336069122'])
            db.insert(query_insert, w=0, j=False)


def notifications():
    data = DEVICES[0]
    req = get_request(
        'do/notifications/list', fbuid=FBUID, sid=data.get('sid'), uid=data.get('uid'))
    try:
        data = response(req)
        NOTIFICATIONS.update(data['response'])
        print data

    except BaseException, E:
        print '[%s] %s' % (req.get_full_url(), E)


def redeem():
    session = DEVICES[0]
    handler = 'do/redeem/{}/'
    for k, v in NOTIFICATIONS.items():
        url = handler.format(k.replace('_', '/'))
        for x in v:
            req = get_request(
                url, uid=session.get('uid'), sid=session.get('sid'),
                nid=x.get('_id'), fbfriend=x.get('fbfriend')
            )
            data = response(req)
            try:
                print data['response']['profile']['balance']
            except BaseException:
                print k, 'x'


def main():
    #get_devices_w_facebook()
    fakes()
    #notifications()
    #redeem()


if __name__ == '__main__':
    main()