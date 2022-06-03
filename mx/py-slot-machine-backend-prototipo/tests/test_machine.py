#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Figment
# Copyright (c) 2013 Kinetiq
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 23/06/2013 01:24

import os
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

for item in ('../src/backend/app', '../src/backend/lib',):
    sys.path.insert(0, os.path.abspath(os.path.join(ROOT_PATH, item)))


import time
import datetime
from casino8.machines.slots import Slot100

machines = (Slot100, )


def main():
    for Machine in machines:
        balance_org = 200
        balance_chg = 200
        balance_payment = 0
        balance_free_spins = 0
        balance_game = 0
        bet = .25
        bet_lines = 8
        free = False
        free_value = 0
        track = False
        rangev = 1
        start = time.time()
        i = 0
        m = None

        for i in xrange(rangev):
            m = Machine(user_level=0)

            try:
                balance_chg, bet, bet_lines = \
                    m.spin(1, '1', balance_chg, bet, bet_lines, free)

                balance_payment += m.payment
                balance_game += 1 if m.game else 0
                balance_free_spins += 1 if m.free_spins else 0

                print '\n'
                print '\x1b[0;35m%s\x1b[0m' % ('*'*80)
                print '\x1b[0;35m%s\x1b[0m' % datetime.datetime.now()
                print '\x1b[0;35m%s\x1b[0m' % ('*'*80)
                print '\x1b[0;34mBalance ($%s):\x1b[0m $%s' % \
                      (balance_chg, m.balance)
                print '\x1b[0;34mBet ($%s):\x1b[0m $%s' % (bet, m.bet)
                print '\x1b[0;34mBet Lines (x%s):\x1b[0m x%s' % \
                      (bet_lines, m.bet_lines)
                print '\x1b[0;34mLines:\x1b[0m %s' % m.lines
                print '\x1b[0;34mLines:\x1b[0m %s' % m._lines
                print '\x1b[0;34mPay Lines:\x1b[0m %s' % m.pay_lines
                print '\x1b[0;34mFree Spins (x%s):\x1b[0m %s' % \
                      (m.free_spins_value, m.free_spins)
                print '\x1b[0;34mGame (x%s):\x1b[0m %s' % \
                      (m.game_value, m.game)
                print '\x1b[0;32mPayment:\x1b[0m $%s' % m.payment

                if m.free_spins:
                    free_value += m.free_spins_value
                    free = True
                    print '\x1b[0;33mFree Spins:\x1b[0m x%s' % free_value
                elif free_value > 0:
                    free = True
                    free_value -= 1
                    print '\x1b[0;34mFree Spins:\x1b[0m x%s' % free_value
                else:
                    free = False

            except BaseException as E:
                print E
                break

        #end = time.time()
        #elapsed = end - start
        #msg = u'\x1b[0;32m@ %d runs in %.4f seconds (%.2f per/sec)\x1b[0m\n'
        #
        #print u'\n'
        #print u'\x1b[0;34m%s\x1b[0m' % (u'-'*80)
        #print u'\x1b[0;34mSLOT (%s):\x1b[0m' % m.FULL_NAME
        #print u'\x1b[0;34m%s\x1b[0m' % (u'-'*80)
        #print u'\x1b[0;33m+ Before.......:\x1b[0m $%s' % balance_org
        #print u'\x1b[0;33m+ After........:\x1b[0m $%s' % balance_chg
        #print u'\x1b[0;33m+ Payment......:\x1b[0m $%s' % balance_payment
        #print u'\x1b[0;33m+ Game.........:\x1b[0m x%s' % balance_game
        #print u'\x1b[0;33m+ Free Spins...:\x1b[0m x%s' % balance_free_spins
        #print u'\x1b[0;33m+ Iterations...:\x1b[0m x%s' % (i+1)
        #print u'\x1b[0;34m%s\x1b[0m' % ('-'*80)
        #print msg % (rangev, elapsed, rangev/elapsed)
        #print u'\n'

main()
