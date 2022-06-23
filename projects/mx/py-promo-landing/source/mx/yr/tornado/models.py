#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Apr 2, 2012, 2:48:31 PM 

import datetime
import re

from bson.objectid import ObjectId
from mx.yr.tornado.utils import datetime_to_str, date_to_str
from mx.yr.tornado.security import secret_key, activation_key, Role, Password
from mongoengine import Document, StringField, IntField, URLField, EmailField,\
                        DateTimeField, BooleanField, Q, ReferenceField, CASCADE

#: -- helpers ------------------------------------------------------------------

__all__ = [
    "User",
    "LegalAudit",
    "Location",
    "DateCompare",
    "get_date_compare",
]

#: -- date compare -------------------------------------------------------------

class DateCompare(object):
    def __init__(self, today, date_min, date_max):
        self.today = today
        self.min   = date_min
        self.max   = date_max

def get_date_compare(date=None):
    now = date or datetime.datetime.now()
    today = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)
    date_min = datetime.timedelta(days=-1) + today
    today = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    date_max = datetime.timedelta(days= 1) + today
    return DateCompare(today, date_min, date_max)

#: -- fields -------------------------------------------------------------------

password_exp = re.compile(r"^sha1\$([A-Z0-9]+)", re.IGNORECASE)

class PasswordField(StringField):
    def __set__(self, instance, value):
        if value and not password_exp.search(str(value)):
            value = Password.generate(str(value))
        StringField.__set__(self, instance, value)
        
#: -- models -------------------------------------------------------------------

