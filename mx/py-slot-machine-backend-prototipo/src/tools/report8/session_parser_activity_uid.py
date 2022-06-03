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
from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from unicodecsv import UnicodeWriter

cnx = MongoClient('localhost')
dbC8 = Database(cnx, 'c8')
dbT8 = Database(cnx, 't8')
dt = datetime.datetime.utcnow()

file_name = os.path.abspath(
    os.path.join(
        ROOT_PATH, 'result/uid_activity_report_%s.csv' % time.time()
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
                "_id": {"uid": "$uid"},
                "total": {"$sum": 1}
            }}
        ])

        for buy in buys.get('result'):
            _id = buy.get('_id')
            uid = _id.get('uid')
            print uid

except Exception as e:
    print traceback.format_exc()
    print e.message