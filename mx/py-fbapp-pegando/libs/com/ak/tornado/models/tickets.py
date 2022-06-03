#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: May 29, 2012, 8:45:04 AM 

from bson.objectid import ObjectId
from com.ak.tornado.models.base import ControlDocument
from com.ak.tornado.models.users import User
from mongoengine import StringField, IntField, Q, ReferenceField, CASCADE

#: -- helpers ------------------------------------------------------------------

__all__ = [
    "TicketLevel",
    "TicketType",
    "Ticket",
]

#: -- models -------------------------------------------------------------------

class TicketLevel(ControlDocument):
    meta = {
        "collection": "ticketlevels",
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
            return TicketLevel.objects(_Q).first()
        except:
            return None
    
    @staticmethod
    def get_by_id(value):
        try:
            _Q = Q(id=ObjectId(value))
            return TicketLevel._get_by__first(_Q)
        except:
            return None
    
    @staticmethod
    def get_by_name(value):
        _Q = Q(name=value)
        return TicketLevel._get_by__first(_Q)
    
    @staticmethod
    def get_all_by_priority(value):
        _Q = ControlDocument.get_status_query()&Q(priority=value)
        return TicketLevel.objects(_Q).all()

#: -----------------------------------------------------------------------------

class TicketType(ControlDocument):
    meta = {
        "collection": "tickettypes",
        "indexes": ["name"]
    }
    
    #: fields
    name = StringField(max_length=32, unique=True)
    
    #: methods
    @staticmethod
    def _get_by__first(query, enabled=True, availabled=True):
        try:
            if not query: 
                raise
            _Q = ControlDocument.get_status_query(enabled, availabled)&query
            return TicketType.objects(_Q).first()
        except:
            return None
    
    @staticmethod
    def get_by_id(value):
        try:
            _Q = Q(id=ObjectId(value))
            return TicketType._get_by__first(_Q)
        except:
            return None
    
    @staticmethod
    def get_by_name(value):
        _Q = Q(name=value)
        return TicketType._get_by__first(_Q)

#: -----------------------------------------------------------------------------

class Ticket(ControlDocument):
    meta = {
        "collection": "tickets",
    }
    
    #: reference
    user_id = ReferenceField(User, CASCADE)
    level_id = ReferenceField(TicketLevel, CASCADE)
    type_id = ReferenceField(TicketType, CASCADE)
    
    #: fields
    menssage = StringField(max_length=5000)

    #: methods
    @staticmethod
    def get_by_id(value, enabled=True, availabled=True):
        try:
            _Q = ControlDocument.get_status_query(enabled, availabled)&\
                 Q(id=ObjectId(value))
            return Ticket.objects(_Q).first()
        except: 
            return None
    
    @staticmethod
    def get_all_by_user(user, ttype=None, tlevel=None):
        _Q = ControlDocument.get_status_query()&Q(user_id=user)
        if ttype and isinstance(ttype, TicketLevel):
            _Q = _Q&Q(type_id=ttype)
        if tlevel and isinstance(tlevel, TicketLevel):
            _Q = _Q&Q(level_id=tlevel)
        return Ticket.objects(_Q).all()
    
    @staticmethod
    def get_all_by_type(value):
        if not value and isinstance(value, TicketType):
            return None
        _Q = ControlDocument.get_status_query()&Q(type_id=value)
        return Ticket.objects(_Q).all()
    
    @staticmethod
    def get_all_by_level(value):
        if not value and isinstance(value, TicketLevel):
            return None
        _Q = ControlDocument.get_status_query()&Q(level_id=value)
        return Ticket.objects(_Q).all()
    
#: -----------------------------------------------------------------------------
