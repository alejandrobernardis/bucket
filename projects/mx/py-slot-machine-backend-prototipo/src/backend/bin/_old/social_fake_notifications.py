#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 30/Nov/2013 02:05


import os
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

for item in ('../app',):
    sys.path.insert(0, os.path.abspath(os.path.join(ROOT_PATH, item)))


import settings
import random
from datetime import datetime
from pymongo.connection import MongoClient
from pymongo.database import Database


def get_mongo_client(collection, database):
    client = MongoClient(
        host=settings.SOCIAL_DATABASE_HOST,
        port=settings.SOCIAL_DATABASE_PORT,
        max_pool_size=settings.SOCIAL_DATABASE_CONN,
        auto_start_request=settings.SOCIAL_DATABASE_AREQ,
        use_greenlets=settings.SOCIAL_DATABASE_UGLS
    )
    database = Database(client, database)
    database.authenticate(
        settings.SOCIAL_DATABASE_USER, settings.SOCIAL_DATABASE_PASS)
    return database[collection]


FBUID = "1469798294"
#FBUID = "100000163692553"


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
        for x in xrange(1, 4):
            query_insert = query.copy()
            query_insert["fbfriend"] = random.choice(
                ['885200371', '1161647266', '1336069122', '1469798294'])
            db.insert(query_insert, w=0, j=False)


if __name__ == '__main__':
    fakes()