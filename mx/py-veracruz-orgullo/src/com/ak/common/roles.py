#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Jan 4, 2013 1:27:47 PM

class Role():
    
    __perms_read  = 1 << 0
    __perms_write = 1 << 16
    __perms_admin = 1 << 32
    
    def __init__(self, name, write=False, admin=False, level=0):
        if not hasattr(Role, "_roles"):
            Role._roles = dict()

        self._name = name
        self._level = level
        self._perms = self.__perms_read

        if write:
            self._perms = self._perms\
                        | self.__perms_write

        if admin:
            self._perms = self._perms\
                        | self.__perms_write\
                        | self.__perms_admin

        if level != 0:
            self._perms = self._perms\
                        | level

        if not Role._roles.has_key(name):
            Role._roles[name] = self
            
    @property
    def name(self):
        return self._name if hasattr(self, "_name") else None

    @property
    def permissions(self):
        return self._perms if hasattr(self, "_perms") else -1

    @property
    def is_admin(self):
        return self.permissions >= self.__perms_admin

    @property
    def is_writer(self):
        return self.permissions >= self.__perms_write

    @property
    def is_reader(self):
        return self.permissions >= self.__perms_read

    @staticmethod
    def get_roles():
        return Role._roles.copy()

    @staticmethod
    def get_role(key=None):
        if key and Role._roles.has_key(key):
            return Role._roles.get(key)
        return None

    @staticmethod
    def get_role_by_value(rid=None):
        if rid and Role._roles:
            for r in Role._roles.items():
                if r[1].permissions == rid:
                    return r[1]
        return None

    @staticmethod
    def get_admin_value():
        return Role.__perms_admin

    @staticmethod
    def get_writer_value():
        return Role.__perms_write

    @staticmethod
    def get_reader_value():
        return Role.__perms_read

    def __repr__(self):
        return str(dict(name=self.name, permissions=self.permissions))
    