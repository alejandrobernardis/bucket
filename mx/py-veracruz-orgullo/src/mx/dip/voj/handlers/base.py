#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Jan 4, 2013 1:14:27 PM

#: imports
import logging
from com.ak.common.forms import LoginForm
from com.ak.common.roles import Role
from com.ak.models.users import User
from math import ceil
from settings import COOKIE_USER_SESSION, USER_DATA_IGNORE
from tornado.escape import json_decode, json_encode, json
from tornado.web import RequestHandler, HTTPError
import settings

#: helpers
__all__ = ['BaseHandler', 'AuthBaseHandler', 'AuthLoginHandler']

#: classes
class BaseHandler(RequestHandler):
    
    def initialize(self):
        try:
            ip = self.request.headers.get('X-Real-Ip', self.request.remote_ip)
        except:
            ip = self.request.remote_ip
        self.remote_ip = self.request.headers.get('X-Forwarded-For', ip)
        
    def get_arguments_list(self, args=[]):
        result = dict()
        for k in args:
            v = self.get_argument(k, None)
            result[k] = None if not v else v
        return result

    def get_response_object(self, error_id=0, error_message=None,
                            response=None):
        return dict(error=dict(id=error_id, message=error_message),
                    response=response)

    def get_response_object_for_json(self, error_id=0, error_message=None,
                                     response=None):
        return dict(error_id=error_id, error_message=error_message,
                    response=response)

    def get_json_str(self, error_id=0, error_message=None, response=None,
                     obj=None):
        result = obj \
                 or self.get_response_object(error_id, error_message, response)
        return json_decode(json_encode(result))

    def get_json_dumps(self, error_id=0, error_message=None, response=None,
                       obj=None):
        result = obj \
                 or self.get_response_object(error_id, error_message, response)
        return json.dumps(result)

    def get_json_response(self, error_id=0, error_message=None, response=None,
                          obj=None):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return self.get_json_str(error_id, error_message, response, obj)

    def get_json_response_and_finish(self, error_id=0, error_message=None,
                                     response=None, obj=None):
        result = self.get_json_response(error_id, error_message, response, obj)
        return self.finish(result)

    def _render_message(self, template, **kwargs):
        try:
            self.set_header('Content-Type', 'text/html; charset=UTF-8')
            self.render(template, **kwargs)
        except:
            raise HTTPError(404, "Missing template %s" % template)
        return True

    def render_error(self, template='views/error.html', **kwargs):
        return self._render_message(template, **kwargs)

    def render_success(self, template='views/success.html', **kwargs):
        return self._render_message(template, **kwargs)

    def xsrf_force(self):
        try:
            print 'xsrf_token', self.xsrf_token
        except: pass

    def next_form_html(self):
        return '<input type="hidden" name="next" value="'+self.next_url+'"/>'

    #: properties

    @property
    def next_url(self):
        return self.get_argument('next', self.root_url)

    @property
    def root_url(self):
        return '/'

    @property
    def login_url(self):
        return self.settings.get('login_url')
    
    #: methods

    def do_logging(self, level='LOG', *args):
        message = '\n '.join([a for a in args])
        logging.log(level, message)

    def do_logging_debug(self, *args):
        self.do_logging('DEBUG', *args)

    def do_logging_info(self, *args):
        self.do_logging('INFO', *args)

    def do_logging_warn(self, *args):
        self.do_logging('WARN', *args)

    def do_logging_error(self, *args):
        self.do_logging('ERROR', *args)

    def do_logging_critical(self, *args):
        self.do_logging('CRITICAL', *args)

    def do_next_or_root(self):
        self.redirect(self.next_url or '/')

    def do_root(self):
        self.redirect('/')

    def do_paginate(self, page_number=0, page_size=50, total=0):
        if total == 0:
            return None
        page_total = int(ceil(total/float(page_size)))
        page_number = int(page_number)
        page_prev = page_number-1 if page_number > 1 else 1
        page_next = page_number+1 if page_number < page_total else page_total
        return dict(total=total, page_size=page_size, page_total=page_total,
                    page_number=page_number, page_next=page_next, 
                    page_prev=page_prev)

#: -- x ------------------------------------------------------------------------
        
class AuthBaseHandler(BaseHandler):

    def get_user_value(self, key=None):
        if not self.current_user or not key:
            return None
        value = key.split('.')
        v = self.current_user.get(value[0])
        if not v:
            return None
        value = value[1:]
        for k in range(len(value)):
            v = v.get(value[k])
            if not v and k < len(value):
                return None
        return v
    
    def get_current_user(self):
        user = self.get_secure_cookie(COOKIE_USER_SESSION)
        return None if not user or user is '' else json_decode(user)

    def set_current_user(self, user=None, access_token=None, remember_me=False):
        user_data = ''
        if isinstance(user, User):
            user_data = user.to_object()
            if access_token:
                user_data['access_token'] = access_token
            user_data = json_encode(user_data)
        user_remember = 1 if not remember_me else 365
        self.set_secure_cookie(COOKIE_USER_SESSION, user_data, user_remember)

    def get_user_model(self, user=None, enabled=True, available=True):
        try:
            if user:
                return User.get_complex(user, enabled, available)
            uid = self.get_user_value('id')
            return User.get_complex(uid, enabled, available)
        except:
            return None
        
    def get_user_role(self, value=None):
        try:
            if not value:
                value = self.get_user_value('role_id')
            role = Role.get_role_by_value(value)
            if not role:
                role = Role.get_role(value)
        except: 
            role = None
        return role

    #: properties

    @property
    def is_admin(self):
        try:
            return self.role.is_admin
        except:
            return False

    @property
    def role(self):
        return self.get_user_role()

    @property
    def role_name(self):
        role = self.role
        return None if not role else role.name

    #: methods

    def do_logout(self, redirect=None):
        self.set_current_user()
        if redirect:
            self.redirect(redirect)
        message = u'The process is finished correctly.'
        return self.get_json_response(0, message, dict(next=self.next_url))

#: -- x ------------------------------------------------------------------------
        
class AuthLoginHandler(AuthBaseHandler):
    _base_template = 'auth/login.html'
    
    def get(self):
        self.render(self._base_template, form=LoginForm(), errors=None)
        
    def post(self):
        try:
            form_data = LoginForm(self)
            form_error = self.do_login(form_data).get('error')
            if form_error.get('id') != 0:
                return self.render(self._base_template, 
                                   form=form_data, 
                                   errors=form_error.get('message'))
            return self.redirect(self.next_url)
        except Exception as E:
            return self.render_error(message=str(E), next_url=self.root_url)

    def do_login(self, form_data=None):
        if not form_data:
            form_data = LoginForm(self)
        if not form_data.validate():
            return self.get_response_object(1, form_data.errors)
        try:
            user, auth = User.do_auth_login(form_data.username.data,
                                            form_data.password.data)
            if not user:
                return self.get_response_object(2, 'The username is incorrect.')
            elif not auth:
                return self.get_response_object(3, 'The password is incorrect.')
            else:
                user.set_last_login()
                self.set_current_user(user, form_data.remember_me.data)
                message = 'The process is finished correctly.'
                response = dict(user=user.to_object(USER_DATA_IGNORE),
                                next=self.next_url)
                return self.get_response_object(0, message, response)
        except Exception as E:
            return self.get_response_object(1000, str(E))
    
    
    
    
    