#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 12/09/2013 08:32


ROULETTE_SLOT_MODE = 'slot'
ROULETTE_SLOT_TOLERANCE = .000001
ROULETTE_SLOT_PROBABILITY = (
    0.10,
    0.10,
    0.10,
    0.10,
    0.10,
    0.10,
    0.10,
    0.10,
    0.10,
    0.10,
)
ROULETTE_SLOT_PAYTABLE = (
    (5, 7.5, 10,),
    (10, 15, 20,),
    (10, 15, 20,),
    (15, 22.5, 30,),
    (20, 30, 40,),
    (30, 45, 60,),
    (50, 75, 100,),
    (100, 150, 200,),
    (150, 225, 300,),
    (200, 300, 400,),
)


ROULETTE_BONUS_MODE = 'bonus'
ROULETTE_BONUS_TOLERANCE = .000001
ROULETTE_BONUS_PROBABILITY = (
    0.22, 0.19, 0.13, 0.12, 0.10, 0.09, 0.07, 0.05, 0.02, 0.01,
)
