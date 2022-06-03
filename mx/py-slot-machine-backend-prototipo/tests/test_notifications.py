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


sid = 'bc813d52-8a17-4abb-9f0b-6ed608db84c1'
iron_man = 'I028005008006011105005122002116002068117024012119004003024006111' \
           '0030060290760930850680900440870810390530470860450250860820760580' \
           '06122090023095010096|B7878F5B-D38D-6F69-3A51-01403B82FFF8'

FB_DATA = (
    {"_id": "a3ae93b0b43db93ab368b6c18933e93b",
     "fbuid": "26cae7718c32180a7a0f8e19d6d40a59"},
)

FB_CHECK = []

# --- HELPERS ------------------------------------------------------------------


def get_request(action='', **kwargs):
    if not kwargs:
        kwargs = {}
    # kwargs.update(i=iron_man)
    return Request('http://64.207.147.105/%s' % action, data=urlencode(kwargs))
    #return Request('http://192.168.56.101/%s' % action, data=urlencode(kwargs))


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

def notifications_post():
    for x in FB_DATA:
        uid = x.get('_id')
        fbuid = x.get('fbuid')

        req = get_request(
            action='n/%s/%s' % (uid, sid),
            fbuid=fbuid,
            friend_uid='fbuid_friend',
            friend_fbuid='fbuid_fbuid',
            friend_name='fbuid_name',
            category='category',
            message='message',
            value=1000,
        )

        req.get_method = lambda: 'POST'

        try:

            for y in xrange(0, 10):
                data = urlopen(req)
                if not data:
                    raise ValueError('Data not found')
                data = json.loads(data.read())
                print json.dumps(data)

        except HTTPError, E:
            print 'POST:HTTP [%s] %s' % (req.get_full_url(), E)

        except ValueError, E:
            print 'POST:VALUE [%s] %s' % (req.get_full_url(), E)


def notifications_get():
    for x in FB_DATA:

        uid = x.get('_id')
        fbuid = x.get('fbuid')

        req = get_request(
            action='n/%s/%s' % (uid, sid),
            fbuid=fbuid,
        )

        req.get_method = lambda: 'GET'

        try:
            data = urlopen(req)
            if not data:
                raise ValueError('Data not found')
            data = json.loads(data.read())
            for y in data['response']:
                FB_CHECK.append(dict(
                    uid=uid,
                    fbuid=fbuid,
                    sid=sid,
                    nid=y['_id']['$oid']
                ))
                print json.dumps(data)

        except HTTPError, E:
            print 'GET:HTTP [%s] %s' % (req.get_full_url(), E)

        except ValueError, E:
            print 'GET:VALUE [%s] %s' % (req.get_full_url(), E)


def notifications_put():
    for x in FB_CHECK:
        _uid = x.get('uid')
        _sid = x.get('sid')
        _nid = x.get('nid')

        req = get_request(
            action='n/%s/%s/%s' % (_uid, _sid, _nid),
        )

        req.get_method = lambda: 'PUT'

        try:
            data = urlopen(req)
            if not data:
                raise ValueError('Data not found')
            data = json.loads(data.read())
            print json.dumps(data)

        except HTTPError, E:
            print 'PUT:HTTP [%s] %s' % (req.get_full_url(), E)

        except ValueError, E:
            print 'PUT:VALUE [%s] %s' % (req.get_full_url(), E)


def notifications_delete():
    for x in FB_CHECK:
        _uid = x.get('uid')
        _sid = x.get('sid')
        _nid = x.get('nid')

        req = get_request(
            action='n/%s/%s/%s' % (_uid, _sid, _nid),
        )

        req.get_method = lambda: 'DELETE'

        try:
            data = urlopen(req)
            if not data:
                raise ValueError('Data not found')
            data = json.loads(data.read())
            print json.dumps(data)

        except HTTPError, E:
            print 'DEL:HTTP [%s] %s' % (req.get_full_url(), E)

        except ValueError, E:
            print 'DEL:VALUE [%s] %s' % (req.get_full_url(), E)


def main():
    notifications_post()
    notifications_get()
    notifications_put()
    notifications_delete()


if __name__ == '__main__':
    main()