#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 21/Dec/2013 18:42

import os
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

for folder in ('../app', '../lib',):
    sys.path.insert(0, os.path.abspath(os.path.join(ROOT_PATH, folder)))

import json
import base64
import urllib2
from casino8.common.utils import ObjectToDict

APPLE_URL_LIVE = 'https://buy.itunes.apple.com/verifyReceipt'
APPLE_URL_SANDBOX = 'https://sandbox.itunes.apple.com/verifyReceipt'

APPLE_ERROR = {
    21000: 'The App Store could not read the JSON object you provided.',
    21002: 'The data in the receipt-data property was malformed.',
    21003: 'The receipt could not be authenticated.',
    21004: 'The shared secret you provided does not match the shared secret '
           'on file for your account.',
    21005: 'The receipt server is not currently available.',
    21006: 'This receipt is valid but the subscription has expired. When this '
           'status code is returned to your server, the receipt data is also '
           'decoded and returned as part of the response.',
    21007: 'This receipt is a sandbox receipt, but it was sent to the '
           'production service for verification.',
    21008: 'This receipt is a production receipt, but it was sent to the '
           'sandbox service for verification.',
}


class VerifyReceipt(ObjectToDict):
    quantity = None
    product_id = None
    transaction_id = None
    purchase_date = None
    original_transaction_id = None
    original_purchase_date = None
    app_item_id = None
    version_external_identifier = None
    bid = None
    bvrs = None
    error = None


def verify_receipt(receipt, url=APPLE_URL_LIVE):
    if not url:
        url = APPLE_URL_SANDBOX

    request = urllib2.Request(url)
    request.data = json.dumps({'receipt-data': base64.b64encode(receipt)})
    request.add_header('Content-Type', 'text/Json; charset=utf-8')

    try:
        cnx = urllib2.urlopen(request)
        response = json.loads(cnx.read())
        status = response.get('status', None)

        if status and status in APPLE_ERROR:
            message = '(%s) %s' % (status, APPLE_ERROR.get(status))
            raise Exception(message)

        return response.get('receipt')

    except Exception, e:
        return {'error': {'id': 21000, 'message': e.message}}

signature = ''

verify = VerifyReceipt(**verify_receipt(signature))

if verify.error:
    raise ValueError(verify.error.get('message'))

elif not verify.product_id:
    raise ValueError('Product ID (x)')

elif not verify.transaction_id:
    raise ValueError('Receipt ID (x)')

