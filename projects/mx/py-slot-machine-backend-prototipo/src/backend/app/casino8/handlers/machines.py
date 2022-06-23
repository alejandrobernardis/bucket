#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 06/09/2013 19:46

import json
import datetime
from casino8.games.roulette import RouletteSlot, RouletteBonus
from casino8.handlers.base import BaseHandler
from casino8.machines.configurations import DEVICE_LEVELS, BONUS_TIME, \
    BONUS_TIMES
from casino8.security.sessions import session_verify
from casino8.security.iron_man import IronMan
from importlib import import_module


class SpinHandler(BaseHandler):
    @session_verify
    def post(self, *args, **kwargs):
        try:
            mid = self.get_argument('mid', None)
            bet = self.get_argument('bet', None)
            lines = self.get_argument('lines', None)

            self.validate_arguments(mid, bet, lines)

            try:
                module = import_module('casino8.machines.slots')

            except ImportError:
                raise ImportError('Slot Module (x)')

            mid = int(mid)

            try:
                machine_class = getattr(module, 'Slot%d' % mid)

            except AttributeError:
                raise ValueError('Slot Machine ID (?)')

            session = self.session.data
            session.update(mid=mid, bet=float(bet), lines=int(lines))
            free_spins = (session.get('free_spins') > 0)
            machine = machine_class(session.get('level'))

            machine.spin(
                session.get('uid'),
                session.get('sid'),
                session.get('balance'),
                session.get('bet'),
                session.get('lines'),
                False,  # self.ai_session_enabled,
                free_spins
            )

            if free_spins:
                value = session.get('free_spins') - 1
                session['free_spins'] = value + machine.free_spins_value

            else:
                value = session.get('points')
                session.update(
                    points=float(value + (machine.bet * machine.bet_lines)),
                    free_spins=machine.free_spins_value,
                )

            session.update(
                bet=machine.bet,
                lines=machine.bet_lines,
                balance=machine.balance,
                game=machine.game_value,
                spin_time=session.get('spin_time') + 1
            )

            # if self.ai_session_enabled:
            #     session['ai_session_spins'] += 1

            level_bet = 0
            level_award = 0
            level_bonus = 0
            level_change = 0
            level_machine = session.get('total_machines', 0)

            if session.get('points') >= session.get('points_next_level'):
                level_change = 1
                level = session.get('level') + 1
                level_data = DEVICE_LEVELS[level-1]
                level_bet = level_data[3]
                level_award = level_data[5]
                level_bonus = level_data[2]
                session.update(
                    level=level,
                    balance=session.get('balance') + level_bonus,
                )

            self.verify_user_config(session)
            session = self.session.data

            return self.get_json_response_and_finish(response={
                'score_info': {
                    'balance': session.get('balance'),
                    'payment': machine.payment,
                    'payment_level': level_bonus,
                    'count_level_reward': level_change,
                    'level': session.get('level'),
                    'value': int(session.get('points')),
                    'next_level_experience': session.get('points_next_level'),
                    'bet': session.get('bet')

                }, 'unlock': {
                    'bet': level_bet,
                    'bonus': level_award,
                    'machine': session.get('total_machines', 0) - level_machine,

                }, 'win_lines': {
                    'id_line': machine.pay_lines,
                    'id_chars': machine.pay_chars,
                    'is_game': (session.get('game') > 0),
                    'free_spin': (session.get('free_spins') > 0),
                    'number_of_free_spins': session.get('free_spins')

                }, 'view_reels': machine.lines
            })

        except Exception, e:
            return self.get_except_json_response_and_finish(e)


class SpinBonusHandler(BaseHandler):
    @session_verify
    def post(self, *args, **kwargs):
        try:
            result = dict()
            session = self.session.data

            if not session.get('gift_available'):
                raise ValueError('Gift (x)')

            total = session.get('gift_total')
            total_cmp = BONUS_TIMES - 1
            balance = session.get('balance')

            if total < total_cmp:
                award = session.get('gift_award')
                balance += award
                result.update(obj=0, amount=award, balance=balance)
                total += 1

            elif total >= total_cmp:
                game = RouletteBonus()

                game.spin(
                    session.get('uid'),
                    session.get('sid'),
                    session.get('balance'),
                    level=session.get('level'),
                )

                balance = game.total

                result.update(
                    obj=1,
                    balance=balance,
                    position=game.position + 1,
                    position_amount=game.payment,
                    options=game.positions,
                )

                total = 0

            else:
                raise ValueError('Gift (?)')

            time_now = datetime.datetime.utcnow()

            session.update(
                balance=balance,
                gift_award=0,
                gift_total=total,
                gift_available=False,
                gift_time_begin=time_now,
                gift_time_finish=time_now + datetime.timedelta(hours=BONUS_TIME)
            )

            config = self.verify_user_config(session)
            result.update(time=config.gift_time)
            return self.get_json_response_and_finish(response=result)

        except Exception, e:
            return self.get_except_json_response_and_finish(e)


