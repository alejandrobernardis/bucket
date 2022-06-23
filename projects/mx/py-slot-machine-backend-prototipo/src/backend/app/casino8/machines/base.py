#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 21/06/2013 10:51

import json
import bisect
import settings
from array import array
from copy import deepcopy
from numpy.random import randint, shuffle
from celery_tasks import push_game_activity
from casino8.machines.configurations import WILDCARD_CHAR, GAME_CHAR, \
    GAME_VALIDATE, WILDCARD_VALIDATE, FREE_SPINS_CHAR, IGNORE_CHARS, \
    CHARACTERS, CHARACTERS_SUM, MPOS, MCOLS, DEFUALT_PAYTABLE_LINES, \
    DEFAULT_BETS, DEVICE_LEVELS, AI_SESSION_VALUES, AI_SESSION_REPLACEMENT


class AbstractMachine(object):
    mid = None
    name = None
    full_name = None
    hash_sum = None
    bets = None
    rails = None
    rails_levels = None
    rails_values = None
    max_lines = None
    paytable_lines = None
    paytable_chars = None
    mini_game = None

    def __init__(self, user_level=0):
        try:
            self._level = DEVICE_LEVELS[user_level - 1]
        except Exception:
            self._level = DEVICE_LEVELS[0]
        try:
            self.bets = DEFAULT_BETS[DEFAULT_BETS.index(self._level[3]):]
        except Exception:
            self.bets = DEFAULT_BETS[-5:]
        self.paytable_lines = DEFUALT_PAYTABLE_LINES[0:self.max_lines]
        try:
            if self.rails_levels:
                self._rails_index, self._rails_data = \
                    self._search_rails(user_level)
            else:
                raise ValueError()
        except:
            self._rails_index, self._rails_data = None, None
        self._balance = None
        self._bet = None
        self._bet_lines = None
        self._lines = None
        self._payment = None
        self._pay_lines = None
        self._pay_chars = None
        self._game = None
        self._balance = None
        self._free_spins = None

    def _search_rails(self, level):
        if level < 1:
            level = 1
        lo, hi = 0, len(self.rails_levels)
        while lo < hi:
            mid = (lo+hi)//2
            if self.rails_levels[mid][0] < level:
                lo = mid + 1
            else:
                hi = mid
        return lo, self.rails_values[lo]

    # Properties

    @property
    def balance(self):
        return self._balance or 0

    @property
    def bet(self):
        return self._bet or 0

    @property
    def bet_lines(self):
        return self._bet_lines or 0

    @property
    def lines(self):
        result = dict()
        y = 0
        for c in MPOS:
            if c != 0 and c % 5 == 0:
                y += 1
            if y not in result:
                result[y] = []
            result[y].append(CHARACTERS.find(self._lines[c:c+1])+1)
        return result or {}

    @property
    def payment(self):
        return self._payment or 0

    @property
    def pay_lines(self):
        try:
            return self._pay_lines.tolist()
        except Exception:
            return []

    @property
    def pay_chars(self):
        try:
            return self._pay_chars
        except Exception:
            return []

    @property
    def free_spins(self):
        return self.free_spins_value > 0

    @property
    def free_spins_value(self):
        return 0 if not self._free_spins or self._free_spins == 0 else \
            self.paytable_chars[FREE_SPINS_CHAR][self._free_spins-1]

    @property
    def game(self):
        return self.game_value > 0

    @property
    def game_value(self):
        return 0 if not self._game or self._game == 0 else \
            self.paytable_chars[GAME_CHAR][self._game-1]

    # Methods

    def spin(self, uid, sid, balance, bet, bet_lines, ais=False, free=False,
             config=None):

        if config:
            self._lines = config.get('lines')
            rails = []
            for item in config.get('rails'):
                values = array('c')
                values.fromstring(item)
                rails.append(values)
            self.rails = rails
            self.paytable_chars = config.get('paytable')
            self.max_lines = int(config.get('max_lines', 30))
            self.mini_game = config.get('mini_game')
            # print '>' * 80
            # print '>>>', self._lines
            # print '>>>', self.rails
            # print '>>>', self.paytable_chars
            # print '>>>', self.max_lines
            # print '>>>', self.mini_game
            # print '>' * 80

        if free:
            self._balance = balance
            self._bet = bet
            self._bet_lines = bet_lines

        else:
            self._balance, self._bet, self._bet_lines = \
                self.bet_validator(balance, bet, bet_lines)

        if not config:
            self._lines = self.lines_generator(ais)

        self._payment, self._pay_lines, self._pay_chars, self._game = \
            self.lines_validator(self._lines, self._bet, self._bet_lines)

        self._balance += self._payment
        self._free_spins = self.free_spins_validator(self._lines)

        try:
            if settings.TRACK:
                push_game_activity.delay(
                    uid=uid,
                    sid=sid,
                    mid=self.mid,
                    activity='spin',
                    balance=balance,
                    balance_diff=self._balance,
                    bet=bet,
                    bet_diff=self.bet,
                    bet_lines=bet_lines,
                    bet_lines_diff=self.bet_lines,
                    bet_max=self.bets[0],
                    lines=self._lines,
                    pay_lines=self.pay_lines,
                    payment=self.payment,
                    game=self.game,
                    game_value=self.game_value,
                    free_spins=self.free_spins,
                    free_spins_value=self.free_spins_value,
                    free=free,
                    # ai_session=ais
                )
        except Exception:
            pass
        return self._balance, self._bet, self._bet_lines

    # Generators

    def lines_generator(self, ais=False):
        result = ''
        chars = randint(CHARACTERS_SUM, size=15)
        x, y = 0, 0
        try:
            if self._rails_data:
                index = bisect.bisect_left(
                    self.rails_levels[self._rails_index][1],
                    self._bet_lines
                )
                rails = self._rails_data[index]
            else:
                raise ValueError('C8(int)')
        except:
            rails = self.rails
        try:
            if ais:
                new_rails = deepcopy(rails)
                replace_char = AI_SESSION_REPLACEMENT
                shuffle(replace_char)
                for i, (k, v) in enumerate(AI_SESSION_VALUES):
                    r = new_rails[i]
                    for ii in xrange(v):
                        r.append(k)
                        r.remove(replace_char[i])
                rails = new_rails
        except:
            rails = self.rails
        for p in MPOS:
            if p != 0 and p % 5 == 0:
                y += 1
            x = p if p < 5 else p - 5 * y
            result += rails[x][chars[p]]
        return result

    # Validators

    def bet_validator(self, balance, bet, bet_lines):
        if balance < self.bets[-1]:
            raise ValueError('balance (?)')
        elif bet not in self.bets:
            raise ValueError('bet (?)')
        elif bet_lines < 0 or bet_lines > self.max_lines:
            raise ValueError('max lines (?)')
        elif balance < (bet * bet_lines):
            if bet_lines > 1:
                _bet_lines = array('b', xrange(1, bet_lines))
                while _bet_lines:
                    bet_lines = _bet_lines.pop()
                    if balance >= (bet * bet_lines):
                        break
            if bet_lines == 1:
                for bet in self.bets:
                    if balance >= (bet * bet_lines):
                        break
        diff = balance - (bet * bet_lines)
        if diff < 0:
            raise ValueError('balance (-)')
        return diff, bet, bet_lines

    def lines_validator(self, lines, bet, bet_lines):
        pay_lines = self.paytable_lines[0:bet_lines]
        balance = 0
        balance_lines = array('b')
        balance_chars = []
        balance_game = 0
        balance_game_line = 0
        line_id = 0
        for pay_line in pay_lines:
            line = ''
            line_id += 1
            base_char = ''
            position = 0
            ignore = False
            for col in MCOLS:
                x = (pay_line[col] * 5) + col
                char = lines[x:x+1]
                if not base_char and char not in IGNORE_CHARS \
                        or (base_char == WILDCARD_CHAR and base_char != char):
                    base_char = char
                if not ignore and char not in IGNORE_CHARS \
                        and char in (base_char, WILDCARD_CHAR,):
                    position += 1
                else:
                    ignore = True
                line += char
            game = GAME_VALIDATE.search(line)
            if game:
                game_value = len(game.group())
                if game_value > balance_game:
                    balance_game = game_value
                    balance_game_line = line_id
            wildcard = WILDCARD_VALIDATE.search(line)
            if wildcard and base_char in IGNORE_CHARS and position > 0:
                base_char = WILDCARD_CHAR
            if base_char not in IGNORE_CHARS and position > 0:
                pay = self.paytable_chars[base_char][position-1] * bet
                if pay > 0 and line_id not in balance_lines:
                    balance_lines.append(line_id)
                    balance_chars.append(pay_line[0:position])
                balance += pay
            try:
                if self.paytable_chars[GAME_CHAR][balance_game-1] > 0 \
                    and balance_game_line not in balance_lines \
                        and balance_game_line > 0:
                    balance_lines.append(balance_game_line)
                    balance_chars.append(pay_line[0:position])
            except Exception:
                pass
        return balance, balance_lines, balance_chars, balance_game

    def free_spins_validator(self, chars):
        result = chars.count(FREE_SPINS_CHAR)
        return result if result < 5 else 5

    # Mini Game

    def get_mini_game(self):
        if not self.mini_game:
            raise ValueError('Mini Game (?)')
        result = []
        for item in self.mini_game:
            line = list(item)
            shuffle(line)
            result.append(result)
        return result

    def verify_mini_game(self, uid, sid, values, matrix, bet, factor):
        if not values or not matrix:
            raise ValueError('Invalid values (x)')
        elif bet not in self.bets:
            raise ValueError('Bet (x)')
        try:
            points = []
            for item, value in enumerate(values):
                row_total, row_values = value
                row_points = matrix[item]
                if row_total > sum(row_points) + 1 or row_total < -1:
                    raise ValueError('Invalid values (sum)')
                elif row_total <= 0:
                    result = 0 if row_points[row_values] < 0 \
                        else sum(sorted(row_points)[-2:])
                else:
                    result = sum(row_points[pos] for pos in row_values)
                points.append(result)
            balance = sum(points) * bet * factor
            try:
                if settings.TRACK:
                    push_game_activity.delay(
                        uid=uid,
                        sid=sid,
                        mid=self.mid,
                        activity='mini_game',
                        matrix=matrix,
                        matrix_values=values,
                        bet=bet,
                        factor=factor,
                        points=points,
                        balance=balance
                    )
            except Exception:
                pass
            return points, balance
        except Exception:
            raise ValueError('Mini Game Verify (x)')
