#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 30/Jan/2014 11:38

import os
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

for folder in ('../app', '../lib',):
    folder_path = os.path.abspath(os.path.join(ROOT_PATH, folder))
    if os.path.isdir(folder_path):
        sys.path.insert(0, folder_path)

import settings
import unicodecsv
import datetime
from boogeyman.parser import get_connection, printer

TRUNCATE_CARD = "TRUNCATE card"
INSERT_CARD = "INSERT INTO card (" \
        "available, modified, created, enabled, number, type_id, status_id, " \
        "user_id" \
    ") VALUES (" \
        "1, %(date)s, %(date)s, 0, %(card)s, %(card_type)s, 2, 0);"


def get_card_type(file_name):
    try:
        return {
            'a': 1,
            'b': 2,
            'c': 3
        }[file_name[0].lower()]
    except Exception as e:
        print '(e) file: %s - error: %s' % (file_name, str(e))
        exit(1)


def run():
    n_cnx = get_connection(settings.DB_MX_COM_LUXURYONE)
    n_cursor = n_cnx.cursor()
    n_cursor.execute(TRUNCATE_CARD)
    base_path = os.path.join(settings.ASSETS_PATH, 'cards')
    for root, dirs, files in os.walk(base_path):
        for file_name in files:
            ext = os.path.splitext(file_name)[1][1:].strip().lower()
            if not ext in ('csv',):
                raise ValueError('Extension %s not supported.' % ext)
            header = None
            card_type = get_card_type(file_name)
            file_name = os.path.join(base_path, file_name)
            with open(file_name, 'r+') as input_file:
                rows = unicodecsv.UnicodeReader(input_file)
                for row in rows:
                    if not header:
                        header = row
                        continue
                    else:
                        card = row[0]
                        try:
                            n_cursor.execute(INSERT_CARD, {
                                'date': datetime.datetime.utcnow(),
                                'card': card.strip().replace('\t', ''),
                                'card_type': card_type
                            })
                            if not n_cursor.lastrowid:
                                raise ValueError('Card not created.')
                            printer('(i) ::: CARD(%s) ... ok' % card)
                        except Exception as e:
                            printer('(e) ::: CARD(%s): %s' % (card, str(e)))
                            printer('(q) ::: %s' % n_cursor.statement)
            n_cnx.commit()
    n_cursor.close()
    n_cnx.close()

if __name__ == '__main__':
    run()