class SpinGameHandler(BaseHandler):
    @session_verify
    def post(self, *args, **kwargs):
        try:
            session = self.session.data
            game_bet = float(session.get('bet', .25))
            game_factor = int(session.get('game', 0))

            if game_factor <= 0:
                raise ValueError('Game (x)')

            game = RouletteSlot()

            game.spin(
                session.get('uid'),
                session.get('sid'),
                session.get('balance'),
                bet=game_bet,
                factor=game_factor,
            )

            session.update(game=0, balance=game.total)
            self.verify_user_config(session)

            return self.get_json_response_and_finish(response={
                'balance': game.total,
                'position': game.position + 1,
                'position_amount': game.payment,
                'options': game.positions,
            })

        except Exception, e:
            return self.get_except_json_response_and_finish(e)


class SpinMiniGameGetHandler(BaseHandler):

    @session_verify
    def post(self, *args, **kwargs):
        try:
            session = self.session.data
            i = self.get_argument('i', None)
            self.validate_arguments(i)
            if not IronMan.defense(i):
                raise ValueError('Iron Man (?)')
            game_id = int(session.get('mid', 0))
            if game_id <= 0:
                raise ValueError('Game (x)')
            game_bet = float(session.get('bet', 0))
            if game_bet <= 0:
                raise ValueError('Game bet (x)')
            game_factor = int(session.get('game', 0))
            if game_factor <= 0:
                raise ValueError('Game factor (x)')
            try:
                module = import_module('casino8.machines.slots')
            except ImportError:
                raise ImportError('Slot Module (x)')
            try:
                machine_class = getattr(module, 'Slot%d' % game_id)
            except AttributeError:
                raise ValueError('Slot Machine ID (?)')
            machine = machine_class(session.get('level'))
            matrix = machine.get_mini_game()
            session.update(
                mini_game_id=game_id,
                mini_game_bet=game_bet,
                mini_game_factor=game_factor,
                mini_game_matrix=matrix
            )
            self.verify_user_config(session)
            return self.get_json_response_and_finish(response={
                'matrix': matrix, 'bet': game_bet, 'factor': game_factor
            })
        except Exception, e:
            return self.get_except_json_response_and_finish(e)


class SpinMiniGameSaveHandler(BaseHandler):

    @session_verify
    def post(self, *args, **kwargs):
        try:
            session = self.session.data
            values = self.get_argument('value', None)
            i = self.get_argument('i', None)
            self.validate_arguments(i, values)
            if not IronMan.defense(i):
                raise ValueError('Iron Man (?)')
            game_id = int(session.get('mini_game_id', 0))
            if game_id <= 0:
                raise ValueError('Game (x)')
            game_bet = float(session.get('mini_game_bet', 0))
            if game_bet <= 0:
                raise ValueError('Game bet (x)')
            game_factor = int(session.get('mini_game_factor', 0))
            if game_factor <= 0:
                raise ValueError('Game factor (x)')
            game_matrix = tuple(session.get('mini_game_matrix', 0))
            game_matrix_len = len(game_matrix)
            if not game_matrix or not game_matrix_len:
                raise ValueError('Game matrix (x)')
            values = json.loads({'values': values}).get('values')
            values_len = len(values)
            if not values_len or values_len != game_matrix_len:
                raise ValueError('Values (x)')
            try:
                module = import_module('casino8.machines.slots')
            except ImportError:
                raise ImportError('Slot Module (x)')
            try:
                machine_class = getattr(module, 'Slot%d' % game_id)
            except AttributeError:
                raise ValueError('Slot Machine ID (?)')
            machine = machine_class(session.get('level'))
            points, balance = machine.verify_mini_game(
                session.get('uid'),
                session.get('sid'),
                values,
                game_matrix,
                game_bet,
                game_factor
            )
            session.update(
                game=0,
                mini_game_id=0,
                mini_game_bet=0,
                mini_game_factor=0,
                mini_game_matrix=None,
                points=session.get('points', 0) + points,
                balance=session.get('balance', 0) + balance
            )
            self.verify_user_config(session)
            return self.get_json_response_and_finish(response={
                'mini_game': {
                    'balance': balance,
                    'bet': game_bet,
                    'factor': game_factor,
                    'points': points,
                },
                'balance': session.get('balance'),
                'points': session.get('points')
            })
        except Exception, e:
            return self.get_except_json_response_and_finish(e)


# ------------------------------------------------------------------------------

handlers_list = [
    (r'/do/spin/?', SpinHandler),
    (r'/do/spin/bonus/?', SpinBonusHandler),
    (r'/do/spin/game/?', SpinGameHandler),
    (r'/do/spin/mini/game/get/?', SpinMiniGameGetHandler),
    (r'/do/spin/mini/game/save/?', SpinMiniGameSaveHandler),
]