class User(Document):
    meta = {
        "collection": "users",
        "indexes": ["token", "facebook_uid", "username"]
    }
    
    #: perms
    __base_role = Role.get_reader_value()
    
    #: gender
    __gender_male = 1
    __gender_female = 2
    
    #: fields
    token = StringField(max_length=64)
    activation_key = StringField(max_length=64)
    activation_key_expire = DateTimeField()
    facebook_uid = StringField(max_length=128)
    username = StringField(min_length=8, max_length=32, required=True, 
                           unique=True)
    password = PasswordField(min_length=8, max_length=128, required=True)
    email = EmailField(max_length=255, required=True, unique=True)
    role = IntField(default=__base_role)
    first_name = StringField(max_length=64)
    middle_name = StringField(max_length=64)
    last_name = StringField(max_length=64)
    birthday = DateTimeField()
    address_state = IntField(default=0)
    phone_lada = IntField(default=0)
    phone_number = IntField(default=0)
    gender = IntField(default=0)
    avatar = URLField()
    remote_ip = StringField(max_length=64)
    secret_question = StringField(max_length=255)
    secret_answer = StringField(max_length=255)
    notes = StringField(max_length=500)
    terms = BooleanField(default=False)
    policy = BooleanField(default=False)
    news = BooleanField(default=False)
    enabled = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.now())
    modified = DateTimeField(default=datetime.datetime.now())
    last_login = DateTimeField(default=datetime.datetime.now())
    
    #: -- properties -----------------------------------------------------------
    
    @property
    def gender_male(self):
        return self.__gender_male
    
    @property
    def gender_female(self):
        return self.__gender_female
    
    def get_gender(self):
        ref = [None, "Male", "Female"]
        try: 
            return ref[self.gender]
        except: return ref[0]
    
    #: -- helpers --------------------------------------------------------------
    
    def __datetime_update(self, key, value):
        try:
            self[key] = value if value else datetime.datetime.now()
            self.save()
            return True
        
        except Exception:
            return False
    
    def set_modified(self, date=None):
        return self.__datetime_update("modified", date)
    
    def set_last_login(self, date=None):
        return self.__datetime_update("last_login", date)
        
    def set_activation_key(self, expire_days=1):
        try:
            self.enabled = False
            self.modified = datetime.datetime.now()
            self.activation_key = activation_key(self.username, self.email)
            self.activation_key_expire = datetime.datetime.now()\
                                       + datetime.timedelta(days=expire_days)
            self.save()
            return True
        
        except Exception:
            return False
        
    def set_activation_key_password(self, password=None):
        try:
            self.enabled = True
            self.modified = datetime.datetime.now()
            self.set_new_password(password)
            return True
        
        except Exception:
            return False
        
    def validate_activation_key(self, key):
        try:            
            if not self.activation_key or not self.activation_key_expire:
                raise
            
            elif self.activation_key_expire < datetime.datetime.today():
                raise
            
            self.modified = datetime.datetime.now()
            self.activation_key = None
            self.activation_key_expire = None
            self.save()
            return True
        
        except Exception:
            return False
        
    def set_new_password(self, password=None):
        try:
            if not password:
                password = secret_key(8)
                
            self.modified = datetime.datetime.now()
            self.password = password
            self.save()
            return True
        
        except Exception:
            return False
        
    def set_disabled(self):
        try:
            self.update(set__enabled=False,
                        set__modified=datetime.datetime.now())
            self.reload()
        except Exception:
            pass
        return True
        
    #: -- output ---------------------------------------------------------------
    
    def _get_gender(self):
        genders = [None, "Male", "Female"]
        try:
            return genders[self.gender]
        except Exception:
            return genders[0]
        
        
    def to_object(self):
        try:
            address_state = Location.get_location(self.address_state).name
        except: address_state = None
        return dict(
            id=str(self.id),
            fbuid=self.facebook_uid,
            username=self.username,
            email=self.email,
            role=self.role,
            first_name=self.first_name,
            last_name=self.last_name,
            gender=self.get_gender(),
            birthday=date_to_str(self.birthday),
            phone_lada=self.phone_lada or 0,
            phone_number=self.phone_number or 0,
            address_state=address_state,)
    
    #: -- auth -----------------------------------------------------------------
    
    @staticmethod
    def auth_login(username, password):
        user = User.objects(Q(enabled=True)&
                            Q(username=username)|Q(email=username)).first()
        auth = Password.check(password, user.password) if user else False
        return user, auth
    
    @staticmethod
    def auth_forgot_password(username):
        try:
            return User.objects(Q(enabled=True)&
                                Q(username=username)|Q(email=username)).first()
        except Exception:
            return None
    
    #: -- user -----------------------------------------------------------------
    
    @staticmethod
    def get_user_complex(uid, only_enabled=False):
        try:
            _Q = Q(facebook_uid=uid)|Q(username=uid)|Q(email=uid)|\
                 Q(token=uid)|Q(activation_key=uid)
            try:
                _QUID = ObjectId(uid)
                _Q = Q(id=_QUID)|_Q
            except: pass
            if only_enabled: 
                _Q = Q(enabled=True)&_Q
            return User.objects(_Q).first()
        except Exception:
            return None
    
    @staticmethod
    def get_user_by_uid(uid, only_enabled=False):
        try:
            _Q = Q(id=ObjectId(uid))
            if only_enabled: 
                _Q = Q(enabled=True)&_Q
            return User.objects(_Q).first()
        except Exception:
            return None
    
    @staticmethod
    def get_user_by_username(username, only_enabled=False):
        try:
            _Q = Q(username=username)
            if only_enabled: 
                _Q = Q(enabled=True)&_Q
            return User.objects(_Q).first()
        except Exception:
            return None
    
    @staticmethod
    def get_user_by_email(email, only_enabled=False):
        try:
            _Q = Q(email=email)
            if only_enabled: 
                _Q = Q(enabled=True)&_Q
            return User.objects(_Q).first()
        except Exception:
            return None
    
    @staticmethod
    def get_user_by_token(token, only_enabled=False):
        try:
            _Q = Q(token=token)
            if only_enabled: 
                _Q = Q(enabled=True)&_Q
            return User.objects(_Q).first()
        except Exception:
            return None
        
    @staticmethod
    def get_user_by_facebook_uid(facebook_uid, only_enabled=False):
        try:
            _Q = Q(facebook_uid=facebook_uid)
            if only_enabled: 
                _Q = Q(enabled=True)&_Q
            return User.objects(_Q).first()
        except Exception:
            return None
    
    @staticmethod
    def get_user_by_activation_key(key, only_enabled=False):
        try:
            _Q = Q(activation_key=key)
            if only_enabled: 
                _Q = Q(enabled=True)&_Q
            return User.objects(_Q).first()
        except Exception:
            return None  
    
    @staticmethod
    def get_users_by_role(role=None, page_number=1, page_size=100, 
                          only_enabled=False):
        try:
            if not role.is_integer():
                role = Role.get_role(role).permissions
            _Q = Q(role=role)
            if only_enabled: 
                _Q = Q(enabled=True)&_Q
            return User.objects(_Q).skip(page_size*(page_number-1))\
                                   .limit(page_size)
        except Exception:
            return None  
    
    @staticmethod
    def set_user_modified(username, date=None, only_enabled=False):
        user = User.get_user_by_username(username, only_enabled)
        return user.set_modified(date)
    
    @staticmethod
    def set_user_last_login(username, date=None, only_enabled=False):
        user = User.get_user_by_username(username, only_enabled)
        return user.set_last_login(date)
    
    @staticmethod
    def set_user_disabled(username):
        return 

