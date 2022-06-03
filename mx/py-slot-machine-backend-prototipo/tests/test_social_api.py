#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 26/09/2013 10:09

import json
import time
import string
from datetime import datetime
from hashlib import md5
from random import choice
from urllib import urlencode
from urllib2 import urlopen, Request
from casino8.common.utils import str_complex_type


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


def printer(obj):
    print json.dumps(obj, indent=4, default=str_complex_type)


# --- METHODS ------------------------------------------------------------------

FBUID = 1469798290
FACTOR = 2  # 11
DEVICES = []


def get_devices_w_facebook():
    for x in xrange(1, FACTOR):
        req = get_request('do/device/config', fbuid=FBUID + x)
        try:
            data = urlopen(req)
            if not data:
                raise ValueError('Data not found')
            data = json.loads(data.read())
            profile = data['response']['profile']
            DEVICES.append(profile)
            print '%2s - %s' % (x, profile.get('fbuid'))

        except BaseException, E:
            print '[%s] %s' % (req.get_full_url(), E)

    print '='*80


def response(req):
    try:
        data = urlopen(req)
        if not data:
            raise ValueError('Data not found')
        return json.loads(data.read())
    except BaseException, E:
        print '[%s] %s' % (req.get_full_url(), E)
    return None


def share_roulette():
    url_handler = 'do/share/bonus/'
    url_friends = 'do/share/bonus/friends/'
    FRIENDS_ONE = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
    FRIENDS_TWO = [100, 101, 102, 103, 104, 200, 201, 202, 203, 204]
    FRIENDS_THR = [205, 206, 207, 208, 209, 300, 301, 302, 303, 304]

    for device in DEVICES:
        uid = device.get('uid')
        sid = device.get('sid')
        balance = device.get('balance')
        friends_one = ','.join(map(str, FRIENDS_ONE))
        friends_two = ','.join(map(str, FRIENDS_TWO))
        friends_thr = ','.join(map(str, FRIENDS_THR))

        for y in (friends_one, friends_two, friends_thr):
            for x in xrange(0, 2):
                data = response(get_request(
                    url_friends,
                    uid=uid,
                    sid=sid,
                    friends=y,
                ))

                friends_list = data['response']['friends']
                print 'Friends: %s' % friends_list

                data = response(get_request(
                    url_handler,
                    uid=uid,
                    sid=sid,
                    balance=balance,
                    friends=y,
                ))

                print 'EID: %s' % data['error']['id']
                time.sleep(1)

            print '*'*80

        print '='*80


def send_gift():
    FRIENDS_ONE = [100, 101, 102, 103]
    FRIENDS_TWO = [100, 101, 102, 103, 104]
    FRIENDS_THR = [205, 206, 207, 208, 209]
    url_handler = 'do/send/gift/'
    url_friends = 'do/send/gift/balance/'

    for device in DEVICES:
        uid = device.get('uid')
        sid = device.get('sid')
        friends_one = ','.join(map(str, FRIENDS_ONE))
        friends_two = ','.join(map(str, FRIENDS_TWO))
        friends_thr = ','.join(map(str, FRIENDS_THR))

        for y in (friends_one, friends_two, friends_thr):
            for x in xrange(0, 2):
                data = response(get_request(
                    url_friends,
                    uid=uid,
                    sid=sid,
                    friends=y,
                ))

                friends_list = data['response']['friends']
                print 'Friends: %s' % friends_list

                data = response(get_request(
                    url_handler,
                    uid=uid,
                    sid=sid,
                    friends=y,
                ))

                print 'EID: %s' % data['error']['id']
                time.sleep(1)

            print '*'*80

        print '='*80


def request_gift():
    FRIENDS_ONE = [100, 101, 102, 103]
    FRIENDS_TWO = [100, 101, 102, 103, 104]
    FRIENDS_THR = [205, 206, 207, 208, 209]
    url_handler = 'do/request/gift/'
    url_friends = 'do/request/gift/balance/'

    for device in DEVICES:
        uid = device.get('uid')
        sid = device.get('sid')
        friends_one = ','.join(map(str, FRIENDS_ONE))
        friends_two = ','.join(map(str, FRIENDS_TWO))
        friends_thr = ','.join(map(str, FRIENDS_THR))

        for y in (friends_one, friends_two, friends_thr):
            for x in xrange(0, 2):
                data = response(get_request(
                    url_friends,
                    uid=uid,
                    sid=sid,
                    friends=y,
                ))

                friends_list = data['response']['friends']
                print 'Friends: %s' % friends_list

                data = response(get_request(
                    url_handler,
                    uid=uid,
                    sid=sid,
                    friends=y,
                ))

                print 'EID: %s' % data['error']['id']
                time.sleep(1)

            print '*'*80

        print '='*80


def invite():
    FRIENDS_ONE = [100, 101, 102, 103]
    FRIENDS_TWO = [100, 101, 102, 103, 104]
    FRIENDS_THR = [205, 206, 207, 208, 209]
    url_handler = 'do/invite/'
    url_friends = 'do/invite/balance/'

    for device in DEVICES:
        uid = device.get('uid')
        sid = device.get('sid')
        friends_one = ','.join(map(str, FRIENDS_ONE))
        friends_two = ','.join(map(str, FRIENDS_TWO))
        friends_thr = ','.join(map(str, FRIENDS_THR))

        for y in (friends_one, friends_two, friends_thr):
            for x in xrange(0, 2):
                data = response(get_request(
                    url_friends,
                    uid=uid,
                    sid=sid,
                    friends=y,
                ))

                friends_list = data['response']['friends']
                print 'Friends: %s' % friends_list

                data = response(get_request(
                    url_handler,
                    uid=uid,
                    sid=sid,
                    friends=y,
                ))

                print 'EID: %s' % data['error']['id']
                time.sleep(1)

            print '*'*80

        print '='*80


def main():
    get_devices_w_facebook()
    share_roulette()
    send_gift()
    request_gift()
    invite()


if __name__ == '__main__':
    main()