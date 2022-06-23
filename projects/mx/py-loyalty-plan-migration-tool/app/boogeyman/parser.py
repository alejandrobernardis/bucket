#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 30/Jan/2014 00:14


import os
import sys
import settings

_parent_path = os.path.split(settings.ROOT_PATH)[0]

for folder in ('bin', 'lib',):
    folder_path = os.path.abspath(os.path.join(_parent_path, folder))
    if os.path.isdir(folder_path):
        sys.path.insert(0, folder_path)

import re
import json
import inspect
import datetime
import hashlib
import math
from pycolorterm.pycolorterm import print_pretty, pretty_output, styles
from queries import USER_INSERT, USER_SELECT, USER_TRUNCATE, USER_POINTS, \
    USER_CARD, USER_CARD_ASSIGNED, USER_CARD_CLEAN, RECEIPT_TRUNCATE, \
    TRANSACTION_TRUNCATE, USER_BONUS, USER_TRANSACTION
from mysql.connector import Connect as MySQLConnector, Error as MySQLError
from mysql.connector.errorcode import ER_ACCESS_DENIED_ERROR, ER_BAD_DB_ERROR

o_cnx = None
n_cnx = None
ENABLED_USERS = []

e_rx = re.compile(r'^(\(e\)).+', re.I)
w_rx = re.compile(r'^(\(q\)).+', re.I)

file_name = os.path.join(
    settings.REPORT_PATH,
    'report_%s.log' % datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
)

file_output = open(file_name, 'w+')


def str_complex_type(value):
    if type(value) in (int, float, long, bool):
        return str(value)
    elif type(value) is unicode:
        return value.encode('utf-8')
    elif isinstance(value, datetime.date) \
        or isinstance(value, datetime.time) \
            or isinstance(value, datetime.datetime):
        return value.isoformat()
    return value


def exit_with_message(message, e_id=1):
    print json.dumps(message, indent=4, default=str_complex_type)
    exit(e_id)


def printer(message, save=False):
    if isinstance(message, unicode):
        message = message.encode('utf-8')
    if e_rx.search(message):
        with pretty_output(
                styles['BOLD'], styles['FG_WHITE'], styles['BG_RED']) as out:
            out.write(message)
        save = True
    elif w_rx.search(message):
        with pretty_output(
                styles['BOLD'], styles['FG_YELLOW']) as out:
            out.write(message)
        save = True
    elif settings.VERBOSE:
        value = message.replace('ok', '{FG_GREEN}ok{END}')\
            .replace('(i)', '{FG_BLUE}{BOLD}(i){END}')
        print_pretty('%s' % value)
    if save or not settings.VERBOSE:
        time_now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        file_output.write('[%s] %s\n' % (time_now, message.strip()))


def get_connection(database):
    if not isinstance(database, basestring):
        raise TypeError('Type invalid, must be a basestring')
    database = str(database).lower()
    if database not in settings.DATABASES:
        raise ValueError('Database "%s" is not supported.' % database)
    try:
        cnx = MySQLConnector(**settings.DATABASES[database])
    except MySQLError as error:
        if error.errno == ER_ACCESS_DENIED_ERROR:
            return exit_with_message(
                'Something is wrong with your user name or password.'
            )
        elif error.errno == ER_BAD_DB_ERROR:
            return exit_with_message('Database does not exists.')
        else:
            return exit_with_message(error)
    else:
        return cnx


class DefaultObject(object):
    def to_dict(self):
        result = dict()
        for key in dir(self):
            value = getattr(self, key)
            if not key.startswith('_') and not inspect.ismethod(value):
                result[key] = value
        return result


class User(DefaultObject):
    id = None
    username = None
    email = None
    email_alternative = None
    password = None
    firstname = None
    last_name = None
    mothers_maiden_name = None
    telephone = None
    mobile = None
    gender = None
    birthdate = None
    street = None
    exterior = None
    interior = None
    newsletter = 1
    email_balance = None
    terms_conditions = 1
    privacy_policy = 1
    recovery = None
    enabled = None
    available = 1
    created = None
    modified = None
    user_role_id = None
    neighborhood_id = 0
    reference_id = 0

    _real_username = 0

    def __init__(self, data):
        self.id = int(data[0])
        self._real_username = data[1]
        self.username = 'username_%s' % self.id
        self.password = data[2]
        self.firstname = data[3]
        self.last_name = data[4]
        self.mothers_maiden_name = data[5]
        self.email = data[6]
        self.email_alternative = data[6]
        self.telephone = str(data[7])
        self.gender = str(data[13]).lower()
        self.street = str(data[17])
        self.birthdate = datetime.date(1900, int(data[12]), int(data[11]))
        self.created = data[10]
        self.modified = datetime.datetime.utcnow()
        self.enabled = int(data[9])
        self.user_role_id = 3

    @property
    def real_username(self):
        return self._real_username

def calculate_card(points):
    if points and 6999 < points:
        return 3
    elif points and 999 < points < 7000:
        return 2
    else:
        return 1


def calculate_amount(points, level):
    if not points or points < 1:
        return 0
    if level == 2:
        factor = 3
    elif level == 3:
        factor = 4
    else:
        factor = 1
    return (points/factor)*50


def fix_points(points):
    if not points or points < 1:
        return 0
    return points


