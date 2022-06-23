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

#: -----------------------------------------------------------------------------

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]
        
#: -----------------------------------------------------------------------------

print 
print 'DATABASE'
print '---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----'

User.drop_collection()

print "EXEC: user-sysadmin"
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
    # --
    u = User()
    u.role = Role('admin', admin=True).permissions;
    u.username = u"sysreport"
    u.password = u"CP#M1nD9+77-"
    u.email = u"alejandro.m.bernardis@gmail.com"
    u.first_name = u"Reporte"
    u.middle_name = u""
    u.last_name = u"Young and Rubicam"
    u.enabled = True
    u.save()
except Exception as E:
    print "ERROR", E
print " END: user-sysadmin"

#: -----------------------------------------------------------------------------

Code.drop_collection()

print "EXEC: codes-accesories"
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
                print "ERROR", E, code.token
except Exception as E:
    print "ERROR", E
print " END: codes-accesories"

print "EXEC: codes-flyers"
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
                print "ERROR", E, code.token
except Exception as E:
    print "ERROR", E
print " END: codes-flyers"

print "EXEC: codes-100"
try:
    f_name = ('%s/codes_list_20120510_134233324076_100.csv' % base_path)
    with open(f_name, 'rb') as f:
        ref = unicode_csv_reader(f)
        for row in ref:
            try:
                code = Code()
                code.token = row[0]
                code.category = 4
                code.points = 2
                code.enabled = True
                code.availabled = bool(row[1] == "1")
                code.created = datetime.datetime.now()
                code.save()
            except Exception as E:
                print "ERROR", E, code.token
except Exception as E:
    print "ERROR", E
print " END: codes-100"

print "EXEC: codes-twitter"
try:
    f_name = ('%s/codes_list_20120517_163356875310_twitter.csv' % base_path)
    with open(f_name, 'rb') as f:
        ref = unicode_csv_reader(f)
        for row in ref:
            try:
                code = Code()
                code.token = row[0]
                code.category = 3
                code.points = 2
                code.enabled = True
                code.availabled = bool(row[1] == "1")
                code.created = datetime.datetime.now()
                code.save()
            except Exception as E:
                print "ERROR", E, code.token
except Exception as E:
    print "ERROR", E
print " END: codes-twitter"

#: -----------------------------------------------------------------------------

Location.drop_collection()

print "EXEC: locations"
try:
    Location.drop_collection()
    with open('%s/locations.csv' % base_path, 'rb') as f:
        ref = unicode_csv_reader(f)
        for row in ref:
            try:
                location = Location()
                location.pid = int(row[0])
                location.name = row[1]
                location.enabled = True
                location.save()
            except Exception as E:
                print "ERROR", E, location.pid
except Exception as E:
    print "ERROR", E
print " END: locations"

#: -----------------------------------------------------------------------------

print 
print 'RESULTS'
print '---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----'
print "+ Users", User.objects.count()    
print "+ Codes", Code.objects.count()
print "+ Locations", Location.objects.count()
Product.drop_collection()
print "- Product", Product.objects.count()
ProductTicket.drop_collection()
print "- ProductTicket", ProductTicket.objects.count()
GamePoint.drop_collection()
print "- GamePoint", GamePoint.objects.count()
Points.drop_collection()
print "- Points", Points.objects.count()
LegalAudit.drop_collection()
print "- LegalAudit", LegalAudit.objects.count()
print
print

#: -----------------------------------------------------------------------------

    
