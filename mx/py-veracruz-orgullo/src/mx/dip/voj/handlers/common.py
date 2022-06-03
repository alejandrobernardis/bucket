#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Jan 4, 2013 1:09:27 PM

#: imports
import datetime
from com.ak.common.security import token
from com.ak.models.users import User
from mx.dip.voj.handlers.base import BaseHandler
from mx.dip.voj.handlers.forms import Register
from mx.dip.voj.models.countries import Country

#: handlers
class MainHandler(BaseHandler):
    def get(self):
        self.redirect('/a')
        #message = u'makes her happy, happy, happy!'
        #self.get_json_response_and_finish(0, 'success', message)

class RegisterHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def post(self):
        try:
            response = self.do_add()
            return self.get_json_response_and_finish(obj=response)
        except Exception as E:
            return self.get_json_response_and_finish(1000, str(E))

    def do_add(self, form_data=None):
        if not form_data:
            form_data = Register(self)
        if not form_data.validate():
            return self.get_response_object(1, form_data.errors)
        try:
            user = User.get_complex(form_data.email.data)
            if user:
                return self.get_response_object(1, u'Su email ya existe en nuestra base de datos, por favor intente nuevamente con otro.')
            try:
                birthday = datetime.datetime.strptime(form_data.birthday.data, '%Y/%m/%d')
            except:
                return self.get_response_object(1, u'La fecha de nacimiento es incorrecta.')
            try:
                country = None
                if form_data.country.data > 0:
                    country = Country.get_by_id(form_data.country.data)
            except:
                return self.get_response_object(1, u'El país seleccionado es incorrecto.')
            _token = token(32)
            user = User()
            user.token = _token
            user.first_name = form_data.first_name.data
            user.last_name = form_data.last_name.data
            user.email = form_data.email.data
            user.birthday = birthday
            user.country = country
            user.city = form_data.city.data or ''
            user.terms = form_data.terms.data
            user.policy = form_data.policy.data
            user.news = form_data.news.data or False
            user.role_id = 1
            user.role_name = 'user'
            user.remote_ip = self.remote_ip
            if form_data.fbuid.data:
                user.facebook_uid = str(form_data.fbuid.data)
                user.username = form_data.fbusername.data
            else:
                user.facebook_uid = 'fb__' + _token
                user.username = _token
            user.created = datetime.datetime.now()
            user.modified = datetime.datetime.now()
            user.available = True
            user.enabled = True
            user.password = _token
            user.save()
            print user.to_object()
            return self.get_response_object(0, u'Gracias por su registro.')
        except Exception as E:
            return self.get_response_object(1000, str(E))

#: handlers's list

handlers_list = [
    (r'/', MainHandler),
    (r'/register', RegisterHandler)
]
