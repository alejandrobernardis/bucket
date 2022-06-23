#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Mar 31, 2012, 1:17:25 AM 

import datetime
from bson.objectid import ObjectId
from mongoengine import Document, StringField, DateTimeField, BooleanField, \
                        IntField, ReferenceField, CASCADE, Q
from mx.yr.tornado.models import User, get_date_compare
from mx.yr.tornado.utils import datetime_to_str

#: -- helpers ------------------------------------------------------------------

__all__ = [
    "Code",
    "ProductTicket",
    "Product",
    "GamePoint",
    "Points",
]

#: -- models -------------------------------------------------------------------

class Code(Document):
    meta = {
        'collection': 'codes',
        'indexes': ['user_id', 'token'],
        'ordering': ['-modified'],
    }
    
    #: const
    
    __category_accesorio = [1,3,"Accesorios"]
    __category_flyer     = [2,2,"Flyer"]
    __category_twitter   = [3,2,"Twitter"]
    __category_100       = [4,2,"Auditoria"]
    
    #: fields
    
    user_id = ReferenceField(User, CASCADE)
    token = StringField(max_length=8, unique=True)
    category = IntField(default=0)
    points = IntField(default=0)
    enabled = BooleanField(default=False)
    availabled = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.now)
    modified = DateTimeField(default=datetime.datetime.now)
    
    #: methods
    
    def __get_category(self, index=0):
        ref = ["Not Found",
               self.__category_accesorio, 
               self.__category_flyer,
               self.__category_twitter,
               self.__category_100]
        try:
            return ref[self.category][index]
        except Exception:
            return ref[0]
    
    def get_category(self):
        return self.__get_category(2)
    
    def get_points(self):
        return self.__get_category(1)
    
    def is_modified(self):
        return (self.created < self.modified)
    
    def set_status(self, user, status):
        try:
            if not self.availabled:
                return None    
            self.update(set__user_id=user,
                        set__enabled=status, 
                        set__modified=datetime.datetime.now())
            self.reload()
            return self
        except Exception:
            return None
    
    #: helpers
    
    @staticmethod
    def get_by_id(oid, only_enabled=False):
        try:
            _Q = Q(id=ObjectId(oid=oid))&Q(availabled=True)
            if only_enabled:
                _Q = _Q&Q(enabled=True)
            return Code.objects(_Q).first()
        except Exception:
            return None
    
    @staticmethod
    def get_by_token(token, only_enabled=False):
        try:
            _Q = Q(token=token)&Q(availabled=True)
            if only_enabled:
                _Q = _Q&Q(enabled=True)
            return Code.objects(_Q).first()
        except Exception:
            return None
    
    @staticmethod
    def set_code_status(oid, user, status=False):
        try:
            code = Code.objects(Q(id=ObjectId(oid=oid))&
                                Q(token=oid)&
                                Q(availabled=True)).first()
            return code.set_status(user, status)
        except Exception:
            return None
    
    @staticmethod
    def get_codes_by_user(user, category=0):
        try:
            _Q = Q(user_id=user)&Q(availabled=True)&Q(enabled=False)
            if category > 0:
                _Q = _Q&Q(category=category)
            return Code.objects(_Q).all()
        except Exception:
            return -1
        
    @staticmethod
    def get_points_by_user(user, category=0):
        try:
            _Q = Q(user_id=user)&Q(availabled=True)&Q(enabled=False)
            if category > 0:
                _Q = _Q&Q(category=category)
            return Code.objects(_Q).sum("points") or 0
        except Exception:
            return -1
        
    @staticmethod
    def get_total_by_user(user, category=0):
        try:
            _Q = Q(user_id=user)&Q(availabled=True)&Q(enabled=False)
            if category > 0:
                _Q = _Q&Q(category=category)
            return Code.objects(_Q).count()
        except Exception:
            return -1
        
    #: -- today --
    
    @staticmethod
    def get_points_by_user_today(user, category=0):
        try:
            _date = get_date_compare()
            _Q = Q(user_id=user)&Q(availabled=True)&Q(enabled=False)&\
                 Q(modified__lt=_date.max)&Q(modified__gt=_date.min)
            if category > 0:
                _Q = _Q&Q(category=category)
            return Code.objects(_Q).sum("points") or 0
        except Exception:
            return -1
        
    @staticmethod
    def get_total_by_user_today(user, category=0):
        try:
            _date = get_date_compare()
            _Q = Q(user_id=user)&Q(availabled=True)&Q(enabled=False)&\
                 Q(modified__lt=_date.max)&Q(modified__gt=_date.min)
            if category > 0:
                _Q = _Q&Q(category=category)
            return Code.objects(_Q).count()
        except Exception:
            return -1
        
    #: to_object
    
    def to_object(self):
        user = None if not self.user_id else self.user_id.id
        return dict(
            user_id=str(user),
            token=self.token,
            category=self.get_category(),
            category_id=self.category,
            points=self.points,
            enabled=self.enabled,
            availabled=self.availabled,
            created=datetime_to_str(self.created),
            modified=datetime_to_str(self.modified),)
        
