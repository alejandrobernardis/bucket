#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 03/Mar/2014 12:51

import os
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

for folder in ('../../backend/lib', '../../backend/app',):
    folder_path = os.path.abspath(os.path.join(ROOT_PATH, folder))
    if os.path.isdir(folder_path):
        sys.path.insert(0, folder_path)

import time
import datetime
import traceback
from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from unicodecsv import UnicodeWriter

cnx = MongoClient('localhost')
dbC8 = Database(cnx, 'c8')
dbT8 = Database(cnx, 't8')
dt = datetime.datetime.utcnow()

file_name = os.path.abspath(
    os.path.join(
        ROOT_PATH, 'result/result_%s.csv' % time.time()
    )
)

# q = dbT8.activity.session.find({'activity': 'start'})
# try:
#     with open(file_name, 'wb') as file_output:
#         writer = UnicodeWriter(file_output)
#         writer.writerow((
#             'sid', 'uid', 'fbuid', 'iteration', 'spins_or_games', 'product',
#             'balance_before', 'balance_after', 'datetime'
#         ))
#
#         for item in q:
#             sid = item.get('sid')
#             uid = item.get('uid', '')
#             fid = item.get('fbuid', '')
#
#             iter_store = dbT8.activity.store.find(
#                 {'sid': sid, 'activity': {'$ne': 'add_coins_error'},
#                  'sandbox': False},
#                 {'track_created': 1, 'product_id': 1, 'balance': 1}
#             )
#
#             iter_store_count = iter_store.count()
#
#             if iter_store_count > 0:
#                 for i, buy in enumerate(iter_store):
#                     created = buy.get('track_created')
#                     activity_min = dbT8.activity.games.find(
#                         {'sid': sid, 'track_created': {'$lte': created}},
#                         {'activity': 1, 'balance_diff': 1, 'track_created': 1}
#                     ).sort('track_created', -1)
#
#                     activity_min_count = activity_min.count()
#
#                     if activity_min_count > 0:
#                         row = (
#                             sid, uid, fid, i+1,
#                             activity_min_count,
#                             buy.get('product_id'),
#                             activity_min[0].get('balance_diff'),
#                             buy.get('balance'),
#                             buy.get('track_created').isoformat()
#                         )
#                         writer.writerow(row)
#                         print row
#
# except Exception:
#     raise IOError('Can\'t save the file: %s' % file_name)

try:
    with open(file_name, 'wb') as file_output:
        writer = UnicodeWriter(file_output)
        writer.writerow((
            'iteration', 'start_seesion', 'sid', 'uid', 'fbuid', 'created',
            'product', 'sandbox', 'activity', 'spins', 'balance_before',
            'balance_after'
        ))

        buys = dbT8.activity.store.find({'activity': 'add_coins_success'}, {
            'sid': 1, 'uid': 1, 'fbuid': 1, 'product_id': 1,
            'balance': 1, 'track_created': 1, 'sandbox': 1
        })

        for i, buy in enumerate(buys):
            sid = buy.get('sid')
            uid = buy.get('uid')
            fbuid = buy.get('fbuid')
            created = buy.get('track_created')

            session_start = dbT8.activity.session.find_one({
                'sid': sid, 'activity': 'start'
            })

            session = dbT8.activity.games.find(
                {'sid': sid, 'track_created': {'$lte': created}},
                {'activity': 1, 'balance_diff': 1, 'track_created': 1}
            ).sort('track_created', -1)

            session_count = session.count()

            if session_count > 0:
                session = session[0]
            else:
                session = {
                    'activity': session_start.get('activity'),
                    'balance_diff': session_start.get('balance'),
                }

            row = (
                i+1, session_start.get('created'), sid, uid, fbuid, created,
                buy.get('product_id'), buy.get('sandbox') or '',
                session.get('activity'), session_count,
                session.get('balance_diff'), buy.get('balance')
            )
            print row
            writer.writerow(row)

except Exception as e:
    print traceback.format_exc()
    print e.message