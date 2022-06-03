#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 12/Dec/2013 14:32

import json
import datetime


filename = './slot_machines.json'


with open(filename, 'rb') as file_input:
    data = json.load(file_input)
    for key, value in data.items():
        print key, value
    data['modified'] = datetime.datetime.utcnow()


with open(filename, 'wb') as file_output:
    json.dump(data, file_output)