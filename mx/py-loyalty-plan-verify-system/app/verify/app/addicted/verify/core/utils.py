#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 02/Dec/2013 16:48

import base64
import datetime
import dateutil.parser
import copy
import hashlib
import inspect
import json
import logging
import string
import sys
import traceback
import unicodedata
from unicodedata import normalize, category
from addicted.verify.core.exceptions import ConfigurationError
from itertools import izip
from random import choice


def random_password(length=8):
    h = '%s%s%s%s' % (
        string.ascii_letters, string.digits, "!@#$=+.-_",
        datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f'))
    return ''.join([choice(h) for _ in range(length)])


def secret_key(length=64):
    h = '%s-%s-%s-%s' % (
        datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f'),
        string.ascii_letters, string.digits, string.punctuation)
    return ''.join([choice(h) for _ in range(length)])


def secret_key_b64(length=64):
    return base64.b64encode(secret_key(length).encode())


def activation_key(username, email):
    h = hashlib.md5()
    h.update(('%s-%s-%s' % (username, email, secret_key())).encode())
    return h.hexdigest()


def activation_key_b64(username, email):
    return base64.b64encode(activation_key(username, email).encode())


def token(length=32, include_date=False):
    h = hashlib.md5()
    h.update(secret_key(length).encode())
    v = ''.join([choice(h.hexdigest()) for _ in range(length)])
    if include_date:
        d = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        v = v[0:length - len(d)] + d
    return v


def token_b64(length=32, include_date=False):
    return base64.b64encode(token(length, include_date).encode())


def user_token(username, length=32, include_date=False):
    h = hashlib.md5()
    h.update(('%s:%s' % (username, secret_key(length))).encode())
    v = ''.join([choice(h.hexdigest()) for _ in range(length)])
    if include_date:
        d = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        v = v[0:length - len(d)] + d
    return v


def user_token_b64(length=32, include_date=False):
    return base64.b64encode(user_token(length, include_date).encode())


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
    from bson.objectid import ObjectId
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


def get_plural(value, singular, plural, default=None):
    try:
        return plural if value > 1 else singular
    except Exception:
        return default or ''


def get_str_plural(value, singular, plural, message='', template=u'%s %s'):
    return template % (value, get_plural(value, singular, plural, message))


def is_primitive(value):
    return isinstance(value, (
        complex, int, float, long, bool, str, basestring, unicode, tuple, list,
    ))


def trace_error(data):
    logging.error(traceback.format_exc())
    if isinstance(data, (tuple, list, dict,)):
        logging.error(json.dumps(data, default=str_complex_type, indent=2))
    else:
        print data


def verify_settings(settings, values=None):
    result = dict()
    for key in values:
        if key not in settings:
            raise KeyError('Key not supported: %s' % key)
        value = settings[key]
        if isinstance(value, (list, tuple, dict, set,)):
            value = copy.deepcopy(value)
        result[key] = value
    return result


def purge_settings(settings, values=None):
    if not values:
        return settings
    result = dict()
    for key in settings:
        if key not in values:
            continue
        value = settings[key]
        if isinstance(value, (list, tuple, dict, set,)):
            value = copy.deepcopy(value)
        result[key] = value
    return result


class SuperObject(object):
    def __init__(self, **kwargs):
        from bson.objectid import ObjectId
        for key, value in kwargs.items():
            if isinstance(value, ObjectId):
                value = str(value)
            setattr(self, key, value)

    def todict(self):
        result = dict()
        for key in dir(self):
            value = getattr(self, key)
            if not key.startswith('_') and not inspect.ismethod(value):
                result[key] = value
        return result


def _resolve_name(name, package, level):
    if hasattr(package, 'rindex'):
        raise ValueError('Package not set to a string.')
    dot = len(package)
    for item in range(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError(
                'Attempted relative import beyond top-level package')
    return "%s.%s" % (package[:dot], name)


def import_module(name, package=None):
    if name.startswith('.'):
        if not package:
            raise TypeError(
                'Relative imports require the package argument')
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]


def import_by_path(dotted_path):
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise ConfigurationError(
            '%s doesn\'t look like a module path' % dotted_path)
    try:
        module = import_module(module_path)
    except ImportError, e:
        raise ConfigurationError(
            'Error importing module %s: %s' % (module_path, e))
    try:
        attr = getattr(module, class_name)
    except AttributeError:
        raise ConfigurationError(
            'Module "%s" does not define a "%s" attribute/class' % (
                module_path, class_name))
    return attr


# def remove_accents(value):
#     normalize = unicodedata.normalize('NFKD', value)
#     return ''.join([i for i in normalize if not unicodedata.combining(i)])

accents = (
    ('a', u'aàáâãäå'),
    ('e', u'eèéêë'),
    ('i', u'iìíîï'),
    ('o', u'oòóôõö'),
    ('u', u'uùúûü'),
    ('c', u'cç'),
    ('n', u'nñ'),
    ('y', u'yýÿ')
)


def strip_accents(value):
    return ''.join(c for c in normalize('NFD', value) if category(c) != 'Mn')


def hack_mongo_accents(value):
    if value:
        value = strip_accents(value)
        for k, v in accents:
            value = value.replace(k, '[%s]' % v)
    return value
