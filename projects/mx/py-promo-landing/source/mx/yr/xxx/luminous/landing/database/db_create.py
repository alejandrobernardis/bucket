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
from mx.yr.xxx.luminous.landing.models import *
from mx.yr.tornado.security import Role
from mx.yr.tornado.models import LegalAudit, Location, User

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
        
def to_unicode(value):
    if isinstance(value, unicode):
        return value.encode("utf-8")
    return value
#: dataentry

User.drop_collection()
try:
    u = User()
    u.role = Role('admin', admin=True).permissions;
    u.username = u"sysadmin"
    u.password = u"CP+M0nD8#13$"
    u.email = u"alejandro.bernardis@gmail.com"
    u.first_name = u"Alejandro"
    u.middle_name = u"M"
    u.last_name = u"Bernardis"
    u.enabled = True
    u.save()
except Exception as E:
    print E
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
                print code.token
            except Exception as E:
                print "ERROR", code.token
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
                print code.token
            except Exception as E:
                print "ERROR", code.token
except Exception as E:
    print E
Location.drop_collection()
try:
    Location.drop_collection()
    with open('%s/locations.csv' % base_path, 'rb') as f:
        ref = unicode_csv_reader(f)
        for row in ref:
            try:
                location = Location()
                location.pid = int(row[0])
                location.name = to_unicode(str(row[1]))
                location.enabled = True
                location.save()
                #print location.name
            except Exception as E:
                print "ERROR", location.pid, E
except Exception as E:
    print E

print '---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----'
print "Users", User.objects.count()    
print "Codes", Code.objects.count()
print "Locations", Location.objects.count()
print '---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----'
Product.drop_collection()
print "Product", Product.objects.count()
ProductTicket.drop_collection()
print "ProductTicket", ProductTicket.objects.count()
GamePoint.drop_collection()
print "GamePoint", GamePoint.objects.count()
Points.drop_collection()
print "Points", Points.objects.count()
LegalAudit.drop_collection()
print "LegalAudit", LegalAudit.objects.count()
print '---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----'
    
