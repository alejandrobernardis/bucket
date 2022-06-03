#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Apr 11, 2012, 12:10:36 PM 

#: -- bootstrap ----------------------------------------------------------------

import os, sys
p_root = os.path.abspath("../")
sys.path.insert(0, p_root+"/libs")
sys.path.insert(1, p_root+"/src")

#: -----------------------------------------------------------------------------

from mongoengine import connect
from mx.yr.xxx.luminous.landing.models import Product

#: -----------------------------------------------------------------------------

connect("xxx_luminous_landing", host="localhost", port=27017,
        username=u"sysadmin", password=u"yrCP+M0nD8!13+")

#: -----------------------------------------------------------------------------

base_dir = os.path.dirname(__file__)
base_path = os.path.join(base_dir, "dataentry")

#: -----------------------------------------------------------------------------

print 
print 'DATABASE'
print '---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----'

print "EXEC: products-change"
try:
    _total = Product.objects().count()
    _t12 = Product.objects(category=1).count()
    _t21 = Product.objects(category=2).count()
    _skip = 0
    _limit = 100
    _range = int(_total/_limit)+1
    i = 0
    for a in range(_range):
        recorset = Product.objects().skip(_skip*_limit).limit(_limit)
        for b in recorset:
            if b.category < 3:
                print b.id, b.category,
                b.update(set__category = 1 if b.category == 2 else 2)
                b.reload()
                print b.category
                i += 1
        _skip += 1
except Exception as E:
    print "ERROR", E
print " END: products-change"

#: -----------------------------------------------------------------------------

print 
print 'RESULTS'
print '---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----'
print 'pasta 1 to 2', _t12, Product.objects(category=2).count()
print 'cepillo 2 to 1', _t21, Product.objects(category=1).count()

#: -----------------------------------------------------------------------------

    
