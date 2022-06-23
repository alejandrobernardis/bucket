#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: May 29, 2012, 8:49:10 AM 

from bson.objectid import ObjectId
from com.ak.tornado.models.base import ControlDocument
from com.ak.tornado.models.users import User
from mongoengine import StringField, IntField, Q, ReferenceField, CASCADE

#: -- helpers ------------------------------------------------------------------

__all__ = [
    "LogLevel",
    "Log",
]

#: -- models -------------------------------------------------------------------

class LogLevel(ControlDocument):
    meta = {
        "collection": "loglevels",
        "indexes": ["name"]
    }
    
    #: fields
    name = StringField(max_length=32, unique=True)
    priority = IntField(default=0)
    
    #: methods
    @staticmethod
    def _get_by__first(query, enabled=True, availabled=True):
        try:
            if not query: 
                raise
            _Q = ControlDocument.get_status_query(enabled, availabled)&query
            return LogLevel.objects(_Q).first()
        except:
            return None
    
    @staticmethod
    def get_by_id(value):
        try:
            _Q = Q(id=ObjectId(value))
            return LogLevel._get_by__first(_Q)
        except:
            return None
    
    @staticmethod
    def get_by_name(value):
        _Q = Q(name=value)
        return LogLevel._get_by__first(_Q)
    
    @staticmethod
    def get_all_by_priority(value):
        _Q = ControlDocument.get_status_query()&Q(priority=value)
        return LogLevel.objects(_Q).all()

#: -----------------------------------------------------------------------------

class Log(ControlDocument):
    meta = {
        "collection": "logs",
        "indexes": ["user_id", "level_id"]
    }
    
    #: reference
    user_id = ReferenceField(User, CASCADE)
    level_id = ReferenceField(LogLevel, CASCADE)
    
    #: fields
    menssage = StringField(max_length=2500)
    
    #: methods
    @staticmethod
    def get_by_id(value, enabled=True, availabled=True):
        try:
            _Q = ControlDocument.get_status_query(enabled, availabled)&\
                 Q(id=ObjectId(value))
            return Log.objects(_Q).first()
        except: 
            return None
    
    @staticmethod
    def get_all_by_user(user, level=None):
        _Q = ControlDocument.get_status_query()&Q(user_id=user)
        if level and isinstance(level, LogLevel):
            _Q = _Q&Q(level_id=level)
        return Log.objects(_Q).all()
    
    @staticmethod
    def get_all_by_level(value):
        if not value and isinstance(value, LogLevel):
            return None
        _Q = ControlDocument.get_status_query()&Q(level_id=value)
        return Log.objects(_Q).all()
    
#: -----------------------------------------------------------------------------
