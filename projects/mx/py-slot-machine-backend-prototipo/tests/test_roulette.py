#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 01/08/2013 23:37

import os
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

for item in ('../src/backend/app', '../src/backend/lib',):
    sys.path.insert(0, os.path.abspath(os.path.join(ROOT_PATH, item)))

import time
import json
from casino8.games.roulette import *


def main_bonus():
    pointer = 0
    balance = 0
    iterations = 10
    start = time.time()
    for l in xrange(1, 10):
        m = RouletteBonus()
        report = {}
        print u'\x1b[0;32m%s\x1b[0m' % (u'-'*80)
        print u'\x1b[0;32m# Level:\x1b[0m %s' % l
        print u'\x1b[0;32m%s\x1b[0m' % (u'-'*80)
        for i in xrange(iterations):
            m.spin(1, 1, balance, level=l)
            balance = m.total
            key = str(m.payment)
            try:
                report[key] += 1
            except Exception:
                report[key] = 1
            pointer += 1
            print u'\x1b[0;34m+ %s -> Payment:\x1b[0m $%s - %s' \
                  % (pointer, m.payment, m.positions)
        print u'\x1b[0;32m%s\x1b[0m' % (u'-'*80)
        print u'\x1b[0;32mReport:\x1b[0m'
        print u'\x1b[0;32m%s\x1b[0m' % (u'-'*80)
        print json.dumps(report, indent=4, sort_keys=True)
        print u'\x1b[0;32m%s\x1b[0m' % (u'-'*80)
    end = time.time()
    elapsed = end - start
    msg = u'\x1b[0;32m@ %d runs in %.4f seconds (%.2f per/sec)\x1b[0m\n'
    print u'\n'
    print msg % (iterations*10, elapsed, iterations*10/elapsed)
    print u'\n'*2


def main_slot():
    pointer = 0
    balance = 0
    iterations = 1000
    start = time.time()
    for f in (1, 1.5, 2,):
        m = RouletteSlot()
        for b in (.25, .50, .75, 1, 2, 5, 10, 2000):
            print u'\x1b[0;32m%s\x1b[0m' % (u'-'*80)
            print u'\x1b[0;32m# Bet (f:%s):\x1b[0m %s' % (f, b,)
            print u'\x1b[0;32m%s\x1b[0m' % (u'-'*80)
            report = {}
            for i in xrange(iterations):
                m.spin(1, 1, balance, bet=b, factor=f)
                balance = m.total
                key = str(m.payment)
                try:
                    report[key] += 1
                except Exception:
                    report[key] = 1
                pointer += 1
                #print u'\x1b[0;34m+ %s -> Payment:\x1b[0m $%s' \
                #      % (pointer, m.payment)
            print u'\x1b[0;32m%s\x1b[0m' % (u'-'*80)
            print u'\x1b[0;32mReport:\x1b[0m'
            print u'\x1b[0;32m%s\x1b[0m' % (u'-'*80)
            print json.dumps(report, indent=4, sort_keys=True)
            print m._positions
            print u'\x1b[0;32m%s\x1b[0m' % (u'-'*80)
    end = time.time()
    elapsed = end - start
    msg = u'\x1b[0;32m@ %d runs in %.4f seconds (%.2f per/sec)\x1b[0m\n'
    print u'\n'
    print msg % (iterations*10, elapsed, iterations*10/elapsed)
    print u'\n'*2


if __name__ == '__main__':
    main_bonus()
    # main_slot()
