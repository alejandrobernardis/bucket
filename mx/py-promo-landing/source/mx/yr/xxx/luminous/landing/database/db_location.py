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

import csv
from mongoengine import connect
from mx.yr.tornado.models import Location

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

states_list = [
    [1, u"Aguascalientes"],
    [2, u"Baja California Norte"],
    [3, u"Baja California Sur"],
    [4, u"Campeche"],
    [5, u"Chiapas"],
    [6, u"Chihuahua"],
    [7, u"Coahuila"],
    [8, u"Colima"],
    [9, u"Distrito Federal"],
    [10, u"Durango"],
    [11, u"Guanajuato"],
    [12, u"Guerrero"],
    [13, u"Hidalgo"],
    [14, u"Jalisco"],
    [15, u"México"],
    [16, u"Michoacán de Ocampo"],
    [17, u"Morelos"],
    [18, u"Nayarit"],
    [19, u"Nuevo León"],
    [20, u"Oaxaca"],
    [21, u"Puebla"],
    [22, u"Querétaro"],
    [23, u"Quintana Roo"],
    [24, u"San Luis Potosí"],
    [25, u"Sinaloa"],
    [26, u"Sonora"],
    [27, u"Tabasco"],
    [28, u"Tamaulipas"],
    [29, u"Tlaxcala"],
    [30, u"Veracruz"],
    [31, u"Yucatán"],
    [32, u"Zacatecas"]
] 

try:
    Location.drop_collection()
    with open('%s/locations.csv' % base_path, 'rb') as f:
        ref = unicode_csv_reader(f)
        for row in ref:
            try:
                location = Location()
                location.pid = int(row[0])
                location.name = str(row[1])
                location.enabled = True
                location.save()
            except Exception as E:
                print "ERROR", location.pid, E
            print location.to_object()
except Exception as E:
    print E
