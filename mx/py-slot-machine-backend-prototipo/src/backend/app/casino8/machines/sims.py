#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 12/Jun/2014 14:40

import _sims


class SimsClient(object):
    @staticmethod
    def get_factor(mid, lines, bet):
        return _sims.getfactor(int(mid), int(lines), float(bet))

    @staticmethod
    def get_matrix(mid, lines, bet):
        return _sims.getmatrix(int(mid), int(lines), float(bet))