def _truncate():
    n_cursor = n_cnx.cursor()
    try:
        n_cursor.execute(USER_TRUNCATE)
        n_cursor.execute(RECEIPT_TRUNCATE)
        n_cursor.execute(TRANSACTION_TRUNCATE)
        printer('(i) ::: TRUNCATE(user, receipt, transaction, cards) ... ok')
    except Exception as e:
        printer('(e) ::: TRUNCATE(user, receipt, transaction) %s' % str(e))
        printer('(q) ::: %s' % n_cursor.statement)
    n_cnx.commit()
    n_cursor.close()


def _normalize_users():
    o_cursor = o_cnx.cursor()
    o_cursor.execute(USER_SELECT)
    n_cursor = n_cnx.cursor()
    for user in o_cursor:
        u = User(user)
        try:
            n_cursor.execute(USER_INSERT, u.to_dict())
            n_cursor.execute(USER_CARD_ASSIGNED, {'id': u.id, 'real_username': u.real_username})
            
            if u.enabled:
                ENABLED_USERS.append([u.id])
            # print u.real_username
            printer('(i) ::: INSERT(user) user: %s ... ok' % u.id)
        except Exception as e:
            printer('(e) ::: INSERT(user) user: %s - %s' % (u.id, str(e)))
            printer('(q) ::: %s' % n_cursor.statement)
            
    n_cnx.commit()
    o_cursor.close()
    n_cursor.close()
 

def _normalize_points_by_user():
    if not ENABLED_USERS:
        raise ValueError('Users not found.')
    o_cursor = o_cnx.cursor()
    for user in ENABLED_USERS:
        uid = user[0]
        try:
            o_cursor.execute(USER_POINTS, {'id': uid})
            points = o_cursor.fetchone()[0]
            user.append(fix_points(points))
            user.append(calculate_card(points))
            printer('(i) ::: SUM(points) user: %s level: %s ... ok'
                    % (uid, user[2]))
        except Exception as e:
            printer('(e) ::: SUM(points) user: %s - %s' % (uid, str(e)))
            printer('(q) ::: %s' % o_cursor.statement)
    o_cursor.close()


def _normalize_card_by_points_by_user():
    if not ENABLED_USERS:
        raise ValueError('Users not found.')
    n_cursor = n_cnx.cursor()
    for user in ENABLED_USERS:
        uid = user[0]
        card_type = user[2]
        try:
            n_cursor.execute(USER_CARD, (card_type,))
            card = n_cursor.fetchone()
            if not card[0]:
                raise ValueError('Card not available')
            user.append(card[0])
            # n_cursor.execute(USER_CARD_ASSIGNED, {
            #     'id': uid,
            #     'date': datetime.datetime.utcnow(),
            #     'card': card[0]
            # })
            # printer('(i) ::: UPDATE(card) user: %s card: %s ... ok'
            #         % (uid, card[1]))
        except Exception as e:
            printer('(e) ::: UPDATE(card) user: %s - %s' % (uid, str(e)))
            printer('(q) ::: %s' % n_cursor.statement)
    n_cnx.commit()
    n_cursor.close()


def _normalize_bonus_by_user():
    if not ENABLED_USERS:
        raise ValueError('Users not found.')
    n_cursor = n_cnx.cursor()
    bonus = 'bonus_2014_0001'
    date_now = datetime.datetime.utcnow()
    date_now = datetime.date(date_now.year, date_now.month, date_now.day)
    h = hashlib.sha1()
    h.update('%s$%s$%s' % (bonus, 0, date_now))
    encrypted = h.hexdigest()
    for user in ENABLED_USERS:
        uid = user[0]
        points = int(user[1])  # fix (points-redeem) / 50
        level = user[2]
        card = user[3]
        amount = calculate_amount(points, level)
        try:
            n_cursor.execute(USER_BONUS, {
                'amout': amount,
                'bonus': bonus,
                'date': date_now,
                'encrypted': encrypted,
            })
            receipt = n_cursor.lastrowid
            if not receipt:
                raise ValueError('Receipt not available')
            printer('(i) ::: UPDATE(receipt) user: %s amount: %s ... ok'
                    % (uid, amount))
            try:
                n_cursor.execute(USER_TRANSACTION, {
                    'id': uid,
                    'card': card,
                    'points': fix_points(points),
                    'date': date_now,
                    'receipt': receipt,
                })
                if not n_cursor.lastrowid:
                    raise ValueError('transaction not available')
                printer('(i) ::: UPDATE(transaction) user: %s ... ok' % uid)
            except Exception as e:
                printer('(e) ::: UPDATE(transaction) user: %s - %s'
                        % (uid, str(e)))
                printer('(q) ::: %s' % n_cursor.statement)
        except Exception as e:
            printer('(e) ::: UPDATE(receipt) user: %s - %s' % (uid, str(e)))
            printer('(q) ::: %s' % n_cursor.statement)
    n_cnx.commit()
    n_cursor.close()


def run():
    global o_cnx, n_cnx
    o_cnx = get_connection(settings.DB_MX_COM_LUXURYHALLREWARDS)
    n_cnx = get_connection(settings.DB_MX_COM_LUXURYONE)
    _truncate()
    _normalize_users()
    _normalize_points_by_user()
    _normalize_card_by_points_by_user()
    _normalize_bonus_by_user()
    n_cnx.close()
    o_cnx.close()

if __name__ == '__main__':
    run()
