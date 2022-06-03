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

from random import randint, sample
from com.ak.tornado.models.users import User
from com.ak.tornado.security import token
from mx.yr.henkel.resistol.fbapp.pegando.models import History

latlng = [
    (19.4326077,-99.13320799999997),
    (41.8781136,-87.62979819999998),
    (23.634501,-102.55278399999997),
    (46.227638,2.213749000000007),
    (20.97,-89.62),
    (19.4326077,-99.13320799999997),
    (21.158964,-86.84593699999999),
    (23.634501,-102.55278399999997),
    (40.7143528,-74.0059731),
    (19.4326077,-99.13320799999997),
    (20.628505,-87.07975199999998),
    (19.4326077,-99.133208),
    (19.4326077,-99.13320799999997),
    (19.6,-99.05000000000001),
    (41.9211423,-87.80922659999999),
    (23.634501,-102.55278399999997),
    (41.9211423,-87.80922659999999),
    (23.634501,-102.55278399999997),
    (19.4326077,-99.13320799999997)
]

histories = [
"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec et augue orci, ut fermentum tellus. Sed venenatis sem et nibh vestibulum sed lacinia libero fringilla. Sed et lorem lorem, eget egestas sem. Aliquam felis est, laoreet consequat dapibus et, iaculis vel arcu. Cras quis est eget eros tincidunt tempor sed eu lorem. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nam dolor orci, pharetra quis accumsan quis, blandit non mauris. Sed viverra odio at neque ultricies nec tincidunt nibh imperdiet. Ut a quam sem. Etiam malesuada laoreet enim, ac condimentum turpis rhoncus non.",
"Suspendisse auctor nisi aliquet leo malesuada ultricies. Suspendisse lobortis blandit sem, in posuere velit pretium ac. Pellentesque faucibus est vel odio sagittis vitae condimentum nisl ullamcorper. Donec convallis adipiscing varius. Aliquam non consequat urna. Suspendisse sodales rhoncus diam sed auctor. Praesent gravida sodales arcu vel placerat. Pellentesque posuere, leo gravida commodo imperdiet, odio augue eleifend ante, vitae accumsan est metus at nulla. Donec vel odio sem, vitae consequat elit. Sed ullamcorper, velit et bibendum lacinia, risus turpis fringilla sem, non faucibus nisl ligula vel felis. Duis urna massa, sagittis eu vehicula a, accumsan vitae dui. Suspendisse id augue nec nisi iaculis placerat. Cras sit amet arcu velit.",
"Pellentesque elit velit, sagittis scelerisque cursus eu, pretium vel risus. Quisque tincidunt, neque sed auctor interdum, risus neque convallis enim, id feugiat dolor odio nec quam. Sed quis sapien pulvinar ipsum vestibulum fringilla at sed felis. Cras in lorem id erat aliquet porta. Aliquam erat volutpat. Morbi sem ante, dignissim vitae convallis id, pretium sed metus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Morbi sodales dui ut ligula dapibus malesuada. Donec molestie tellus turpis. Praesent leo lorem, fringilla in suscipit vitae, gravida ut tellus. Nam lacinia porttitor eros at ornare. Nullam ullamcorper lorem vel justo mollis eu facilisis enim iaculis. Curabitur ipsum neque, vulputate eget venenatis non, ultricies vulputate tellus. Sed sed libero vitae leo eleifend convallis at ut velit."
]

emails = [
    "alejandro.bernardis@gmail.com",
    "polly.jex@gmail.com",
    "berna@gmail.com",
    "carla.a@gmail.com",
]

user = User.get_by_username("sysadmin")
History.drop_collection()

for a in range(101):
    t = token();
    c = randint(1,3)
    m_lat, m_lng = sample(latlng, 1)[0]
    f_lat, f_lng = sample(latlng, 1)[0]
    history = History()
    history.email = sample(emails, 1)[0]
    history.token = token()
    history.my_name = "Manuel"
    history.my_location_x = m_lat
    history.my_location_y = m_lng
    history.my_photo = "/static/img/fake2.jpg"
    history.friend_fbuid = token()
    history.friend_name = "Sofia"
    history.friend_location_x = f_lat
    history.friend_location_y = f_lng
    history.friend_photo = "/static/img/fake.jpg"
    history.history_category = c
    history.history_category_name = history.get_category(c)
    history.history_detail = sample(histories, 1)[0]
    history.history_location = u"en el trabajo"
    history.image_01 = '/static/img/fake3.jpg'
    history.image_02 = '/static/img/fake4.jpg'
    history.image_03 = '/static/img/fake5.jpg'
    history.enabled = True
    history.availabled = True
    history.save()
    print history.token
print History.objects.count()


