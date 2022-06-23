#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 01/08/2013 00:18

import settings
from celery_tasks import push_game_activity
from casino8.common.utils import random_and_probability
from casino8.games.configurations import ROULETTE_BONUS_MODE, \
    ROULETTE_SLOT_MODE, ROULETTE_BONUS_PROBABILITY, ROULETTE_SLOT_PROBABILITY, \
    ROULETTE_BONUS_TOLERANCE, ROULETTE_SLOT_TOLERANCE, ROULETTE_SLOT_PAYTABLE
from casino8.machines.configurations import DEVICE_LEVELS
from numpy.random import shuffle


class Roulette(object):
    def __init__(self):
        self._bet = 0
        self._factor = 0
        self._balance = 0.0
        self._payment = 0.0
        self._position = 0
        self._positions = None
        self._mode = None
        self.paytable = None
        self.tolerance = None
        self.probability = None

    @property
    def bet(self):
        return self._bet

    @property
    def factor(self):
        return self._factor

    @property
    def balance(self):
        return self._balance

    @property
    def total(self):
        return self.balance + self.payment

    @property
    def payment(self):
        return self._payment

    @property
    def position(self):
        return self._position

    @property
    def positions(self):
        return self._positions

    @property
    def mode(self):
        return self._mode

    def spin(self, uid, sid, balance, *args, **kwargs):
        raise NotImplementedError()

    def _track(self, uid, sid):
        try:
            if settings.TRACK:
                push_game_activity.delay(
                    uid=uid,
                    sid=sid,
                    activity='roulette',
                    bet=self.bet,
                    factor=self.factor,
                    payment=self.payment,
                    balance=self.balance,
                    total=self.total,
                    poistion=self.position,
                    mode=self.mode,
                )
        except Exception:
            pass


class RouletteBonus(Roulette):
    def __init__(self):
        super(RouletteBonus, self).__init__()
        self._mode = ROULETTE_BONUS_MODE
        self.tolerance = ROULETTE_BONUS_TOLERANCE
        self.probability = ROULETTE_BONUS_PROBABILITY

    def spin(self, uid, sid, balance, *args, **kwargs):
        if 'level' not in kwargs:
            raise KeyError('Argument not found (level)')
        try:
            award = DEVICE_LEVELS[kwargs.get('level', 1)-1][5]
        except BaseException:
            award = 1
        self._position = \
            random_and_probability(self.probability, self.tolerance)
        self._positions = [item * award for item in xrange(1, 11)]
        self._payment = self._positions[self._position]
        self._balance = balance
        self._track(uid, sid)
        shuffle(self._positions)
        for i, v in enumerate(self._positions):
            if v == self._payment:
                self._position = i
                break
        return self._position


class RouletteSlot(Roulette):
    def __init__(self):
        super(RouletteSlot, self).__init__()
        self._mode = ROULETTE_SLOT_MODE
        self.tolerance = ROULETTE_SLOT_TOLERANCE
        self.probability = ROULETTE_SLOT_PROBABILITY

    def spin(self, uid, sid, balance, *args, **kwargs):
        if 'factor' not in kwargs or 'bet' not in kwargs:
            raise KeyError('Argument not found (factor/bet)')
        self._bet = kwargs.get('bet', .25)
        self._factor = int(kwargs.get('factor', 1))
        cols = ROULETTE_SLOT_PAYTABLE[0]
        cols_len = len(cols)
        if self._factor > cols_len:
            self._factor = cols_len - 1
        elif self._factor > 0:
            self._factor -= 1
        else:
            self._factor = 0
        self._position = \
            random_and_probability(self.probability, self.tolerance)
        self._positions = \
            [self._bet * item[self._factor] for item in ROULETTE_SLOT_PAYTABLE]
        self._payment = self._positions[self._position]
        self._balance = balance
        self._track(uid, sid)
        return self._position
