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

import csv, datetime
from mongoengine import connect
from mx.yr.xxx.luminous.landing.models import Code

#: -----------------------------------------------------------------------------

connect("xxx_luminous_landing", host="localhost", port=27017,
        username=u"sysadmin", password=u"yrCP+M0nD8!13+")

#: -----------------------------------------------------------------------------

base_dir = os.path.dirname(__file__)
base_path = os.path.join(base_dir, "dataentry")

#: -----------------------------------------------------------------------------

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]
        
#: -----------------------------------------------------------------------------

print 
print 'DATABASE'
print '---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----'

print "EXEC: codes-flyers"
try:
    f_name = ('%s/codes_list_20120509_124530383928_flyers.csv' % base_path)
    with open(f_name, 'rb') as f:
        ref = unicode_csv_reader(f)
        for row in ref:
            try:
                code = Code.objects(token=row[0]).first()
                if code:
                    print (code.token == row[0]), code.to_object()
                    code.update(
                        set__enabled=True,
                        set__availabled=True,
                        set__modified=datetime.datetime.now())
                    code.reload();
                    print " - -", code.to_object()
            except Exception as E:
                print "ERROR", E, code.token
except Exception as E:
    print "ERROR", E
print " END: codes-flyers"

#: -----------------------------------------------------------------------------

print 
print 'RESULTS'
print '---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----'
print "+ Codes", Code.objects(availabled=True).count()

#: -----------------------------------------------------------------------------

    
