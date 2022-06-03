#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Apr 11, 2012, 7:46:10 PM 

#: -- bootstrap ----------------------------------------------------------------

import os, sys
p_root = os.path.abspath("../")
sys.path.insert(0, p_root+"/libs")
sys.path.insert(1, p_root+"/src")

#: -----------------------------------------------------------------------------

from mongoengine import connect

from mx.yr.xxx.luminous.landing.models import *
from mx.yr.tornado.models import User, LegalAudit

#: -----------------------------------------------------------------------------

connect("xxx_luminous_landing", host="localhost", port=27017,
        username=u"sysadmin", password=u"yrCP+M0nD8!13+")

#: -----------------------------------------------------------------------------

try:
    Product.drop_collection()
    print "Product", Product.objects.count()
    
    ProductTicket.drop_collection()
    print "ProductTicket", ProductTicket.objects.count()
    
    Points.drop_collection()
    print "Points", Points.objects.count()
    
    Code.drop_collection()
    print "Code", Code.objects.count()
    
    GamePoint.drop_collection()
    print "GamePoint", GamePoint.objects.count()
    
    LegalAudit.drop_collection()
    print "LegalAudit", LegalAudit.objects.count()
    
    u = User.get_user_by_username("alejandromb")
    u.update(set__enabled=True)
    u.reload()
    print
    print "User:", u.username, "Enabled:", u.enabled
    
except Exception as E:
    print E
