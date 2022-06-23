#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 21/Apr/2014 11:19

import sys
import time
import random

N = 624
M = 397
MATRIX_A = 0x9908b0dfL
UPPER_MASK = 0x80000000L
LOWER_MASK = 0x7fffffffL
TEMPERING_MASK_B = 0x9d2c5680L
TEMPERING_MASK_C = 0xefc60000L


def TEMPERING_SHIFT_U(y):
    return (y >> 11)


def TEMPERING_SHIFT_S(y):
    return (y << 7)


def TEMPERING_SHIFT_T(y):
    return (y << 15)


def TEMPERING_SHIFT_L(y):
    return (y >> 18)


mt = []
mti = N + 1


def sgenrand(seed):
    global mt, mti
    mt = []
    mt.append(seed & 0xffffffffL)
    for i in xrange(1, N + 1):
        mt.append((69069 * mt[i - 1]) & 0xffffffffL)
    mti = i


def genrand():
    global mt, mti
    mag01 = [0x0L, MATRIX_A]
    y = 0
    if mti >= N:
        if mti == N + 1:
            sgenrand(4357)
        for kk in xrange((N - M) + 1):
            y = (mt[kk] & UPPER_MASK) | (mt[kk + 1] & LOWER_MASK)
            mt[kk] = mt[kk + M] ^ (y >> 1) ^ mag01[y & 0x1]
        for kk in xrange(kk, N):
            y = (mt[kk] & UPPER_MASK) | (mt[kk + 1] & LOWER_MASK)
            mt[kk] = mt[kk + (M - N)] ^ (y >> 1) ^ mag01[y & 0x1]
        y = (mt[N - 1] & UPPER_MASK) | (mt[0] & LOWER_MASK)
        mt[N - 1] = mt[M - 1] ^ (y >> 1) ^ mag01[y & 0x1]
        mti = 0
    y = mt[mti]
    mti += 1
    y ^= TEMPERING_SHIFT_U(y)
    y ^= TEMPERING_SHIFT_S(y) & TEMPERING_MASK_B
    y ^= TEMPERING_SHIFT_T(y) & TEMPERING_MASK_C
    y ^= TEMPERING_SHIFT_L(y)
    return float(y)/0xffffffffL


def main():
    rangev = 1000000
    start = time.time()
    sgenrand(4357)
    for j in xrange(rangev):
        genrand()
    end = time.time()
    elapsed = end - start
    print u'\x1b[0;32m@ %d runs in %.4f seconds (%.2f per/sec)\x1b[0m\n' \
          % (rangev, elapsed, rangev/elapsed)

main()


def main_lib():
    rangev = 1000000
    start = time.time()
    for j in xrange(rangev):
        random.random()
    end = time.time()
    elapsed = end - start
    print u'\x1b[0;32m@ %d runs in %.4f seconds (%.2f per/sec)\x1b[0m\n' \
          % (rangev, elapsed, rangev/elapsed)


main_lib()