#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 15/Nov/2013 11:10

import os
import random
import settings
from config import DEVICE_LEVELS, DEFAULT_BETS_ASC
from math import floor
from PyQt5.QtGui import QFont, QColor


# Assets
def get_asset(asset):
    asset_path = os.path.join(settings.ASSETS_PATH, asset)
    if not os.path.isfile(asset_path):
        return os.path.join(settings.ASSETS_PATH, 'default.png')
    return asset_path


# Helpers
def set_bets_by_level(level):
    index = 5
    device_level = DEVICE_LEVELS[level-1]
    if device_level[0] == level:
        max_bet = device_level[3]
        low, high = 0, len(DEFAULT_BETS_ASC)-1
        while low <= high:
            mid = int(floor((low+high)/2))
            value = DEFAULT_BETS_ASC[mid]
            if value < max_bet:
                low = mid + 1
            elif value > max_bet:
                high = mid - 1
            else:
                index = mid + 1
                break
    return DEFAULT_BETS_ASC[0:index]


def set_lines_by_level(level, fix=False):
    try:
        value = DEVICE_LEVELS[level-1][4]
    except Exception:
        value = DEVICE_LEVELS[0][4]
    return value if not fix else value + 1


def set_points_by_level(level):
    try:
        value = DEVICE_LEVELS[level-1][1]
    except Exception:
        value = DEVICE_LEVELS[0][1]
    return value


def set_points_next_level(level=1):
    try:
        device_total = len(DEVICE_LEVELS)
        if level > device_total:
            level = device_total
        elif level < 0:
            level = 0
        device_level = DEVICE_LEVELS[level-1]
        device_next_level = level
        if device_level[0] == level and device_next_level <= device_total:
            device_level = DEVICE_LEVELS[device_next_level]
        return device_level[1]
    except Exception:
        return 0


def get_level_by_points(points=0):
        index = 0
        low, high = 0, len(DEVICE_LEVELS)-1
        while low <= high:
            mid = int(floor((low+high)/2))
            value = DEVICE_LEVELS[mid][1]
            if value < points:
                low = mid + 1
                index = mid
            elif value > points:
                high = mid - 1
                index = mid
            else:
                index = mid
                break
        if points < DEVICE_LEVELS[index][1]:
            index -= 1
        return DEVICE_LEVELS[index]  # [0]


def tail(f, n, offset=None):
    avg_line_length = 74
    to_read = n + (offset or 0)
    while 1:
        try:
            f.seek(-(avg_line_length * to_read), 2)
        except IOError:
            f.seek(0)
        pos = f.tell()
        lines = f.read().splitlines()
        if len(lines) >= to_read or pos == 0:
            return lines[-to_read:offset and -offset or None], \
                len(lines) > to_read or pos > 0
        avg_line_length *= 1.3


def _approx_eq(v1, v2, tolerance):
    return abs(v1-v2) <= tolerance


def _whithin(low, value, high, tolerance):
    return (value > low or _approx_eq(low, value, tolerance)) \
        and (value < high or _approx_eq(high, value, tolerance))


def random_and_probability(probability, tolerance):
    acc = 0.0
    acc_list = [acc]
    for item in probability:
        acc += item
        acc_list.append(acc)
    interval = -1
    number = random.random()
    for item in xrange(len(acc_list)-1):
        if _whithin(acc_list[item], number, acc_list[item+1], tolerance):
            interval = item
            break
    return 0 if interval == -1 else interval


# Fonts
FONT_VERDANA_10 = QFont('Verdana', 10)
FONT_VERDANA_12 = QFont('Verdana', 12)
FONT_VERDANA_TABLE = QFont('Verdana', 10, QFont.Bold)
FONT_VERDANA_TABLE_ROW = QFont('Verdana', 10)
FONT_VERDANA_REPORT = QFont('Verdana', 12, QFont.Bold)
FONT_VERDANA_REPORT_ROW = QFont('Verdana', 12)

# Colors
COLOR_OK = QColor(223, 240, 216)
COLOR_ERROR = QColor(242, 222, 222)
COLOR_INFO = QColor(217, 237, 247)
COLOR_WARNING = QColor(252, 248, 227)