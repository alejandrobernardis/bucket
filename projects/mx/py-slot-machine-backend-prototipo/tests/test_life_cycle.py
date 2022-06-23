#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 26/Nov/2013 21:23

import os
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

for item in ('../src/backend/app',):
    sys.path.insert(0, os.path.abspath(os.path.join(ROOT_PATH, item)))

import json
import time
from urllib import urlencode
from urllib2 import urlopen, Request
from casino8.common.utils import str_complex_type
from casino8.security.iron_man import IronMan, SECRET_HASH

domain = 'app.casino-8.net'
iron_man = 'I028005008006011105005122002116002068117024012119004003024006111' \
           '0030060290760930850680900440870810390530470860450250860820760580' \
           '06122090023095010096|B7878F5B-D38D-6F69-3A51-01403B82FFF8'
iron_man = 'I%s' % IronMan.doit(iron_man, SECRET_HASH)


#: --

def printer(obj):
    print json.dumps(obj, indent=4, default=str_complex_type)


def get_request(action='', **kwargs):
    if not kwargs:
        kwargs = {}
    kwargs.update(device='IPAD', i=iron_man)
    return Request('http://%s/%s' % (domain, action), data=urlencode(kwargs))


def response(req):
    try:
        data = urlopen(req)
        if not data:
            raise ValueError('Data not found')
        return json.loads(data.read())
    except BaseException, E:
        print '[%s] %s' % (req.get_full_url(), E)
    return None


#: --

device_session = response(get_request(
    'do/device/config',
    fbuid='1469798294',
    #uid='1c9a9a08fa298f8c4e5ce97283dc1874'
))

if not device_session:
    exit('Not device session...')
else:
    device_session = device_session.get('response')
    printer(device_session)

profile = device_session['profile']
uid = profile.get('uid')
sid = profile.get('sid')
mid = 100
bet = 2
lines = 10

for i in xrange(200):
    spin = response(
        get_request('do/spin', uid=uid, sid=sid, mid=mid, bet=bet, lines=lines))
    if spin:
        value = spin['response']
        if not value:
            break
        info = value.get('score_info')
        print value.get('unlock'), info.get('level'), info.get('value')
    time.sleep(.2)