#: -----------------------------------------------------------------------------

class ProductTicket(Document):
    meta = {
        'collection': 'producttickets',
        'indexes': ['user_id', 'token'],
        'ordering': ['-modified'],
    }
    
    #: fields
    
    user_id = ReferenceField(User, CASCADE)
    token = StringField(max_length=32)
    rfc = StringField(max_length=32)
    date_and_time = DateTimeField()
    enabled = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.now)
    modified = DateTimeField(default=datetime.datetime.now)
    
    #: methods
    
    def is_modified(self):
        return (self.created < self.modified)
    
    #: helpers
    
    @staticmethod
    def get_by_user(user, only_enabled=False):
        try:
            _Q = Q(user_id=user)
            if only_enabled:
                _Q = _Q&Q(enabled=True)
            return ProductTicket.objects(_Q).all()
        except Exception:
            return None
    
    @staticmethod
    def get_by_token(token, only_enabled=False):
        try:
            _Q = Q(token=token)
            if only_enabled:
                _Q = _Q&Q(enabled=True)
            return ProductTicket.objects(_Q).all()
        except Exception:
            return None
    
    @staticmethod
    def get_user_by_token(user, token, only_enabled=False):
        try:
            _Q = Q(user_id=user)&Q(token=token)
            if only_enabled:
                _Q = _Q&Q(enabled=True)
            return bool(ProductTicket.objects(_Q).first() != None)
        except Exception:
            return True
    
    @staticmethod
    def get_total_by_user(user, only_enabled=False):
        try:
            _Q = Q(user_id=user)
            if only_enabled:
                _Q = _Q&Q(enabled=True)
            return ProductTicket.objects(_Q).count()
        except Exception:
            return -1
    
    @staticmethod
    def get_total_by_token(token, only_enabled=False):
        try:
            _Q = Q(token=token)
            if only_enabled:
                _Q = _Q&Q(enabled=True)
            return ProductTicket.objects(_Q).count()
        except Exception:
            return -1
        
    #: -- today --
    
    @staticmethod
    def get_total_by_user_today(user):
        try:
            _date = get_date_compare()
            _Q = Q(user_id=user)&Q(enabled=False)&\
                 Q(created__lt=_date.max)&Q(created__gt=_date.min)
            return Code.objects(_Q).count()
        except Exception:
            return -1
    
    #: to_object
    
    def to_object(self):
        user = None if not self.user_id else self.user_id.id
        return dict(
            user_id=str(user),
            token=self.token,
            enabled=self.enabled,
            created=datetime_to_str(self.created),
            modified=datetime_to_str(self.modified),)

class Product(Document):
    meta = {
        'collection': 'products',
        'indexes': ['ticket_id'],
        'ordering': ['-modified'],
    }
    
    #: const
    
    QUANTITY_MAX = 50
    CATEGORY_MIN = 1
    CATEGORY_MAX = 3
    
    __category_cepillo  = [1,5,"Cepillo"]
    __category_pasta    = [2,3,"Pasta"]
    __category_enjuague = [3,7,"Enjuague"]
    
    #: fields
    
    ticket_id = ReferenceField(ProductTicket, CASCADE)
    category = IntField(default=0)
    quantity = IntField(default=0)
    points = IntField(default=0)
    enabled = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.now)
    modified = DateTimeField(default=datetime.datetime.now)
    
    #: methods
    
    def __get_category(self, index=0):
        ref = ["Not Found",
               self.__category_cepillo, 
               self.__category_pasta, 
               self.__category_enjuague]
        try:
            return ref[self.category][index]
        except Exception:
            return ref[0]
    
    def get_category(self):
        return self.__get_category(2)
    
    def get_points(self):
        return self.__get_category(1)
    
    def is_modified(self):
        return (self.created < self.modified)
    
    #: helpers
    
    @staticmethod
    def validate_category(category):
        return bool(category >= Product.CATEGORY_MIN and 
                    category <= Product.CATEGORY_MAX)
        
    @staticmethod
    def validate_quantity(quantity):
        return bool(quantity <= Product.QUANTITY_MAX)
    
    @staticmethod
    def get_all(ticket, category=0, only_enabled=False):
        try:
            _Q = Q(ticket_id=ticket)
            if category > 0:
                _Q = _Q&Q(category=category)
            if only_enabled:
                _Q = _Q&Q(enabled=True)
            return Product.objects(_Q).all()
        except Exception:
            return -1
    
    @staticmethod
    def get_points_by_category(ticket, category=0, only_enabled=False):
        try:
            _Q = Q(ticket_id=ticket)
            if category > 0:
                _Q = _Q&Q(category=category)
            if only_enabled:
                _Q = _Q&Q(enabled=True)
            return Product.objects(_Q).sum("points") or 0
        except Exception:
            return -1
    
    @staticmethod
    def get_total_by_category(ticket, category=0, only_enabled=False):
        try:
            _Q = Q(ticket_id=ticket)
            if category > 0:
                _Q = _Q&Q(category=category)
            if only_enabled:
                _Q = _Q&Q(enabled=True)
            return Product.objects(_Q).sum("quantity") or 0
        except Exception:
            return -1
    
    #: to_object
    
    def to_object(self):
        ticket = None if not self.ticket_id else self.ticket_id.id
        return dict(
            ticket_id=str(ticket),
            category=self.get_category(),
            category_id=self.category,
            quantity=self.quantity,
            points=self.points,
            enabled=self.enabled,
            created=datetime_to_str(self.created),
            modified=datetime_to_str(self.modified),)

