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
from urllib2 import urlopen, Request
from casino8.common.utils import str_complex_type


cmd = 'add_coins'
iron_man = 'I028005008006011105005122002116002068117024012119004003024006111' \
           '0030060290760930850680900440870810390530470860450250860820760580' \
           '06122090023095010096|B7878F5B-D38D-6F69-3A51-01403B82FFF8'


# --- HELPERS ------------------------------------------------------------------

def get_request(action='', **kwargs):
    if not kwargs:
        kwargs = {}
    kwargs.update(cmd=cmd, i=iron_man)
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


def main():
    receipt = '{"signature" = "AkhBYOFHfTWR3Nf20OwaeCAHwg4afEY1mDofb/U61cJ0j9ryFv1jVeiNroFHox7DYO/kDNgHzYU8bYoIZc5yozcUvpOkBfdqJY6CjeXplZBKHPmSnuv61di82SdUIEpvqgG8RQ4JHdjzdRC6x6Rj3ZhzkRPVF1L/eCJlEf25KmIKAAADVzCCA1MwggI7oAMCAQICCGUUkU3ZWAS1MA0GCSqGSIb3DQEBBQUAMH8xCzAJBgNVBAYTAlVTMRMwEQYDVQQKDApBcHBsZSBJbmMuMSYwJAYDVQQLDB1BcHBsZSBDZXJ0aWZpY2F0aW9uIEF1dGhvcml0eTEzMDEGA1UEAwwqQXBwbGUgaVR1bmVzIFN0b3JlIENlcnRpZmljYXRpb24gQXV0aG9yaXR5MB4XDTA5MDYxNTIyMDU1NloXDTE0MDYxNDIyMDU1NlowZDEjMCEGA1UEAwwaUHVyY2hhc2VSZWNlaXB0Q2VydGlmaWNhdGUxGzAZBgNVBAsMEkFwcGxlIGlUdW5lcyBTdG9yZTETMBEGA1UECgwKQXBwbGUgSW5jLjELMAkGA1UEBhMCVVMwgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAMrRjF2ct4IrSdiTChaI0g8pwv/cmHs8p/RwV/rt/91XKVhNl4XIBimKjQQNfgHsDs6yju++DrKJE7uKsphMddKYfFE5rGXsAdBEjBwRIxexTevx3HLEFGAt1moKx509dhxtiIdDgJv2YaVs49B0uJvNdy6SMqNNLHsDLzDS9oZHAgMBAAGjcjBwMAwGA1UdEwEB/wQCMAAwHwYDVR0jBBgwFoAUNh3o4p2C0gEYtTJrDtdDC5FYQzowDgYDVR0PAQH/BAQDAgeAMB0GA1UdDgQWBBSpg4PyGUjFPhJXCBTMzaN+mV8k9TAQBgoqhkiG92NkBgUBBAIFADANBgkqhkiG9w0BAQUFAAOCAQEAEaSbPjtmN4C/IB3QEpK32RxacCDXdVXAeVReS5FaZxc+t88pQP93BiAxvdW/3eTSMGY5FbeAYL3etqP5gm8wrFojX0ikyVRStQ+/AQ0KEjtqB07kLs9QUe8czR8UGfdM1EumV/UgvDd4NwNYxLQMg4WTQfgkQQVy8GXZwVHgbE/UC6Y7053pGXBk51NPM3woxhd3gSRLvXj+loHsStcTEqe9pBDpmG5+sk4tw+GK3GMeEN5/+e1QT9np/Kl1nj+aBw7C0xsy0bFnaAd1cSS6xdory/CUvM6gtKsmnOOdqTesbp0bs8sn6Wqs0C9dgcxRHuOMZ2tm8npLUm7argOSzQ=="; "purchase-info" = "ewoJIm9yaWdpbmFsLXB1cmNoYXNlLWRhdGUtcHN0IiA9ICIyMDEzLTA4LTI3IDEyOjIxOjM1IEFtZXJpY2EvTG9zX0FuZ2VsZXMiOwoJInVuaXF1ZS1pZGVudGlmaWVyIiA9ICJkNjY4OTMwZDU1YjFmOGQxMTJlZGNhZDE2ZTg1NGJmYjdjY2RmYTc3IjsKCSJvcmlnaW5hbC10cmFuc2FjdGlvbi1pZCIgPSAiMTAwMDAwMDA4NTMyNTE0MCI7CgkiYnZycyIgPSAiMS4wLjAiOwoJInRyYW5zYWN0aW9uLWlkIiA9ICIxMDAwMDAwMDg1MzI1MTQwIjsKCSJxdWFudGl0eSIgPSAiMSI7Cgkib3JpZ2luYWwtcHVyY2hhc2UtZGF0ZS1tcyIgPSAiMTM3NzYzMTI5NTg0NSI7CgkidW5pcXVlLXZlbmRvci1pZGVudGlmaWVyIiA9ICJDRUY0MkQ0Ri1GMjI2LTQ2NkYtQTk4NS00MEY2MzAzMjVDNTAiOwoJInByb2R1Y3QtaWQiID0gImNvbS5maWdtZW50LmRlc2Fycm9sbG8ubWlsbW9uZWRhcyI7CgkiaXRlbS1pZCIgPSAiNjkwMjM3OTI1IjsKCSJiaWQiID0gImNvbS5maWdtZW50LmRlc2Fycm9sbG8uZGVidWciOwoJInB1cmNoYXNlLWRhdGUtbXMiID0gIjEzNzc2MzEyOTU4NDUiOwoJInB1cmNoYXNlLWRhdGUiID0gIjIwMTMtMDgtMjcgMTk6MjE6MzUgRXRjL0dNVCI7CgkicHVyY2hhc2UtZGF0ZS1wc3QiID0gIjIwMTMtMDgtMjcgMTI6MjE6MzUgQW1lcmljYS9Mb3NfQW5nZWxlcyI7Cgkib3JpZ2luYWwtcHVyY2hhc2UtZGF0ZSIgPSAiMjAxMy0wOC0yNyAxOToyMTozNSBFdGMvR01UIjsKfQ=="; "environment" = "Sandbox"; "pod" = "100"; "signing-status" = "0";}'

    req = get_request(
        'do/coins/add',
        uid='0792e8a6d020ece0c0fe05184ee80616',
        sid='0792e8a6d020ece0c0fe05184ee80616',
        receipt=receipt,
        transaction_id='1000000085325140',
        product_id='com.figment.desarrollo.milmonedas',
        balance=200,
        coins='1,000',
    )

    data = urlopen(req)
    data = json.loads(data.read())
    print json.dumps(data, default=str_complex_type, indent=4)

if __name__ == '__main__':
    main()