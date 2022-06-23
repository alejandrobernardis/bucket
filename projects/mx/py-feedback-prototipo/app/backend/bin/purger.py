# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 05/Jun/2014 15:48

import os
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

for folder in ('../app', '../../tasks', '../../../lib',):
    folder_path = os.path.abspath(os.path.join(ROOT_PATH, folder))
    if os.path.isdir(folder_path):
        sys.path.insert(0, folder_path)

import copy
import json
import logging
import settings
import datetime
from com.feedback.core.exceptions import ConfigurationError
from optparse import OptionParser
from pymongo.bulk import BulkWriteError
from pymongo.common import validate
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from pymongo.mongo_replica_set_client import MongoReplicaSetClient


# ------------------------------------------------------------------------------
logger_name = 'feedback_purger'
logger_level = logging.INFO
logger_format = logging.Formatter('[%(asctime)s|%(levelname)s]: %(message)s')
logger = logging.getLogger(logger_name)
logger.setLevel(logger_level)
logger_file = logging.FileHandler('/tmp/%s.log' % logger_name)
logger_file.setLevel(logger_level)
logger_file.setFormatter(logger_format)
logger.addHandler(logger_file)


# ------------------------------------------------------------------------------
_database_cache = {}
opts = None
args = None


# ------------------------------------------------------------------------------
def database(name='default'):
    try:
        global _database_cache
        if name not in _database_cache:
            database_list = settings.DATABASE
            if name not in database_list:
                raise ConfigurationError('Database not supported: %s' % name)
            configuration = copy.deepcopy(database_list[name])
            config = copy.deepcopy(configuration.get('settings'))
            if not config:
                raise ConfigurationError(
                    'Database config not supported: %s' % name)
            db_host_or_uri = config.get('host_or_uri')
            for key, value in config.items():
                try:
                    validate(key, value)
                except Exception:
                    del config[key]
            if db_host_or_uri and config.get('replicaset'):
                client = MongoReplicaSetClient(db_host_or_uri, **config)
            else:
                db_host = config.get('host', 'localhost')
                db_port = config.get('port', 27017)
                client = MongoClient(db_host, db_port, **config)
            db_user = configuration.get('username')
            db_pass = configuration.get('password')
            db = Database(client, configuration.get('name', 'test'))
            if db_user and db_pass:
                db.authenticate(db_user, db_pass, db)
            _database_cache[name] = db
            logger.info('Database connection create: %s' % name)
        else:
            logger.info('Database connection exist: %s' % name)
        return _database_cache[name]
    except Exception as e:
        from com.feedback.core.utils import trace_error
        trace_error(e)
        logger.error('DATABASE: %s' % e.message.encode('utf-8'))
        exit(1000)


# ------------------------------------------------------------------------------
def options_parser():
    parser = OptionParser()
    parser.add_option('-i', action='store_true', dest='ignore', default=False)
    parser.add_option('-v', action='store_true', dest='verbose', default=False)
    return parser.parse_args()


# ------------------------------------------------------------------------------
def run():
    global opts, args
    opts, args = options_parser()
    if opts.verbose:
        logger.setLevel(logging.DEBUG)
        logger_file.setLevel(logging.DEBUG)
        logger.debug('### DEBUGGER MODE ###')
    else:
        logger.info('### OPS ###')
    logger.debug('1. Initialize...')
    message = u'Desea eliminar los datos obsoletos? [Y/n] -> '.encode('utf-8')
    if not opts.ignore and raw_input(message) != 'Y':
        logger.warning('Cancel and not release the purger process.')
        exit(1)
    else:
        logger.info('Confirmation ignored.')
    logger.debug('2. Validation... OK')
    db = database()
    logger.debug('3. DataBase connect... OK')
    now = datetime.datetime.utcnow()  # + datetime.timedelta(days=20)
    logger.info('Process initializing.')
    bulk = db.evaluations_pending.initialize_ordered_bulk_op()
    bulk.find({'created': {'$lt': now}}).remove()
    try:
        bulk.execute()
        logger.debug('4. Bulk execute... OK')
    except BulkWriteError as e:
        logger.critical('Bulk remove failed: %s' % json.dumps(e.details))
        exit(100)
    except Exception as e:
        logger.critical('Bulk remove failed: %s' % e.message)
        exit(101)
    logger.info('Process finishing.')


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        run()
    except Exception as er:
        print ' - %s' % er.message.encode('utf-8')
    except KeyboardInterrupt:
        pass
