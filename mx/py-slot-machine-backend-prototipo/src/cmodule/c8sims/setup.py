#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 12/Jun/2014 16:18

from distutils.core import setup, Extension
c_ext = Extension("_sims", ["_sims.c"])
setup(ext_modules=[c_ext])