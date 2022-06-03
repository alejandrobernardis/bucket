#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Mar 31, 2012, 8:43:15 PM


from com.ak.tornado.models.users import User
from com.ak.tornado.security import Role

from math import ceil

from tornado.escape import json_decode, json_encode, json
from tornado.web import RequestHandler
from tornado_utils.send_mail import send_email

#: -- helpers ------------------------------------------------------------------

__all__ = [
    "BaseHandler",
    "AuthBaseHandler",
    "AuthLoginHandler",
    "AuthForgotPasswordHandler"
]

COOKIE_USER_SESSION = "cookie_user_session"

#: -- BaseHandler --------------------------------------------------------------

class BaseHandler(RequestHandler):

    def initialize(self):
        try:
            ip = self.request.headers.get('X-Real-Ip', self.request.remote_ip)
        except:
            ip = self.request.remote_ip
        self.remote_ip = self.request.headers.get('X-Forwarded-For', ip)

    #: helpers

    def is_msie(self):
        user_agent = self.request.headers["User-Agent"]
        if 'msie' in user_agent.lower():
            return True
        return False

    def msie_header_fix(self):
        if self.is_msie():
            self.set_header("P3P", 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"')

    def check_xsrf_cookie(self):
        pass

    def get_arguments_list(self, args=[]):
        result = dict()
        for k in args:
            v = self.get_argument(k, None)
            result[k] = None if not v else v
        return result

    def get_json(self, error_id=0, error_message=None, response=None):
        result = dict(error=dict(id=error_id, message=error_message),
                      response=response)
        return json_decode(json_encode(result))

    def get_json_dumps(self, error_id=0, error_message=None, response=None):
        result = dict(error=dict(id=error_id, message=error_message),
                      response=response)
        return json.dumps(result)

    def get_json_response(self, error_id=0, error_message=None, response=None):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return self.get_json(error_id, error_message, response)

    def get_json_response_and_finish(self, error_id=0, error_message=None,
                                     response=None):
        result = self.get_json_response(error_id, error_message, response)
        return self.finish(result)

    def render_error(self, template="views/error.html", **kwargs):
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        self.render(template, **kwargs)
        return True

    def render_success(self, template="views/success.html", **kwargs):
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        self.render(template, **kwargs)
        return True

    def xsrf_force(self):
        try:
            print 'xsrf_token', self.xsrf_token
        except: pass

    def next_form_html(self):
        return '<input type="hidden" name="next" value="'+self.next_url+'"/>'

    #: properties

    @property
    def next_url(self):
        return self.get_argument("next", self.root_url)

    @property
    def root_url(self):
        return "/"

    @property
    def login_url(self):
        return self.settings.get("login_url")

    #: methods

    def do_next_or_root(self):
        self.redirect(self.next_url or "/")

    def do_root(self):
        self.redirect("/")

    def do_send_mail(self, email_from, email_to, subject, message):
        return send_email(
            backend='tornado_utils.send_mail.backends.smtp.EmailBackend',
            subject=subject,
            message=message,
            from_email="Administrator <%s>" % email_from,
            recipient_list=[email_to])

    def do_paginate(self, page_number=0, page_size=50, total=0):
        if total == 0:
            return None
        page_total = int(ceil(total / float(page_size)))
        page_number = int(page_number)
        page_prev = page_number - 1 if page_number > 1 else 1
        page_next = page_number + 1 if page_number < page_total else page_total
        return dict(total=total, page_size=page_size, page_total=page_total,
                    page_number=page_number, page_next=page_next,
                    page_prev=page_prev)

#: -- AuthBaseHandler ----------------------------------------------------------

class AuthBaseHandler(BaseHandler):

    #: helpers

    def get_user_value(self, key=None):
        if not self.current_user or not key:
            return None
        value = key.split(".")
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
        user = self.get_secure_cookie(self.settings.get(COOKIE_USER_SESSION))
        return None if not user or user is "" else json_decode(user)

    def set_current_user(self, user=None, facebook=None, access_token=None, remember_me=False):
        user_data = ""
        if isinstance(user, User):
            user_data = user.to_object()
            if facebook:
                facebook["access_token"] = facebook
            if access_token:
                user_data["access_token"] = access_token
            user_data = json_encode(user_data)
        user_remember = 1 if not remember_me else 365
        self.set_secure_cookie(self.settings.get(COOKIE_USER_SESSION),
                               user_data, user_remember)

    def get_user_model(self, user=None, enabled=True, availabled=True):
        try:
            if user:
                return User.get_complex(user, enabled, availabled)
            uid = self.get_user_value("id")
            return User.get_complex(uid, enabled, availabled)
        except Exception:
            return None

    #: properties

    @property
    def is_admin(self):
        try:
            return self.role.is_admin
        except:
            return False

    @property
    def role(self):
        role = self.get_user_value("role")
        return Role.get_role_by_value(role)

    @property
    def role_name(self):
        role = self.role
        return None if not role else role.name

    #: methods

    def do_logout(self):
        self.set_current_user()
        return self.get_json_response(0, "The process is finished correctly.",
                                      dict(next=self.next_url))

