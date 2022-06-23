#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 10/Mar/2014 11:30

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
# import json
# from casino8.common.utils import str_complex_type
# from pycolorterm.pycolorterm import print_pretty, pretty_output, styles
from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from unicodecsv import UnicodeWriter

cnx = MongoClient('localhost')
dbC8 = Database(cnx, 'c8')
dbT8 = Database(cnx, 't8')
dt = datetime.datetime.utcnow()

file_name = os.path.abspath(
    os.path.join(
        ROOT_PATH, 'result/activity_report_%s.csv' % time.time()
    )
)

try:
    with open(file_name, 'wb') as file_output:
        writer = UnicodeWriter(file_output)
        writer.writerow((
            'sid', 'uid', 'fbuid', 'uid_fbuid', 'remote_ip', 'device',
            'created', 'activity', 'product_id', 'balance'
        ))

        buys = dbT8.activity.store.aggregate([
            {"$match": {
                "activity": "add_coins_success"
            }}, {"$group": {
                "_id": {"sid": "$sid", "activity": "$activity"},
                "total": {"$sum": 1}
            }}
        ])

        for item, buy in enumerate(buys.get('result')):
            sid = buy['_id']['sid']

            session = dbT8.activity.session.find_one({'sid': sid,
                                                      'activity': 'start'})

            uid = session.get('uid')
            fbuid = session.get('fbuid') or ''
            uid_fbuid = session.get('uid_fbuid') or ''
            balance = session.get('balance')
            device = session.get('device')
            remote_ip = session.get('remote_ip')

            row = (
                sid,
                uid,
                fbuid,
                uid_fbuid,
                remote_ip,
                device,
                session.get('track_created').isoformat(),
                'start_session',
                '',
                balance
            )

            store_session = list(dbT8.activity.store.find({
                'sid': sid
            }).sort('track_created', 1))

            store_session_len = len(store_session)
            store_session_data = store_session.pop(0)
            store_session_created = store_session_data.get('track_created')

            games_session = dbT8.activity.games.find({
                'sid': sid
            }).sort('track_created', 1)

            writer.writerow(row)
            print '\n$:', store_session_len, row

            for game in games_session:
                game_track_created = game.get('track_created')

                if store_session_data \
                        and store_session_created < game_track_created:
                    row = (
                        sid,
                        uid,
                        fbuid,
                        uid_fbuid,
                        remote_ip,
                        device,
                        store_session_created.isoformat(),
                        store_session_data.get('activity'),
                        store_session_data.get('product_id'),
                        store_session_data.get('balance')
                    )

                    writer.writerow(row)
                    print '>>> +', row

                    if len(store_session) > 0:
                        store_session_data = store_session.pop(0)
                        store_session_created = \
                            store_session_data.get('track_created')
                    else:
                        store_session_data = store_session_created = None

                row = (
                    sid,
                    uid,
                    fbuid,
                    uid_fbuid,
                    remote_ip,
                    device,
                    game_track_created.isoformat(),
                    game.get('activity'),
                    '',
                    game.get('balance')
                )

                writer.writerow(row)
                # print '==>', row

            if store_session_data:
                store_session.append(store_session_data)

            for store in store_session:
                row = (
                    sid,
                    uid,
                    fbuid,
                    uid_fbuid,
                    remote_ip,
                    device,
                    store.get('track_created').isoformat(),
                    store.get('activity'),
                    store.get('product_id'),
                    store.get('balance')
                )

                writer.writerow(row)
                print '>>> *', row

except Exception as e:
    print traceback.format_exc()
    print e.message