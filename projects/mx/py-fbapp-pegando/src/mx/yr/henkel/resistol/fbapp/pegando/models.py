#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Aug 6, 2012, 7:12:21 PM

from bson.objectid import ObjectId
from com.ak.tornado.models.base import ControlDocument
from mongoengine import StringField, IntField, FloatField, Q

#: -----------------------------------------------------------------------------

class History(ControlDocument):
    my_name = StringField()
    my_location_x = FloatField()
    my_location_y = FloatField()
    my_location = StringField()
    my_photo = StringField()
    friend_name = StringField()
    friend_location_x = FloatField()
    friend_location_y = FloatField()
    friend_location = StringField()
    friend_photo = StringField()
    friend_fbuid = StringField()
    history_category = IntField()
    history_category_name = StringField()
    history_location = StringField()
    history_detail = StringField()
    image_01 = StringField()
    image_02 = StringField()
    image_03 = StringField()
    email = StringField()
    token = StringField(unique=True)
    action_token = StringField(unique=True)

    def get_category(self, cid=0):
        if 0 < cid < 4:
            return ["Amistad", "Familia", "Romance"][cid-1]
        return None

    @staticmethod
    def get_by_id(oid, enabled=True, availabled=True):
        try:
            _Q = Q(id=ObjectId(oid=oid))\
                 &Q(enabled=enabled)\
                 &Q(availabled=availabled)
            return History.objects(_Q).first()
        except Exception:
            return None

    @staticmethod
    def get_by_token(token, enabled=True, availabled=True):
        try:
            _Q = Q(token=token)\
                 &Q(enabled=enabled)\
                 &Q(availabled=availabled)
            return History.objects(_Q).first()
        except Exception:
            return None

    @staticmethod
    def get_by_action_token(token, enabled=True, availabled=True):
        try:
            _Q = Q(action_token=token)\
                 &Q(enabled=enabled)\
                 &Q(availabled=availabled)
            return History.objects(_Q).first()
        except Exception:
            return None

    @staticmethod
    def get_paginate_enabled(page_number=1, page_size=50, query=None, category=0):
        _Q = Q(enabled=True)&Q(availabled=True)
        if query:
            _Q = _Q&query
        if not query and category > 0:
            _Q = _Q&Q(history_category=category)
        return History.objects(_Q).skip(page_size*(page_number-1))\
                      .limit(page_size).order_by("-created")

