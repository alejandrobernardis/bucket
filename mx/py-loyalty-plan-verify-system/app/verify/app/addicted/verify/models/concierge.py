#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 23/Feb/2014 00:49


from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class ConciergeUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    added = Column(DateTime)
    modified = Column(DateTime)
    access_level = Column(Integer)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    password = Column(String)
    active = Column(Integer)
    news = Column(String)
    email_balance = Column(String)
    recovery = Column(String)
    recovery_expiration = Column(DateTime)


class ConciergeContact(Base):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    telephone = Column(String)
    mobile = Column(String)
    gender = Column(String)
    birthday = Column(DateTime)
    street = Column(String)
    exterior = Column(String)
    interior = Column(String)
    postal_code = Column(Integer)
    estado = Column(String)
    municipio = Column(String)
    colonia = Column(String)
    email2 = Column(String)


class ConciergeCard(Base):
    __tablename__ = 'card'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    number = Column(String)
    level = Column(Integer)
    assigned = Column(DateTime)
    updated = Column(DateTime)
    active = Column(Integer)
