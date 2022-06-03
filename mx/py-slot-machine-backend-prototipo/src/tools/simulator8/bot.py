#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 19/Nov/2013 13:10

from __future__ import division

import os
import json
import time
import traceback
import copy
import settings
from array import array
from common import get_level_by_points, set_points_next_level
from config import DEFAULT_REPORT
from machine import BotMachine, RouletteSlot
from optparse import OptionParser
from unicodecsv import UnicodeReader, UnicodeWriter


def options_parser():
    parser = OptionParser()
    parser.add_option(
        '-f', '--file', dest='filename', default=None, type='string')
    parser.add_option(
        '-o', '--output', dest='output', default=None, type='string')
    parser.add_option(
        '-d', '--delay', dest='delay', default=0, type='int')
    parser.add_option(
        '-i', '--iterations', dest='iterations', default=400, type='int')
    parser.add_option(
        '-m', '--balance', dest='balance', default=200, type='int')
    parser.add_option(
        '-b', '--bet', dest='bet', default=0.25, type='float')
    parser.add_option(
        '-l', '--lines', dest='lines', default=30, type='int')
    parser.add_option(
        '-x', '--max-lines', dest='max_lines', default=0, type='int')
    parser.add_option(
        '-n', '--level', dest='level', default=1, type='int')
    parser.add_option(
        '-p', '--points', dest='points', default=0, type='int')
    parser.add_option(
        '-v', '--verbose', action='store_true', dest='verbose', default=False)
    return parser.parse_args()


def rails_parser(file_name=None):
    if not file_name:
        file_name = os.path.join(settings.DATA_PATH, 'table.tmp.csv')
    with open(file_name, 'rb') as file_input:
        header = None
        result = [
            array('c', ''),
            array('c', ''),
            array('c', ''),
            array('c', ''),
            array('c', '')
        ]
        data = UnicodeReader(file_input)
        for row in data:
            if not header and str(row[0]).lower() == 'x':
                header = row
                continue
            elif str(row[0]).lower() != 'eof':
                char = str(row[0]).upper()
                for col in xrange(0, 5):
                    for c in xrange(int(row[col+1])):
                        result[col].append(char)
            else:
                break
        return tuple(result)


