#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 23/08/2013 07:46


import json
import string
import cPickle as pickle
from datetime import datetime
from hashlib import md5
from random import choice
from urllib import urlencode
from urllib2 import urlopen, Request, HTTPError
from casino8.common.utils import str_complex_type


cmd = 'device/config'
device = 'IPAD'

iron_man = 'I028005008006011105005122002116002068117024012119004003024006111' \
           '0030060290760930850680900440870810390530470860450250860820760580' \
           '06122090023095010096|B7878F5B-D38D-6F69-3A51-01403B82FFF8'

FB_DATA = (
    {"_id": "70f928d8e9682d720723012ee9764017",
     "fbuid": "26cae7718c32180a7a0f8e19d6d40a59"},
    {"_id": "e73382e4112e2e13156cd5866db22771",
    "fbuid": "26cae7718c32180a7a0f8e19d6d40a59"},
    {"_id": "576824177bf8eb1b18c45827771ffd82",
    "fbuid": "26cae7718c32180a7a0f8e19d6d40a59"},
    {"_id": "2447486ea436a712a127716a46418f6a",
    "fbuid": "26cae7718c32180a7a0f8e19d6d40a59"},
    {"_id": "aff9fa0a340bbfae004bcff0cbfc4bbd",
    "fbuid": "26cae7718c32180a7a0f8e19d6d40a59"},
    {"_id": "d073cc577bfcba317593c8618d186fb7",
    "fbuid": "26cae7718c32180a7a0f8e19d6d40a59"},
    {"_id": "6f62a1afaa022844ffd8aa4e626f61ff",
    "fbuid": "26cae7718c32180a7a0f8e19d6d40a59"},
    {"_id": "8e84444c47b8f0f960c47666c4f54828",
    "fbuid": "26cae7718c32180a7a0f8e19d6d40a59"},
    {"_id": "b8157a17d2fadb81243ffb2ad0de4b78",
    "fbuid": "26cae7718c32180a7a0f8e19d6d40a59"},
    {"_id": "7b5532779ba777195a71a7934d3bab73",
    "fbuid": "26cae7718c32180a7a0f8e19d6d40a59"},
)

DV_DATA = (
    {"_id": "8c3c722c37877727587725927a27739f"},
    {"_id": "0792e8a6d020ece0c0fe05184ee80616"},
    {"_id": "3c888c3c33a227d7d6743118271a804a"},
    {"_id": "08599e94e280f055e29a609c2eeeceb7"},
    {"_id": "103b3f23bf150ff70f2f3b0903703399"},
    {"_id": "c76946cbdc89684b4a665a1fc16b959b"},
    {"_id": "bcc4fec9e4be3ca225ebce9f4efcacec"},
    {"_id": "89a15db857aed951b97a95b7c8a9d8fe"},
    {"_id": "16e53a5cf96c72d53561f1d908a46f6a"},
    {"_id": "18eae778397ae3eb317b8847484e5088"},
)


# --- HELPERS ------------------------------------------------------------------

def get_request(action='', **kwargs):
    if not kwargs:
        kwargs = {}
    kwargs.update(cmd=cmd, device=device, i=iron_man)
    return Request('http://192.168.56.101/%s' % action, data=urlencode(kwargs))


def secret_key(length=32):
    h = '%s%s%s%s' % (
      datetime.utcnow().strftime('%Y%m%d%H%M%S%f'),
      string.letters,
      string.digits,
      string.punctuation)
    return ''.join([choice(h) for _ in range(length)])


def token(length=32, include_date=True):
    h = md5()
    h.update(secret_key(length))
    h = unicode(h.hexdigest())
    t = ''.join([choice(h) for _ in range(length)])
    if include_date and length > 16:
        d = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        t = d + '_' + t[0:length-(len(d)+1)]
    return t


# --- METHODS ------------------------------------------------------------------

def session_start_device_wo_fb():
    for x in DV_DATA:
        uid = x.get('_id')
        req = get_request('do/device/config', uid=uid)
        try:
            data = urlopen(req)
            if not data:
                raise ValueError('Data not found')
            data = json.loads(data.read())
            #print json.dumps(data, indent=4)
            print json.dumps(data)
            response = data.get('response', {})
            x['sid'] = response['profile']['sid']
            print json.dumps(data, default=str_complex_type)

        except HTTPError, E:
            print '[%s] %s' % (req.get_data(), E)

        except ValueError, E:
            print '[%s] %s' % (req.get_data(), E)


def session_verify_device_wo_fb():
    for x in DV_DATA:
        uid = x.get('_id')
        sid = x.get('sid')
        req = get_request('do/device/config', uid=uid, sid=sid)
        try:
            data = urlopen(req)
            if not data:
                raise ValueError('Data not found')
            data = json.loads(data.read())
            pickle.dump(data, open('dumps/%s.%s' % (uid, sid), 'wb'))
            print json.dumps(data, default=str_complex_type)
            # print json.dumps(data, default=str_complex_type, indent=4)

        except HTTPError, E:
            print '[%s] %s' % (req.get_data(), E)

        except ValueError, E:
            print '[%s] %s' % (req.get_data(), E)


def session_start_device_w_fb():
    for x in FB_DATA:
        uid = x.get('_id')
        fbuid = x.get('fbuid')
        req = get_request('do/device/config', uid=uid, fbuid=fbuid)
        try:
            data = urlopen(req)
            if not data:
                raise ValueError('Data not found')
            data = json.loads(data.read())
            response = data.get('response', {})
            x['sid'] = response['profile']['sid']
            print json.dumps(data, default=str_complex_type)

        except HTTPError, E:
            print '[%s] %s' % (req.get_data(), E)

        except ValueError, E:
            print '[%s] %s' % (req.get_data(), E)


def session_verify_device_w_fb():
    for x in FB_DATA:
        uid = x.get('_id')
        sid = x.get('sid')
        req = get_request('do/device/config', uid=uid, sid=sid)

        try:
            data = urlopen(req)
            if not data:
                raise ValueError('Data not found')
            data = json.loads(data.read())
            pickle.dump(data, open('dumps/%s.%s' % (uid, sid), 'wb'))
            print json.dumps(data, default=str_complex_type)
            # print json.dumps(data, default=str_complex_type, indent=4)

        except HTTPError, E:
            print '[%s] %s' % (req.get_data(), E)

        except ValueError, E:
            print '[%s] %s' % (req.get_data(), E)


def main():
    session_start_device_wo_fb()
    session_verify_device_wo_fb()
    session_start_device_w_fb()
    session_verify_device_w_fb()


if __name__ == '__main__':
    main()