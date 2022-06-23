#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 02/Oct/2013 10:33

import os
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

for folder in ('../app', '../lib',):
    sys.path.insert(0, os.path.abspath(os.path.join(ROOT_PATH, folder)))

import json
import settings
from math import ceil
from pymongo.mongo_replica_set_client import MongoReplicaSetClient
from pymongo.database import Database


def get_mongo_client(collection=None, database=None):
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


def main():
    coll = get_mongo_client('profiles', settings.DATABASE_NAME)
    total = min(coll.count(), 10)
    page_size = 10
    page_total = min(int(ceil(total/float(page_size))), 10)

    coll.ensure_index([
        ('level', -1),
        ('points', -1),
        ('enabled', -1),
        ('available', -1)
    ])

    for page in xrange(page_total):
        page_number = page + 1

        query = {'enabled': True, 'available': True}

        values = {'level': 1, 'points': 1, 'balance': 1}

        records = coll.find(query, values) \
                      .sort([('level', -1), ('points', -1)]) \
                      .limit(page_size) \
                      .skip(page * page_size)

        records_value = [document for document in records]

        records_default = \
            [{"_id": "1469798294", "balance": 200.0, "points": 100, "level": 1}]

        data = dict(
            page_number=page_number,
            page_total=page_total,
            total=total,
            records=records_value or records_default
        )

        path = '%s/data/podium' % settings.STATIC_PATH

        if not os.path.isdir(path):
            os.makedirs(path, 0755)

        with open('%s/%s.json' % (path, page_number), 'w') as output:
            json.dump(data, output)


if __name__ == "__main__":
    main()