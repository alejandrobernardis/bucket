#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Apr 3, 2012, 3:45:45 PM 

#: -- bootstrap ----------------------------------------------------------------

import os, sys
p_root = os.path.abspath("../")
sys.path.insert(0, p_root+"/libs")
sys.path.insert(1, p_root+"/src")

#: -----------------------------------------------------------------------------

from mongoengine import connect

from mx.yr.tornado.models import User, LegalAudit

#: -----------------------------------------------------------------------------

connect("xxx_luminous_landing", host="localhost", port=27017,
        username=u"sysadmin", password=u"yrCP+M0nD8!13+")

#: -----------------------------------------------------------------------------

try:
    user = User.get_user_by_username("alejandromb")
    legal = LegalAudit.set_enabled_by_user(user, True)
    print "Audit:", legal, "Total:", \
        LegalAudit.get_total_by_user(user, only_enabled=True)
except Exception as E:
    print E
