#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 19/09/2013 09:31

import json
import string
import time
from datetime import datetime
from hashlib import md5
from random import choice
from urllib import urlencode
from urllib2 import urlopen, Request, HTTPError


cmd = 'get_user_config'
device = 'IPAD'
iron_man = 'I028005008006011105005122002116002068117024012119004003024006111' \
           '0030060290760930850680900440870810390530470860450250860820760580' \
           '06122090023095010096|B7878F5B-D38D-6F69-3A51-01403B82FFF8'

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

FBUID = 1469798294
DB_DEVICES = []
FACTOR = 200


def get_devices_wo_facebook():
    for x in xrange(1, FACTOR):
        req = get_request('do/device/config')
        try:
            data = urlopen(req)
            if not data:
                raise ValueError('Data not found')
            data = json.loads(data.read())
            profile = data['response']['profile']
            DB_DEVICES.append(profile)
            print profile

        except HTTPError, E:
            print '[%s] %s' % (req.get_data(), E)

        except ValueError, E:
            print '[%s] %s' % (req.get_data(), E)

    print '*'*80


def get_devices_w_facebook():
    for x in xrange(1, FACTOR):
        req = get_request('do/device/config', fbuid=FBUID)
        try:
            data = urlopen(req)
            if not data:
                raise ValueError('Data not found')
            data = json.loads(data.read())
            profile = data['response']['profile']
            print profile

        except HTTPError, E:
            print '[%s] %s' % (req.get_data(), E)

        except ValueError, E:
            print '[%s] %s' % (req.get_data(), E)

    print '*'*80


def get_devices_sync():
    for x in DB_DEVICES:
        req = get_request(
            'do/device/sync', fbuid=FBUID, uid=x['uid'], sid=x['sid'])
        try:
            data = urlopen(req)
            if not data:
                raise ValueError('Data not found')
            data = json.loads(data.read())
            profile = data['response']['profile']
            print profile
            time.sleep(.8)

        except HTTPError, E:
            print '[%s] %s' % (req.get_data(), E)

        except ValueError, E:
            print '[%s] %s' % (req.get_data(), E)

    print '*'*80


def get_devices_sync_error():
    for x in DB_DEVICES:
        req = get_request(
            'do/device/sync', fbuid=FBUID, uid=x['uid'], sid=x['sid'])
        try:
            data = urlopen(req)
            if not data:
                raise ValueError('Data not found')
            data = json.loads(data.read())
            print data
            time.sleep(.8)

        except HTTPError, E:
            print '[%s] %s' % (req.get_data(), E)

        except ValueError, E:
            print '[%s] %s' % (req.get_data(), E)

    print '*'*80


def get_devices_sync_error_alt():
    for x in DB_DEVICES:
        req = get_request(
            'do/device/sync', fbuid=FBUID+1, uid=x['uid'], sid=x['sid'])
        try:
            data = urlopen(req)
            if not data:
                raise ValueError('Data not found')
            data = json.loads(data.read())
            print data
            time.sleep(.8)

        except HTTPError, E:
            print '[%s] %s' % (req.get_data(), E)

        except ValueError, E:
            print '[%s] %s' % (req.get_data(), E)

    print '*'*80

def main():
    get_devices_wo_facebook()
    # get_devices_w_facebook()
    get_devices_sync()
    get_devices_sync_error()
    get_devices_sync_error_alt()


if __name__ == '__main__':
    main()