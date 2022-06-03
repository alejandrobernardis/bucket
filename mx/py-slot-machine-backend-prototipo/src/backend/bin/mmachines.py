#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 12/Jun/2014 12:31

import os
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

for folder in ('../app', '../../../lib',):
    folder_path = os.path.abspath(os.path.join(ROOT_PATH, folder))
    if os.path.isdir(folder_path):
        sys.path.insert(0, folder_path)

import time
import json
import logging
import settings
import traceback
from casino8.security.sessions import ClientFactory
from optparse import OptionParser


# ------------------------------------------------------------------------------
logger_name = 'casino8_machines'
logger_level = logging.INFO
logger_format = logging.Formatter('[%(asctime)s|%(levelname)s]: %(message)s')
logger = logging.getLogger(logger_name)
logger.setLevel(logger_level)
logger_file = logging.FileHandler('/tmp/%s.log' % logger_name)
logger_file.setLevel(logger_level)
logger_file.setFormatter(logger_format)
logger.addHandler(logger_file)


# ------------------------------------------------------------------------------
opts = None
args = None

MACHINE_PATH = os.path.abspath(
    os.path.join(ROOT_PATH, '../../public/static/data/machines')
)


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
    message = u'Desea borrar las máquinas? [Y/n] -> '.encode('utf-8')

    if not opts.ignore and raw_input(message) != 'Y':
        logger.warning('Cancel and not release the massive dispatch.')
        exit(1)
    else:
        logger.info('Confirmation ignored.')

    if not len(args) or not len(args[0]):
        logger.warning('Key not defined.')
        exit(2)
    logger.debug('2. Connect...')

    mc = ClientFactory.create(settings.SESSION)
    logger.debug('3. Sanitization...')

    def normalize(value):
        try:
            return int(str(value).strip().replace(' ', ''))
        except Exception:
            logger.critical('Invalid keys, must be a integer.')
            exit(3)

    keys = [normalize(item) for item in args]
    logger.debug('Machines: %s' % keys)
    logger.debug('4. Delete...')

    for mid in keys:
        machine_file = '{}/{}.json'.format(MACHINE_PATH, mid)

        try:
            with open(machine_file, 'r') as file_input:
                machine_data = json.load(file_input)
        except Exception as e:
            logger.critical('File: %s' % e)
            exit(3)

        if 'groups' not in machine_data:
            logger.critical('Groups is empty.')
            exit(4)

        # TODO: paginar la matriz para hacerlo más eficiente.

        machine_list = [
            'cfg-{}-factor-{}'.format(mid, group)
            for group in machine_data.get('groups', [])
        ]

        machine_list.append('cfg-{}'.format(mid))
        logger.debug('List: %s' % ', '.join(machine_list))

        mc.engine.delete_multi(machine_list)
        logger.info('Finish: %s' % mid)

        time.sleep(.5)

    logger.info('Process finishing.')


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        run()
    except Exception as er:
        logging.error(traceback.format_exc())
        print ' - %s' % er.message.encode('utf-8')
    except KeyboardInterrupt:
        pass




get(mid, lines, bet)