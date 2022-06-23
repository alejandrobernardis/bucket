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

#: helper

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

#: dataentry

Code.drop_collection()

try:
    f_name = ('%s/codes_list_20120411_132400974959_accesorios.csv' % base_path)
    with open(f_name, 'rb') as f:
        ref = unicode_csv_reader(f)
        for row in ref:
            try:
                code = Code()
                code.token = row[0]
                code.category = 1
                code.points = 3
                code.enabled = True
                code.availabled = bool(row[1] == "1")
                code.created = datetime.datetime.now()
                code.save()
            except Exception as E:
                print "ERROR", code.token
            #print code.to_object()
except Exception as E:
    print E
    
try:
    f_name = ('%s/codes_list_20120409_131125383928_flyers.csv' % base_path)
    with open(f_name, 'rb') as f:
        ref = unicode_csv_reader(f)
        for row in ref:
            try:
                code = Code()
                code.user_id = None
                code.token = row[0]
                code.category = 2
                code.points = 2
                code.enabled = True
                code.availabled = bool(row[1] == "1")
                code.created = datetime.datetime.now()
                code.save()
            except Exception as E:
                print "ERROR", code.token
            #print print code.to_object()
except Exception as E:
    print E
    
    
    
    
    
