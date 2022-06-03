# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 04/Jun/2014 11:28

import os
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

for folder in ('../app', '../../tasks', '../../../lib',):
    folder_path = os.path.abspath(os.path.join(ROOT_PATH, folder))
    if os.path.isdir(folder_path):
        sys.path.insert(0, folder_path)

import copy
import time
import math
import json
import emails
import base64
import logging
import settings
import datetime
from com.feedback.core.exceptions import ConfigurationError
from com.feedback.core.utils import SuperObject, mexico_time_zone, \
    secret_key, activation_key_b64
from com.feedback.security.password import SHA256PasswordHasher
from optparse import OptionParser
from pymongo.bulk import BulkWriteError
from pymongo.common import validate
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from pymongo.mongo_replica_set_client import MongoReplicaSetClient
from tasks import push__client_notification


# ------------------------------------------------------------------------------
logger_name = 'feedback_dispatcher'
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
dt_mexico = mexico_time_zone(datetime.datetime.utcnow())


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
    parser.add_option('--week', dest='week', default=-1, type='int')
    parser.add_option('--sleep-time', dest='sleep', default=1.0, type='float')
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
    message = u'Desea realizar el envío? [Y/n] -> '.encode('utf-8')
    if not opts.ignore and raw_input(message) != 'Y':
        logger.warning('Cancel and not release the massive dispatch.')
        exit(1)
    else:
        logger.info('Confirmation ignored.')
    if opts.week not in (1, 2, 4):
        logger.error('Week not supported (1, 2 or 4): %s' % opts.week)
        exit(2)
    logger.debug('2. Validation... OK')
    db = database()
    logger.debug('3. DataBase connect... OK')
    rs_limit, rs_skip, rs_check = (600, 0, 0)
    rs_query = {
        'dispatch': opts.week, 
        'permissions.user': True, 
        'enabled': True, 
        'available': True
    }
    rs_count = db.users.find(rs_query).sort('_id', 1).count()
    rs_break = int(math.floor(rs_count/rs_limit))
    logger.info('Process initializing.')
    logger.info('Total: %s' % rs_count)
    logger.info('Iterations: %s, Data Set: %s' % (rs_break, rs_limit))
    now = datetime.datetime.utcnow()
    expires = now + datetime.timedelta(days=7)
    while True:
        recordset = db.users\
            .find(rs_query)\
            .sort('_id', 1)\
            .skip(int(math.floor(rs_skip*rs_limit)))\
            .limit(rs_limit)
        logger.info(' - Iteration: %s.' % rs_skip)
        bulk = db.evaluations_pending.initialize_unordered_bulk_op()
        bulk_emails = []
        for record in recordset:
            record = SuperObject(**record)
            if not record.email:
                continue
            evaluation = SuperObject()
            evaluation.username = record.username
            _token = secret_key()
            evaluation.token = _token
            evaluation.activation_key = \
                activation_key_b64(record.username, record.email)
            _password = SHA256PasswordHasher().make(_token)
            _separator = _password.find('$', 1)
            evaluation.public_key = \
                base64.encodestring(_password[_separator:]).replace('\n', '|')
            evaluation.public_key_method = _password[0:_separator]
            evaluation.public_key_expires = expires
            evaluation.private_key = secret_key(16)
            evaluation.enabled = True
            evaluation.available = True
            evaluation.created = now
            evaluation.modified = now
            bulk.insert(evaluation.todict())
            public = base64.b64encode(evaluation.public_key)
            user_email = '"%s %s" <%s>' \
                         % (record.first_name, record.last_name, record.email)
            bulk_emails.append((
                user_email,
                emails.NOTIFICATION_EVALUATION_SUBJECT,
                emails.NOTIFICATION_EVALUATION % {
                    'first_name': record.first_name.split(' ')[0],
                    'site_domain': settings.SITE_DOMAIN,
                    'activation_key': public,
                }
            ))
            logger.debug(
                '   - Item: %s %s' % (user_email, evaluation.activation_key))
            rs_check += 1
        try:
            bulk.execute()
            logger.debug('4. Bulk execute... OK')
        except BulkWriteError as e:
            logger.critical('Bulk remove failed: %s' % json.dumps(e.details))
            exit(100)
        except Exception:
            logger.critical('Bulk insert failed %s / %s.' % (rs_skip, rs_break))
            exit(101)
        else:
            logger.debug(' - Send emails.')
            for _to, _subject, _body in bulk_emails:
                push__client_notification.delay(_to, _subject, _body)
                logger.debug('   - %s' % _to)
        if rs_skip >= rs_break:
            break
        rs_skip += 1
        time.sleep(opts.sleep)
    if rs_check != rs_count:
        logger.error('Record Set Check %s -> %s.' % (rs_check, rs_count))
    logger.info('Process finishing.')


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        run()
    except Exception as er:
        print ' - %s' % er.message.encode('utf-8')
    except KeyboardInterrupt:
        pass
