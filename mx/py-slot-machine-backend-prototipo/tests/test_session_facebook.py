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
from datetime import datetime
from hashlib import md5
from random import choice
from urllib import urlencode
from urllib2 import urlopen, Request, HTTPError


device = 'IPAD'

iron_man = 'I028005008006011105005122002116002068117024012119004003024006111' \
           '0030060290760930850680900440870810390530470860450250860820760580' \
           '06122090023095010096|B7878F5B-D38D-6F69-3A51-01403B82FFF8'


# --- HELPERS ------------------------------------------------------------------

def get_request(action='', **kwargs):
    if not kwargs:
        kwargs = {}
    kwargs.update(device=device, i=iron_man)
    #return Request('http://192.168.56.101/%s' % action, data=urlencode(kwargs))
    return Request('http://64.207.147.105/%s' % action, data=urlencode(kwargs))


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

def response(req):
    try:
        data = urlopen(req)
        if not data:
            raise ValueError('Data not found')
        return json.loads(data.read())
    except BaseException, E:
        print '[%s] %s' % (req.get_full_url(), E)
    return None


DEVICES_ID = []


def session_start_device_wo_fb():
    balance = 0
    for x in xrange(10):
        data = response(get_request('do/device/config'))
        DEVICES_ID.append(data['response']['profile'])
        balance += int(data['response']['profile']['balance'] or 0)
    assert balance == 200 * (x + 1)


def session_start_device_w_fb():
    balance = 0
    for x in DEVICES_ID:
        data = response(get_request(
            'do/device/sync',
            uid=x.get('uid'),
            sid=x.get('sid'),
            fbuid='123645'
        ))
        try:
            balance = int(data['response']['profile']['balance'] or 0)
        except:
            print data
    print balance


def session_start_device_verify():
    for x in DEVICES_ID:
        data = response(get_request(
            'do/device/verify',
            uid=x.get('uid'),
            sid=x.get('sid'),
            fbuid='123645'
        ))
        print data['error']


def main():
    session_start_device_wo_fb()
    session_start_device_w_fb()
    session_start_device_w_fb()
    session_start_device_verify()


if __name__ == '__main__':
    main()