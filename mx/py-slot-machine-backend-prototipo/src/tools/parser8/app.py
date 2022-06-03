#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 21/Nov/2013 22:26

from __future__ import division

import os
import datetime
import settings
from array import array
from optparse import OptionParser
from unicodecsv import UnicodeReader


RAIL_TEMPLATE = "{},\n"
PAYTABLE_TEMPLATE = "'{}': ({}),\n"


def options_parser():
    parser = OptionParser()
    parser.add_option(
        '-f', '--file', dest='filename', default=None, type='string')
    parser.add_option(
        '-o', '--output', dest='output', default=None, type='string')
    parser.add_option(
        '-v', '--verbose', action='store_true', dest='verbose', default=False)
    parser.add_option(
        '-r', '--rail-mode', action='store_true', dest='rails_mode',
        default=False)
    parser.add_option(
        '-p', '--paytable-mode', action='store_true', dest='paytable_mode',
        default=False)
    return parser.parse_args()


def rails_parser(file_name=None):
    if not file_name:
        file_name = os.path.join(settings.DATA_PATH, 'rails.tmp.csv')
    with open(file_name, 'rb') as file_input:
        result = [
            array('c', ''),
            array('c', ''),
            array('c', ''),
            array('c', ''),
            array('c', ''),
        ]
        data = UnicodeReader(file_input)
        for row in data:
            if str(row[0]).lower() not in ('x', 'eof',):
                char = str(row[0]).upper()
                for col in xrange(0, 5):
                    for c in xrange(int(row[col+1])):
                        result[col].append(char)
        return tuple(result)


def paytable_parser(file_name=None):
    if not file_name:
        file_name = os.path.join(settings.DATA_PATH, 'paytable.tmp.csv')
    with open(file_name, 'rb') as file_input:
        result = {}
        data = UnicodeReader(file_input)
        for row in data:
            if str(row[0]).lower() not in ('x', 'eof',):
                char = str(row[0]).upper()
                values = []
                for col in xrange(1, 6):
                    values.append(int(row[col]))
                result[char] = tuple(values)
        return result


def run(opts):
    date = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    recordset = rails_parser(opts.filename) \
        if opts.rails_mode else paytable_parser(opts.filename)
    output_name = os.path.join(settings.DATA_PATH, 'output_%s.txt' % date) \
        if not opts.output else opts.output
    if opts.verbose:
        print '-' * 80
        print 'Verbose Mode:'
        print '-' * 80
    with open(output_name, 'wb') as output_file:
        if opts.rails_mode:
            for row in recordset:
                tmpl = RAIL_TEMPLATE.format(row)
                output_file.write(tmpl)
                if opts.verbose:
                    print tmpl,
        else:
            keys = recordset.keys()
            keys.sort()
            for key in keys:
                value = ', '.join([str(item) for item in recordset[key]])
                tmpl = PAYTABLE_TEMPLATE.format(key, value)
                output_file.write(tmpl)
                if opts.verbose:
                    print tmpl,
    if opts.verbose:
        print '-' * 80


if __name__ == '__main__':
    options, arguments = options_parser()
    if not options.rails_mode and not options.paytable_mode:
        raise ValueError('Mode not found')
    elif options.rails_mode and options.paytable_mode:
        raise ValueError(
            'Running in ambiguous mode, rails and pay table together')
    else:
        run(options)