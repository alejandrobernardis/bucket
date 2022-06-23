#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Mar 31, 2012, 8:43:15 PM

import logging, datetime

from mx.yr.xxx.luminous.landing.models import Points
from mx.yr.tornado.forms import LoginForm, ForgotPasswordForm
from mx.yr.tornado.models import User, LegalAudit
from mx.yr.tornado.security import secret_key, Role
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

class LegalAuditError(Exception):
    def __init__(self, eid=0, message=None):
        self.eid = eid
        self.message = message
    def __repr__(self):
        return str(self.message)
    def __str__(self):
        return repr(self.message)

#: -- BaseHandler --------------------------------------------------------------

class BaseHandler(RequestHandler):
    
    def initialize(self):
        try:
            ip = self.request.headers.get('X-Real-Ip', self.request.remote_ip)
        except: 
            ip = self.request.remote_ip
        self.remote_ip = self.request.headers.get('X-Forwarded-For', ip)
    
    #: helpers
    
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
            print self.xsrf_token
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
    
    def set_user_points(self, value="0"):
        self.set_secure_cookie('user_points', str(value), 1)
    
    def get_user_points(self):
        points = self.get_secure_cookie('user_points', None)
        if points and points != "0":
            return points
        try:
            user = User.get_user_by_username(self.get_user_value('username'))
            if user:
                points = str(Points.get_points_by_user(user))
            points = points or 0
            self.set_user_points(points)
            return points
        except:
            return 0
    
    def get_current_user(self):
        user = self.get_secure_cookie(self.settings.get(COOKIE_USER_SESSION))
        return None if not user or user is "" else json_decode(user)
    
    def set_current_user(self, user=None, access_token=None, remember_me=False):
        user_data = ""
        if isinstance(user, User):
            user_data = user.to_object() 
            if access_token:
                user_data["access_token"] = access_token
            user_data = json_encode(user_data)
        user_remember = 1 if not remember_me else 365
        self.set_secure_cookie(self.settings.get(COOKIE_USER_SESSION), 
                               user_data, user_remember)
    
    def get_user_model(self, user=None, only_enabled=True):
        try:
            if user:
                return User.get_user_complex(user, only_enabled)
            uid = self.get_user_value("id")
            return User.get_user_by_uid(uid, only_enabled)
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
        
    def do_legal_audit(self, menssage, audit_quantity=None, audit_today=False):
        try:
            if not audit_quantity:
                audit_quantity = self.settings.get("max_legal_audit")
            user = User.get_user_by_uid(self.get_user_value("id"))
            audit = LegalAudit()
            audit.user_id = user
            audit.menssage = menssage
            audit.enabled = True
            audit.created = datetime.datetime.now()
            audit.save()
            quantity = LegalAudit.get_total_by_user(user, audit_today, True)
            logging.warn("AUDIT (%s): %s" % (quantity, audit.to_object()))
            if quantity >= audit_quantity:
                message = "AUDIT (%s): the user '%s' (%s) is disabled." % \
                          (quantity, user.username, str(user.id))
                logging.error(message)
                user.set_disabled()
                self.do_logout()
                raise LegalAuditError(message=message)
        except LegalAuditError as E:
            raise E
        except Exception as E:
            logging.error("AUDIT: %s" % str(E))

#: -- AuthLoginHandler ---------------------------------------------------------

class AuthLoginHandler(AuthBaseHandler):
    
    def post(self, action=None):
        if action == "login":
            result = self.do_login()
        else:
            message = "The action '%s' is undefined." % action
            result = self.get_json_response(100, message)
        self.finish(result)
    
    def do_login(self):
        data = LoginForm(self)
        if not data.validate():
            return self.get_json_response(1, data.errors)
        try:
            user, auth = User.auth_login(data.username.data, 
                                         data.password.data)
            if not user:
                return self.get_json_response(2, "The username is incorrect.")
            elif not auth:
                return self.get_json_response(3, "The password is incorrect.")
            else:
                user.set_last_login()
                self.set_current_user(user, data.remember_me.data)
        except Exception as E:
            return self.get_json_response(1000, str(E))
        return self.get_json_response(0, "The process is finished correctly.", 
                                      dict(next=self.next_url, 
                                           user=user.to_object()))

#: -- AuthForgotPasswordHandler ------------------------------------------------

class AuthForgotPasswordHandler(AuthBaseHandler):
    
    def post(self, action):
        if action == "forgot-password":
            result = self.do_forgot_password()
        else:
            message = "The action '%s' is undefined." % action
            result = self.get_json_response(100, message)
        self.finish(result)

    def do_forgot_password(self, actiovation_key=None):
        data = ForgotPasswordForm(self)
        if not data.validate():
            return self.get_json_response(1, data.errors)
        try:
            user = User.auth_forgot_password(data.username_or_email.data)
            if not user:
                return self.get_json_response(2, "The username or email does "
                                                 "not exist.")
            password = secret_key(12)
            user.set_new_password(password)
            mail = self.do_send_mail(
                u"noreply@yr.com", 
                user.email, 
                u"Password Recovery",
                u"Hi %s,\nYour new passwors is: %s\n\nRegards,\nA!~" % \
                    (user.first_name, password))
            if not mail:
                return self.get_json_response(3, "The email could not be sent.")
        except Exception as E:
            return self.get_json_response(1000, str(E))
        return self.get_json_response(0, ("The instructions to recover your "
                                          "password were sent to: %s") % \
                                          user.email,
                                      dict(next=self.next_url))
            
