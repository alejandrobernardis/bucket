#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 11/Dec/2013 16:51


import os
import sys
import json

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

for item in ('../src/backend/app',):
    sys.path.insert(0, os.path.abspath(os.path.join(ROOT_PATH, item)))

from casino8.machines.slots import *

machines = (
    Slot104,
)

for machine in machines:
    for i in (9, 9, 9, 9,):
        m = machine(i)
        m.spin(1, 1, 42448, 25, 25)
        print m.lines, m.pay_lines, m.payment
        print json.dumps(m.pay_chars)
