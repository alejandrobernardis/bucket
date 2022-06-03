#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 09/Oct/2013 14:40

import os
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

for folder in ('../app', '../lib',):
    sys.path.insert(0, os.path.abspath(os.path.join(ROOT_PATH, folder)))

import settings
import datetime
import shutil


def week_range(value=None):
    if not value or not isinstance(value, datetime.date):
        value = datetime.date.today()
    value = datetime.datetime(value.year, value.month, value.day)
    y, w, d = value.isocalendar()
    ws = value if d == 7 else value - datetime.timedelta(d)
    we = ws + datetime.timedelta(6)
    return ws, we


def week_days_list(value=None):
    ws, we = week_range(value)
    return [ws + datetime.timedelta(item) for item in xrange(0, 7)]


def main():
    year = None
    month = None
    date = datetime.datetime.utcnow()
    today = datetime.datetime(date.year, date.month, date.day)
    base_path = '%s/data/graph' % settings.STATIC_PATH

    for date in week_days_list():
        if date < today:
            path = '%s/%s/%s/%s' % (base_path, date.year, date.month, date.day)
            if not year:
                year = date.year
            elif year and year < date.year:
                path = '%s/%s' % (base_path, year)
                if os.path.isdir(path):
                    shutil.rmtree(path)
            if not month:
                month = date.month
            elif month and month < date.month:
                path = '%s/%s/%s' % (base_path, year, month)
                if os.path.isdir(path):
                    shutil.rmtree(path)
            if os.path.isdir(path):
                shutil.rmtree(path)
        else:
            break


if __name__ == "__main__":
    main()