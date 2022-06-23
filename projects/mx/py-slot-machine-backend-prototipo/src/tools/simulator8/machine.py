#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 19/Nov/2013 13:10

import math
from array import array
from common import random_and_probability
from config import DEVICE_LEVELS, DEFAULT_BETS, DEFUALT_PAYTABLE_LINES, \
    CHARACTERS_SUM, WILDCARD_CHAR, IGNORE_CHARS, FREE_SPINS_CHAR, GAME_CHAR, \
    GAME_VALIDATE, WILDCARD_VALIDATE, CHARACTERS, MPOS, MCOLS, \
    ROULETTE_SLOT_TOLERANCE, ROULETTE_SLOT_MODE, ROULETTE_SLOT_PROBABILITY, \
    ROULETTE_SLOT_PAYTABLE
from numpy.random import randint


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

    def __init__(self, user_level=0):
        try:
            self.level = DEVICE_LEVELS[user_level - 1]
        except Exception:
            self.level = DEVICE_LEVELS[0]
        try:
            self.bets = DEFAULT_BETS[DEFAULT_BETS.index(self.level[3]):]
        except Exception:
            self.bets = DEFAULT_BETS[-5:]
        self.paytable_lines = DEFUALT_PAYTABLE_LINES[0:self.max_lines]
        if self.rails_levels:
            self.rails = self._search_rails(user_level)
        self._balance = None
        self._bet = None
        self._bet_lines = None
        self._lines = None
        self._payment = None
        self._pay_lines = None
        self._game = None
        self._balance = None
        self._free_spins = None
        self._free = None
        self._combos = {}

    def _search_rails(self, level):
        if level < 1:
            level = 1
        index = 0
        low, high = 0, len(self.rails_levels)-1
        while low <= high:
            mid = int(math.floor((low+high)/2))
            value = self.rails_levels[mid]
            if value < level:
                low = mid + 1
                index = mid
            elif value > level:
                high = mid - 1
                index = mid
            else:
                index = mid
                break
        if index > 0 and level < self.rails_levels[index]:
            index -= 1
        return self.rails_values[index]

    # Properties

    @property
    def combos(self):
        return self._combos

    @combos.setter
    def combos(self, value):
        self._combos = value

    @property
    def matrix(self):
        return self._lines

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

    def spin(self, balance, bet, bet_lines, free=False):
        if free:
            self._balance = balance
            self._bet = bet
            self._bet_lines = bet_lines
        else:
            self._balance, self._bet, self._bet_lines = \
                self.bet_validator(balance, bet, bet_lines)
        self._free = free
        self._lines = self.lines_generator()
        self._payment, self._pay_lines, self._game = \
            self.lines_validator(self._lines, self._bet, self._bet_lines)
        self._balance += self._payment
        self._free_spins = self.free_spins_validator(self._lines)
        return self._balance, self._bet, self._bet_lines

    # Generators

    def lines_generator(self):
        result = ''
        chars = randint(CHARACTERS_SUM, size=15)
        x, y = 0, 0
        for p in MPOS:
            if p != 0 and p % 5 == 0:
                y += 1
            x = p if p < 5 else p - 5 * y
            result += self.rails[x][chars[p]]
        return result

    # Validators

    def bet_validator(self, balance, bet, bet_lines):
        if balance < self.bets[-1]:
            raise ValueError('balance (?)')
        elif bet not in self.bets:
            raise ValueError('bet (?)')
        elif bet_lines < 0 or bet_lines > self.max_lines:
            raise ValueError('max lines  (?)')
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
                    if not self._free:
                        try:
                            combo = self._combos[position]
                            combo[0] += 1
                            combo[1] += pay
                        except Exception:
                            self._combos[position] = [1, pay]
                    balance_lines.append(line_id)
                balance += pay
            try:
                if self.paytable_chars[GAME_CHAR][balance_game-1] > 0 \
                    and balance_game_line not in balance_lines \
                        and balance_game_line > 0:
                    balance_lines.append(balance_game_line)
            except Exception:
                pass
        return balance, balance_lines, balance_game

    def free_spins_validator(self, chars):
        result = chars.count(FREE_SPINS_CHAR)
        return result if result < 5 else 5


class BotMachine(AbstractMachine):
    mid = 101
    name = "BM"
    full_name = "Bot Machine"
    max_lines = 10

    rails = (
        array('c', 'AAAAAABBBBBBCCCCDDEEEEFFGGHIJKKL'),
        array('c', 'AAAAAAABBBBCCCCCDDDEEEFFFGHIJJKL'),
        array('c', 'AAAAAAABBBBCCCDDEEEEFFGGGHHIIJKL'),
        array('c', 'AAAAABBBBBCCCCDDDEEEFFFFGGHHIJKL'),
        array('c', 'AAAAAABBBCCCCDDEEFFFFGGGGHHIIJKL'),
    )

    paytable_chars = {
        'A': (0, 0, 5, 15, 70),
        'B': (0, 0, 5, 20, 90),
        'C': (0, 0, 8, 30, 110),
        'D': (0, 0, 10, 55, 180),
        'E': (0, 0, 12, 65, 250),
        'F': (0, 2, 15, 85, 340),
        'G': (0, 2, 18, 100, 500),
        'H': (0, 5, 25, 115, 700),
        'I': (0, 6, 50, 145, 1300),
        'J': (0, 0, 1, 1.5, 2),
        'K': (0, 0, 10, 20, 30),
        'L': (0, 5, 60, 600, 3000),
    }


class AbstractRoulette(object):
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


class RouletteSlot(AbstractRoulette):
    def __init__(self):
        super(RouletteSlot, self).__init__()
        self._mode = ROULETTE_SLOT_MODE
        self.tolerance = ROULETTE_SLOT_TOLERANCE
        self.probability = ROULETTE_SLOT_PROBABILITY

    def spin(self, balance, *args, **kwargs):
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
        return self._position