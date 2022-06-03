#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 24/Nov/2013 20:09

import datetime
from pymongo.database import Database
from pymongo.mongo_replica_set_client import MongoReplicaSetClient

# mongodb://c8admin:fgDB4dM1nC4s1N00ch0@

DATABASE_RSET = u'r0'
DATABASE_HURI = u'ip-172-31-38-71:27000,'\
                u'ip-172-31-38-71:27001,'\
                u'ip-172-31-38-71:27002,'\
                u'ip-172-31-38-71:27003'
DATABASE_HOST = u'ip-172-31-38-71'
DATABASE_PORT = 27000
DATABASE_CONN = 100
DATABASE_AREQ = True
DATABASE_UGLS = True
DATABASE_USER = 'c8admin'
DATABASE_PASS = 'fgDB4dM1nC4s1N00ch0'

c = MongoReplicaSetClient(
    hosts_or_uri=DATABASE_HURI,
    replicaset=DATABASE_RSET,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    max_pool_size=DATABASE_CONN,
    auto_start_request=DATABASE_AREQ,
    use_greenlets=DATABASE_UGLS
)

d = Database(c, 'c8')

try:
    d.authenticate(DATABASE_USER, DATABASE_PASS)

except Exception as e:
    print DATABASE_HURI
    print e

print 'done!'