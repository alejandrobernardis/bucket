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

from mx.yr.tornado.models import User
from mx.yr.tornado.security import Role

#: -----------------------------------------------------------------------------

connect("xxx_luminous_landing", host="localhost", port=27017,
        username=u"sysadmin", password=u"yrCP+M0nD8!13+")

#: -----------------------------------------------------------------------------

try:
    # db.users.update({username: 'alejandromb'}, {$set:{enabled: true}});
    User.drop_collection()
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
