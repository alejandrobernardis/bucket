#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 28/Jan/2014 23:39

import re
import os
import json
import hashlib

e_list = []
e_dict = {}
e_analyzer_dict = {}
e_parser = None
e_analyzer = False
e_last_line = None

new_date = 140131
i_rx = re.compile(r'^\[I', re.I)
w_rx = re.compile(r'^\[W', re.I)
e_rx = re.compile(r'^\[E', re.I)
d_rx = re.compile(r'^\[E\s\d+\s', re.I)
s_rx = re.compile(r'^\s', re.I)
r_rx = re.compile(r'^\[E(.+)\s\{', re.I)
n_rx = re.compile(r'^\s+\n', re.I)

for root, dirs, files in os.walk('./supervisord'):
    for f in files:
        filename = './supervisord/%s' % f
        fname, fext = os.path.splitext(filename)
        if fext.lower() not in ('.log',):
            continue
        reader = open(filename, 'r')
        for i in reader.readlines():
            e = e_rx.search(i)
            if e:
                if new_date:
                    try:
                        date = int(d_rx.search(i).group().replace('[E ', ''))
                        if date < new_date:
                            continue
                    except Exception as e:
                        continue
                h = hashlib.md5()
                h.update(i)
                e_parser = h.hexdigest()
                e_analyzer = not bool(r_rx.search(i))
                e_dict[e_parser] = []
                e_dict[e_parser].append(i)
                print '>>> %s' % e_parser
                print i,
            elif i_rx.search(i) or w_rx.search(i):
                if e_parser:
                    print i
                    print ''
                e_parser = None
            elif e_parser and s_rx.search(i):
                e_dict[e_parser].append(i)
                if e_analyzer and e_last_line and n_rx.search(i):
                    e_analyzer = False
                    h = hashlib.md5()
                    h.update(e_last_line)
                    e_analyzer_hash = h.hexdigest()
                    try:
                        e_analyzer_dict[e_analyzer_hash]['q'] += 1
                        # e_analyzer_dict[e_analyzer_hash]['h'].append(e_parser)
                    except:
                        e_analyzer_dict[e_analyzer_hash] = {
                            'e': e_last_line.strip(), 'q': 1  #, 'h': [e_parser]
                        }
                e_last_line = i
                print e_last_line,
        print 'File: %s ... ok' % filename

json.dump(e_analyzer_dict, open('report.json', 'w'), indent=4)
print 'FIN!'