#: -----------------------------------------------------------------------------
    
class LegalAudit(Document):
    meta = {
        'collection': 'legalaudit',
        'indexes': ['user_id']
    }
    
    #: fields
    
    user_id = ReferenceField(User, CASCADE)
    menssage = StringField(max_length=500)
    enabled = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.now)
    modified = DateTimeField(default=datetime.datetime.now)
    
    #: helpers
    
    @staticmethod
    def get_total_by_user(user, today=False, only_enabled=False):
        try:
            _Q = Q(user_id=user)
            if today:
                _date = get_date_compare()
                _Q = _Q&Q(modified__lt=_date.max)&Q(modified__gt=_date.min)
            if only_enabled:
                _Q = _Q&Q(enabled=True)
            return LegalAudit.objects(_Q).count() or 0
        except Exception:
            return -1
        
    @staticmethod
    def get_total_by_user_today(user, only_enabled=False):
        try:
            _date = get_date_compare()
            _Q = Q(user_id=user)&\
                 Q(modified__lt=_date.max)&Q(modified__gt=_date.min)
            if only_enabled:
                _Q = _Q&Q(enabled=True)
            return LegalAudit.objects(_Q).count() or 0
        except Exception:
            return -1
        
    @staticmethod
    def set_enabled_by_user(user, today=False):
        try:
            _Q = Q(enabled=True)&Q(user_id=user)
            if today:
                _date = get_date_compare()
                _Q = _Q&Q(modified__lt=_date.max)&Q(modified__gt=_date.min)
            LegalAudit.objects(_Q).update(set__enabled=False)
            return True
        except Exception:
            return False
    
    #: to_object
    
    def to_object(self):
        user = None if not self.user_id else self.user_id.id
        return dict(
            user_id=str(user),
            menssage=self.menssage,
            enabled=self.enabled,
            created=datetime_to_str(self.created),
            modified=datetime_to_str(self.modified),)
    
#: -----------------------------------------------------------------------------    

class Location(Document):
    meta = {
        'collection': 'locations',
        'indexes': ['pid'],
    }
    
    #: fields
    
    pid = IntField()
    name = StringField(max_length=128)
    enabled = BooleanField(default=False)
    
    #: helpers
    
    @staticmethod
    def get_location(pid=None):
        try:
            if not pid:
                return Location.objects(enabled=True).all()
            return Location.objects(Q(enabled=True)&Q(pid=pid)).first()
        except Exception:
            return None
        
    @staticmethod
    def get_id_by_name(name=None):
        try:
            if not name:
                return Location.objects(enabled=True).all()
            loc = Location.objects(Q(enabled=True)&Q(name=name)).first()
            return loc.pid
        except Exception:
            return None
        
    @staticmethod
    def get_html_options():
        try:
            code = '<option value="0">--</option>'
            for a in Location.objects(enabled=True).all():
                code += '<option value="%s">%s</option>' % (a.pid, a.name)
            return code
        except Exception:
            return None
        
    #: to_object
    
    def to_object(self):
        return dict(pid=self.pid, name=self.name, enabled=self.enabled)
    