def run(options, paytable=None, report_date=None, not_return=True):
    # metrics

    m_iterations = 0
    m_iterations_break = 0
    m_bet = 0
    m_lines = 0
    m_payment = 0
    m_game = 0
    m_game_wofs = 0
    m_game_payment = 0
    m_free_spins = 0
    m_free_spins_wofs = 0
    m_free_spins_times = 0
    m_free_spins_times_wofs = 0
    m_free_spins_payment = 0
    m_spin = 0
    m_spin_payment = 0
    m_spin_win = 0
    m_level = options.level
    m_level_payment = 0
    m_points = options.points

    # condition zero

    balance = options.balance
    balance_old = options.balance
    bet = options.bet
    lines = options.lines
    free_spins = False
    next_level_points = set_points_next_level(m_level)
    rails = rails_parser(options.filename)

    report = copy.deepcopy(DEFAULT_REPORT)
    report_csv = \
        os.path.join(settings.DATA_PATH, 'csv/report.%s.csv' % report_date)

    if options.iterations >= 50000:
        options.verbose = True

    # machine

    machine = BotMachine(m_level)
    machine.rails = rails
    machine.max_lines = options.max_lines

    if paytable:
        machine.paytable_chars = paytable

    if options.verbose:
        print json.dumps({
            'machine': {
                'bets': machine.bets,
                'rails': machine.rails.__str__(),
                'paytable': machine.paytable_chars,
                'level': machine.level,
            }
        })

    # iterations

    with open(report_csv, 'wb') as file_report_out:
        writer = UnicodeWriter(file_report_out)
        writer.writerow(('iteration', 'matrix', 'balance_begin',
                         'balance_finish', 'bet', 'lines', 'payment', 'game',
                         'game_value', 'free_spins', 'free_spins_value',
                         'free_spins_mode'))

        for _ in xrange(options.iterations):
            try:
                free_spins_mode = free_spins > 0

                balance, bet, lines = \
                    machine.spin(balance, bet, lines, free_spins_mode)

                m_lines += lines
                m_bet += bet * lines
                matrix = machine.matrix

                if free_spins_mode:
                    free_spins_value = free_spins - 1
                    free_spins = free_spins_value + machine.free_spins_value
                    m_free_spins += machine.free_spins_value
                    m_free_spins_payment += machine.payment

                else:
                    m_points += bet * lines
                    m_spin += 1
                    m_game_wofs += 1 if machine.game else 0
                    m_free_spins_times_wofs += 1 if machine.free_spins else 0
                    m_free_spins_wofs += machine.free_spins_value

                    if m_points >= next_level_points:
                        level = get_level_by_points(m_points)
                        m_level = level[0]
                        m_level_payment += level[5]
                        m_payment += level[5]
                        balance += level[5]

                        next_level_points = set_points_next_level(m_level)
                        combos = machine.combos

                        machine = BotMachine(m_level)
                        machine.rails = rails
                        machine.combos = combos
                        machine.max_lines = options.max_lines

                        if paytable:
                            machine.paytable_chars = paytable

                    m_spin_payment += machine.payment

                if machine.free_spins:
                    free_spins += machine.free_spins_value
                    m_free_spins += machine.free_spins_value
                    m_free_spins_times += 1

                m_payment += machine.payment
                spin_win = (machine.payment > 0)

                if machine.game:
                    game = RouletteSlot()
                    game.spin(balance, factor=machine.game_value, bet=bet)
                    m_game += 1
                    m_game_payment += game.payment
                    m_payment += game.payment
                    balance += game.payment
                    spin_win = (game.payment > 0)

                m_iterations += 1
                m_spin_win += 1 if spin_win else 0

                if options.verbose:
                    print json.dumps({
                        'iteration': m_iterations,
                        'balance': balance,
                        'bet': bet,
                        'lines': lines,
                        'payment': machine.payment,
                        'pay_lines': machine.pay_lines,
                        'game': machine.game,
                        'game_value': machine.game_value,
                        'free_spins': machine.free_spins,
                        'free_spins_value': machine.free_spins_value,
                        'free_spins_mode': free_spins_mode
                    }, sort_keys=True)

                writer.writerow([
                    m_iterations,
                    matrix,
                    balance_old,
                    balance,
                    bet,
                    lines,
                    machine.payment,
                    machine.game,
                    machine.game_value,
                    machine.free_spins,
                    machine.free_spins_value,
                    free_spins_mode
                ])

                balance_old = balance

                if options.delay > 0:
                    time.sleep(options.delay)

            except Exception as e:
                if options.verbose:
                    print '(e): %s' % e
                    print '(t): %s' % traceback.format_exc()
                m_iterations_break = m_iterations
                break

    # report

    combo_x2 = machine.combos.get(2, [0, 0])
    combo_x3 = machine.combos.get(3, [0, 0])
    combo_x4 = machine.combos.get(4, [0, 0])
    combo_x5 = machine.combos.get(5, [0, 0])

    data = {
        'free_spins': m_free_spins,
        'free_spins_times': m_free_spins_times,
        'free_spins_payment': m_free_spins_payment,
        'gain': balance - options.balance,
        'game_times': m_game,
        'game_payment': m_game_payment,
        'machine_bet': m_bet,
        'machine_balance_begin': options.balance,
        'machine_balance_finish': balance,
        'machine_cfg_level': machine.level,
        'machine_cfg_max_lines': machine.max_lines,
        'machine_cfg_bets': machine.bets,
        'machine_iterations': options.iterations,
        'machine_iterations_break': m_iterations_break,
        'machine_level': m_level,
        'machine_lines': m_lines,
        'machine_payment': m_spin_payment,
        'machine_points': m_points,
        'machine_combo_x2_times': combo_x2[0],
        'machine_combo_x2_payment': combo_x2[1],
        'machine_combo_x3_times': combo_x3[0],
        'machine_combo_x3_payment': combo_x3[1],
        'machine_combo_x4_times': combo_x4[0],
        'machine_combo_x4_payment': combo_x4[1],
        'machine_combo_x5_times': combo_x5[0],
        'machine_combo_x5_payment': combo_x5[1],
        'machine_spin': m_spin,
        'options': vars(options) or options,
        'payment': m_payment,
    }

    file_output_path = \
        os.path.join(settings.DATA_PATH, options.output or 'report.json')

    with open(file_output_path, 'w') as file_output:
        json.dump(data, file_output, indent=4, sort_keys=True)

    if options.verbose:
        print json.dumps(data, indent=4, sort_keys=True)

    # Report !

    report[0][1] = report_date
    report[2][1] = '{:,}'.format(options.iterations)
    report[3][1] = '{:,}'.format(m_spin)
    report[4][1] = '{:,}'.format(m_iterations_break)
    report[5][1] = '{:,}'.format(balance)
    report[6][1] = '{:,}'.format(balance - options.balance)

    report[8][1] = '{:,}'.format(m_spin_win)
    report[9][1] = '{:,}'.format(m_iterations - m_spin_win)

    report[11][1] = '{:,}'.format(m_spin_payment)
    report[12][1] = '{:,}'.format(m_free_spins_payment)
    report[13][1] = '{:,}'.format(m_game_payment)
    report[14][1] = '{:,}'.format(m_payment)
    report[16][1] = '{:,}'.format(m_bet)

    total_combos = sum((combo_x2[0], combo_x3[0], combo_x4[0], combo_x5[0]))
    pay_combos = sum((combo_x2[1], combo_x3[1], combo_x4[1], combo_x5[1]))

    def calculate_percentage(value, total):
        if value == 0:
            return 0
        return '%.2f' % float(value/total*100) + '%'

    def calculate_percentage_one(value, total):
        if value == 0:
            return 0
        return '%.2f' % float(1/(value/total))

    report[19][1] = '{:,}'.format(combo_x2[0])
    report[19][2] = calculate_percentage(combo_x2[0], total_combos)
    report[19][3] = '{:,}'.format(combo_x2[1])
    report[19][4] = calculate_percentage(combo_x2[1], pay_combos)
    report[20][1] = '{:,}'.format(combo_x3[0])
    report[20][2] = calculate_percentage(combo_x3[0], total_combos)
    report[20][3] = '{:,}'.format(combo_x3[1])
    report[20][4] = calculate_percentage(combo_x3[1], pay_combos)
    report[21][1] = '{:,}'.format(combo_x4[0])
    report[21][2] = calculate_percentage(combo_x4[0], total_combos)
    report[21][3] = '{:,}'.format(combo_x4[1])
    report[21][4] = calculate_percentage(combo_x4[1], pay_combos)
    report[22][1] = '{:,}'.format(combo_x5[0])
    report[22][2] = calculate_percentage(combo_x5[0], total_combos)
    report[22][3] = '{:,}'.format(combo_x5[1])
    report[22][4] = calculate_percentage(combo_x5[1], pay_combos)
    report[23][1] = '{:,}'.format(total_combos)
    report[23][3] = '{:,}'.format(pay_combos)

    report[26][1] = '{:,}'.format(m_free_spins_times_wofs)
    report[27][1] = calculate_percentage(m_free_spins_times_wofs, m_spin)
    report[28][1] = \
        calculate_percentage_one(m_free_spins_times_wofs, m_spin)
    report[29][1] = '{:,}'.format(m_free_spins)
    report[30][1] = '{:,}'.format(m_free_spins_payment)
    report[31][1] = calculate_percentage(m_free_spins_payment, m_payment)

    report[34][1] = '{:,}'.format(m_game_wofs)
    report[35][1] = calculate_percentage(m_game_wofs, m_spin)
    report[36][1] = calculate_percentage_one(m_game_wofs, m_spin)
    report[37][1] = '{:,}'.format(m_game_payment)
    report[38][1] = calculate_percentage(m_game_payment, m_payment)

    wofs_kj = m_free_spins_times_wofs + m_game_wofs
    report[41][1] = '{:,}'.format(wofs_kj)
    report[42][1] = calculate_percentage(wofs_kj, m_spin)
    report[43][1] = calculate_percentage_one(wofs_kj, m_spin)
    pay_kj = m_free_spins_payment + m_game_payment
    report[44][1] = '{:,}'.format(pay_kj)
    report[45][1] = calculate_percentage(pay_kj, m_payment)

    final_report_csv = os.path.join(
        settings.DATA_PATH, 'csv/report.result.%s.csv' % report_date)

    with open(final_report_csv, 'wb') as tmpreport:
        writer = UnicodeWriter(tmpreport, quotechar='"')
        writer.writerows(report_csv)

    if not not_return:
        return report


class OptionsHelper(object):
    filename = None
    output = None
    output_csv = None
    delay = 0
    iterations = 0
    balance = 0
    bet = 0
    lines = 0
    max_lines = 0
    level = 0
    points = 0
    verbose = False


if __name__ == '__main__':
    opts, arguments = options_parser()
    run(opts)
