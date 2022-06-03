#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 12/Dec/2013 15:07

from __future__ import division

import os
import re
import settings
from array import array
from unicodecsv import UnicodeReader


rgx_level = re.compile(r'N\d+-\d+')
rgx_lines = re.compile(r'L\d+-\d+')


def rails_parser(filename=None):
    if not filename:
        filename = os.path.join(settings.DATA_PATH, 'rails.tmp.csv')
    with open(filename, 'rb') as fileinput:
        result = [
            array('c', ''),
            array('c', ''),
            array('c', ''),
            array('c', ''),
            array('c', ''),
        ]
        data = UnicodeReader(fileinput)
        for row in data:
            if str(row[0]).lower() not in ('x', 'eof',):
                char = str(row[0]).upper()
                for col in xrange(0, 5):
                    for c in xrange(int(row[col+1])):
                        result[col].append(char)
        return tuple(result)


def filename_analizer(filename):
    try:
        level = rgx_level.search(filename).group().split('-')[1]
        lines = rgx_lines.search(filename).group().split('-')[1]
        return level, lines
    except:
        raise ValueError('Nomenclatura mal definida: %s' % filename)


def run():
    base_path = os.walk(os.path.join(settings.DATA_PATH, 'general'))

    for root, dirs, files in base_path:
        for fileinput in files:
            path = os.path.abspath(os.path.join(root, fileinput))
            rails = rails_parser(path)
            level, lines = filename_analizer(fileinput)

            print path, level, lines
            print rails
            print '--'


if __name__ == '__main__':
    run()