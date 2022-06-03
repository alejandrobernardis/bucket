#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Aug 7, 2012, 12:30:23 PM


#: -- bootstrap ----------------------------------------------------------------

import os, sys
p_root = os.path.abspath("../")
sys.path.insert(0, p_root+"/libs")
sys.path.insert(1, p_root+"/src")

#: -----------------------------------------------------------------------------

import csv
from mongoengine import connect

#: -----------------------------------------------------------------------------

connect("henkel_resistol_fbapp0001", host="localhost", port=27017,
        username=u"sysadmin", password=u"yrHK+R1nD0M0!71+")

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

_sep = "#: -----------------------------------------------------------------------------"

#: -----------------------------------------------------------------------------

from com.ak.tornado.models.users import User, UserGender, UserRole
from com.ak.tornado.security import Role, token

#: -----------------------------------------------------------------------------
"""
print
print "#: GENDER..."
print _sep

try:
    user_gender_list = [('male', 1),
                        ('female', 2)]

    UserGender.drop_collection()

    for _name, _uid in user_gender_list:
        gender = UserGender()
        gender.uid = _uid
        gender.name = _name
        gender.enabled = True
        gender.availabled = True
        gender.save()
        print gender.uid, gender.name

    print
    print "Total:", UserGender.objects.count()

except Exception as E:
    print "Error:", str(E)

#: -----------------------------------------------------------------------------

print
print "#: ROLES..."
print _sep

try:
    user_role_list = [('admin', False, True),
                      ('moderator', True, False),
                      ('user', False, False)]

    UserRole.drop_collection()

    for _name, _write, _admin in user_role_list:
        r = Role(_name, _write, _admin, 0)
        role = UserRole()
        role.name = r.name
        role.permissions = r.permissions
        role.admin = _admin
        role.write = _write
        role.level = 0
        role.read = True
        role.enabled = True
        role.availabled = True
        role.save()
        print role.name, role.permissions, role.admin

    print
    print "Total:", UserRole.objects.count()

except Exception as E:
    print "Error:", str(E)
"""
#: -----------------------------------------------------------------------------

print
print "#: USERS..."
print _sep

try:
    user_list = [(
     'alejandro',
     'manuel',
     'bernardis',
     1,
     'admin',
     'sysadmin',
     'sysadmin',
     'alejandro.bernardis@gmail.com',
     '1469798294'
    )]

    User.drop_collection()

    for _fn, _mn, _ln, _g, _r, _u, _p, _e, _fbuid in user_list:
        #role = UserRole.get_by_name(_r)
        #gender = UserGender.get_by_uid(_g)
        user = User()
        user.token = token()
        user.facebook_uid = _fbuid
        user.first_name = _fn
        user.middle_name = _mn
        user.last_name = _ln
        #user.gender = gender
        user.username = _u
        user.password = _p
        user.email = _e
        #user.role = role
        user.availabled = True
        user.enabled = True
        user.save()

        print user.first_name, user.last_name, user.username
        print user.to_object()

    print
    print "Total:", User.objects.count()

except Exception as E:
    print "Error:", str(E)

