#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 09/Dec/2013 22:05

import os
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

for item in ('../src/backend/app', '../src/backend/lib',):
    sys.path.insert(0, os.path.abspath(os.path.join(ROOT_PATH, item)))

try:
    import cPickle as pickle
except:
    import pickle


import json
import time
from urllib import urlencode
from urllib2 import urlopen, Request
from casino8.common.utils import str_complex_type
from casino8.security.iron_man import IronMan, SECRET_HASH
from casino8.security.base import token

domain = 'app.casino-8.net'
iron_man = 'I028005008006011105005122002116002068117024012119004003024006111' \
           '0030060290760930850680900440870810390530470860450250860820760580' \
           '06122090023095010096|B7878F5B-D38D-6F69-3A51-01403B82FFF8'
iron_man = 'I%s' % IronMan.doit(iron_man, SECRET_HASH)


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
    except BaseException, e:
        print '[%s] %s' % (req.get_full_url(), e)
    return None


def create_session(uid='', fbuid=''):
    data = response(
        get_request('do/device/config', uid=uid, fbuid=fbuid)
    )
    with open('./session.json', 'wb') as file_output:
        json.dump(data, file_output)
    return data


def destroy_session(uid='', fbuid='', sid=''):
    response(
        get_request('do/device/disconnect', uid=uid, fbuid=fbuid, sid=sid)
    )


def sync(uid='', fbuid='', sid=''):
    return response(
        get_request('do/device/sync', uid=uid, facebookid=fbuid, sid=sid)
    )


def spin(uid, sid, mid=100, bet=.25, lines=10, **kwargs):
    data = response(
        get_request(
            'do/spin',
            uid=uid,
            sid=sid,
            mid=mid,
            bet=bet,
            lines=lines,
            **kwargs
        )
    )
    if data:
        return data
    else:
        exit(1)


def game(uid, sid, **kwargs):
    data = response(
        get_request(
            'do/spin/game',
            uid=uid,
            sid=sid,
            **kwargs
        )
    )
    if data:
        return data
    else:
        exit(1)


#session = create_session()
#profile = session['response']['profile']

i = 1
error = 0

import logging
logger = logging.getLogger('lifecycle')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('output.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)
tok = token(8)

profile = {}
profile['uid'] = 'dc36383ebe23e37338d936f9d289273e'
profile['sid'] = '55e3d199-50a8-4e7a-b511-c2cbcbc69f6b'

while True:
    _data = spin(
        profile['uid'],
        profile['sid'],
        bet=.5, mid=108, lines=30)
    error = int(_data['error']['id'])

    if error != 0 or i == 501:
        break

    resp = _data['response']

    _info = resp['score_info']
    _lines = resp['win_lines']
    _game = _lines['is_game']
    balance = _info['balance']

    if _game:
        _game_resp = game(
            profile['uid'],
            profile['sid'])
        if _game_resp['error']['id'] == 0:
            balance = _game_resp['response']['balance']

    data_str = '%8s\t%6d\t%2d\t%4d\t%6d\t%9d\t%9d\t%5s\t%5s\t%4d\t%4d' % (
        tok, i, error, _info['level'], _info['value'], balance,
        _info['payment'], _game, _lines['free_spin'],
        _lines['number_of_free_spins'], len(_lines['id_line']),
    )

    print data_str
    logger.info(data_str)

    i += 1
    time.sleep(.2)