#: -----------------------------------------------------------------------------

class GamePoint(Document):
    meta = {
        'collection': 'gamepoints',
        'indexes': ['user_id'],
        'ordering': ['-modified'],
    }
    
    #: fields
    
    user_id = ReferenceField(User, CASCADE)
    points = IntField(default=0)
    enabled = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.now)
    modified = DateTimeField(default=datetime.datetime.now)
    
    #: methods
    
    def is_modified(self):
        return (self.created < self.modified)
    
    #: helpers
    
    @staticmethod
    def get_by_user(user, only_enabled=False):
        try:
            _Q = Q(user_id=user)
            if only_enabled:
                _Q = _Q&Q(enabled=True)
            return GamePoint.objects(_Q).all()
        except Exception:
            return None
        
    @staticmethod
    def get_points_by_user(user, only_enabled=False):
        try:
            _Q = Q(user_id=user)
            if only_enabled:
                _Q = _Q&Q(enabled=True)
            return GamePoint.objects(_Q).sum("points") or 0
        except Exception:
            return -1
    
    @staticmethod
    def get_total_by_user(user, only_enabled=False):
        try:
            _Q = Q(user_id=user)
            if only_enabled:
                _Q = _Q&Q(enabled=True)
            return GamePoint.objects(_Q).count()
        except Exception:
            return -1
        
    #: -- today --
    
    @staticmethod
    def get_points_by_user_today(user):
        try:
            _date = get_date_compare()
            _Q = Q(user_id=user)&Q(enabled=True)&\
                 Q(created__lt=_date.max)&Q(created__gt=_date.min)
            return GamePoint.objects(_Q).sum("points") or 0
        except Exception:
            return -1
        
    @staticmethod
    def get_total_by_user_today(user):
        try:
            _date = get_date_compare()
            _Q = Q(user_id=user)&Q(enabled=True)&\
                 Q(created__lt=_date.max)&Q(created__gt=_date.min)
            return Code.objects(_Q).count()
        except Exception:
            return -1
    
    #: to_object
    
    def to_object(self):
        user = None if not self.user_id else self.user_id.id
        return dict(
            user_id=str(user),
            points=self.points,
            enabled=self.enabled,
            created=datetime_to_str(self.created),
            modified=datetime_to_str(self.modified),)

#: -----------------------------------------------------------------------------

class Points(Document):
    meta = {
        'collection': 'points',
        'indexes': ['user_id'],
        'ordering': ['-modified'],
    }
    
    #: fields
    
    user_id = ReferenceField(User, CASCADE)
    points = IntField(default=0)
    enabled = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.now)
    modified = DateTimeField(default=datetime.datetime.now)

    #: methods
    
    def add_points(self, points):
        try:
            if self.enabled:
                self.update(inc__points=points, 
                            set__modified=datetime.datetime.now())
                self.reload()
                return self.points or 0
            raise 
        except Exception:
            return 0
        
    def is_modified(self):
        return (self.created < self.modified)
    
    #: helpers
        
    @staticmethod
    def add_points_by_user(user, points):
        try:
            ref = Points.objects(Q(user_id=user)).first()
            if not ref:
                ref = Points()
                ref.user_id = user
                ref.enabled = True
                ref.created = datetime.datetime.now()
                ref.save()
            return ref.add_points(points)
        except Exception:
            return 0
        
    @staticmethod
    def get_points_by_user(user):
        try:
            ref = Points.objects(Q(user_id=user)).first()
            return ref.points
        except Exception:
            return 0
    
    #: to_object
    
    def to_object(self):
        user = None if not self.user_id else self.user_id.id
        return dict(
            user_id=str(user),
            points=self.points,
            enabled=self.enabled,
            created=datetime_to_str(self.created),
            modified=datetime_to_str(self.modified),)

#: -----------------------------------------------------------------------------

