#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 22/08/2013 08:17

import datetime
import dateutil.parser
import inspect
import random
import logging
import traceback
import json
import hashlib
from bson.objectid import ObjectId
from itertools import izip


def safe_str_cmp(a, b):
    if len(a) != len(b):
        return False
    result = 0
    for x, y in izip(a, b):
        result |= ord(x) ^ ord(y)
    return result == 0


def swallow_args(func):
    def decorator(arg, *unused_args):
        if not arg:
            return None
        return func(arg, *unused_args)
    return decorator


@swallow_args
def bool_to_str(arg):
    return str(arg).lower()


@swallow_args
def unicode_to_str(arg):
    return arg.encode('utf-8')


@swallow_args
def datetime_to_str(arg):
    return '%d-%02d-%02d %02d:%02d:%02d' %\
           (arg.year, arg.month, arg.day,
            arg.hour, arg.minute, arg.second)


@swallow_args
def datetimefull_to_str(arg):
    return '%d-%02d-%02d %02d:%02d:%02d.%06d' %\
           (arg.year, arg.month, arg.day,
            arg.hour, arg.minute, arg.second, arg.microsecond)


@swallow_args
def date_to_str(arg):
    return arg.strftime('%Y-%m-%d')


@swallow_args
def time_to_str(arg):
    return '%02d:%02d:%02d' %\
           (arg.hour, arg.minute, arg.second)


@swallow_args
def timefull_to_str(arg):
    return '%02d:%02d:%02d.%06d' %\
           (arg.hour, arg.minute, arg.second, arg.microsecond)


def _strptime(arg, strptime_format):
    split_arg = arg.split('.')
    datetime_obj = datetime.datetime.strptime(split_arg[0], strptime_format)
    if len(split_arg) == 2:
        datetime_obj = datetime_obj.replace(microsecond=int(split_arg[1]))
    return datetime_obj


def str_to_unicode(arg):
    return unicode(arg)


def str_to_date(arg):
    return _strptime(arg, '%Y-%m-%d').date()


def str_to_time(arg):
    return _strptime(arg, '%H:%M:%S').time()


def str_to_datetime(arg):
    return _strptime(arg, '%Y-%m-%d %H:%M:%S')


def week_range(value=None):
    if not value or not isinstance(value, datetime.date):
        value = datetime.date.today()
    value = datetime.datetime(value.year, value.month, value.day)
    year, week, dow = value.isocalendar()
    ws = value if dow == 7 else value - datetime.timedelta(dow)
    we = ws + datetime.timedelta(6)
    return ws, we


def datetime_parser(value, default=None):
    kwargs = {}
    if isinstance(value, datetime.date) \
            or isinstance(value, datetime.time) \
            or isinstance(value, datetime.datetime) \
            or isinstance(value, datetime.timedelta):
        return value
    elif isinstance(value, (tuple, list)):
        value = ' '.join([str(x) for x in value])
    elif isinstance(value, int):
        value = str(value)
    elif isinstance(value, dict):
        kwargs = value
        value = kwargs.pop('date')
    try:
        try:
            parsedate = dateutil.parser.parse(value, **kwargs)
        except ValueError:
            parsedate = dateutil.parser.parse(value, fuzzy=True, **kwargs)
        return parsedate
    except Exception:
        return default or datetime.datetime.utcnow()


def str_complex_type(value):
    if type(value) in (int, float, long, bool) or isinstance(value, ObjectId):
        return str(value)
    elif type(value) is unicode:
        return unicode_to_str(value)
    elif isinstance(value, datetime.date) \
        or isinstance(value, datetime.time) \
            or isinstance(value, datetime.datetime):
        return value.isoformat()
    return value


def str_to_int(value, key=None, default='0'):
    try:
        if isinstance(value, int):
            return value
        elif isinstance(value, dict):
            value = value.get(key, default)
        return int(value.replace(r',', '', 2))
    except Exception:
        return None


def get_plural(value, singular, plural, message=''):
    try:
        return plural if value > 1 else singular
    except Exception:
        return message


def get_str_plural(value, singular, plural, message='', template=u'%s %s'):
    return template % (value, get_plural(value, singular, plural, message))


def is_primitive(value):
    return type(value) in (
        complex,
        int,
        float,
        long,
        bool,
        str,
        basestring,
        unicode,
        tuple,
        list
    )


class ObjectToDict(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def todict(self):
        result = dict()
        for key in dir(self):
            value = getattr(self, key)
            if not key.startswith('_') and not inspect.ismethod(value):
                result[key] = value
        return result


def _approx_eq(v1, v2, tolerance):
    return abs(v1-v2) <= tolerance


def _whithin(low, value, high, tolerance):
    return (value > low or _approx_eq(low, value, tolerance)) \
        and (value < high or _approx_eq(high, value, tolerance))


def random_and_probability(probability, tolerance):
    acc = 0.0
    acc_list = [acc]
    for item in probability:
        acc += item
        acc_list.append(acc)
    interval = -1
    number = random.random()
    for item in xrange(len(acc_list)-1):
        if _whithin(acc_list[item], number, acc_list[item+1], tolerance):
            interval = item
            break
    return 0 if interval == -1 else interval


def trace(data):
    logging.error(traceback.format_exc())
    logging.error(json.dumps(data, default=str_complex_type, indent=2))


def hash_uid(uid, fbuid=None):
    if not fbuid:
        return uid
    else:
        h = hashlib.md5()
        h.update('%s-%s' % (uid, fbuid))
        return h.hexdigest()