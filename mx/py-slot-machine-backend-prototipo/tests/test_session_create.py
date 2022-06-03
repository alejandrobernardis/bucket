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
    for x in xrange(1, 2):
        req = get_request('do/device/config')
        try:
            data = urlopen(req)
            if not data:
                raise ValueError('Data not found')
            data = json.loads(data.read())
            print json.dumps(data, indent=4)

        except HTTPError, E:
            print '[%s] %s' % (req.get_data(), E)

        except ValueError, E:
            print '[%s] %s' % (req.get_data(), E)


import time


def session_start_device_w_fb():
    for x in xrange(1000):
        req = get_request('do/device/config', fbuid=10+x)
        try:
            data = urlopen(req)
            if not data:
                raise ValueError('Data not found')
            data = json.loads(data.read())
            print x

        except HTTPError, E:
            print '[%s] %s' % (req.get_data(), E)

        except ValueError, E:
            print '[%s] %s' % (req.get_data(), E)

        time.sleep(.3)


def main():
    #session_start_device_wo_fb()
    session_start_device_w_fb()


if __name__ == '__main__':
    main()