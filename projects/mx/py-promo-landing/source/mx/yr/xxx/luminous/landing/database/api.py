#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Apr 10, 2012, 10:16:10 AM 

import datetime, re

from hashlib import md5
from mx.yr.xxx.luminous.landing.forms import (RegisterForm,
    RedeemAccessoriesForm, RedeemTicketsForm, RedeemGameForm)
from mx.yr.xxx.luminous.landing.models import *
from mx.yr.tornado.handlers import (AuthBaseHandler,
    BaseHandler, AuthLoginHandler, AuthForgotPasswordHandler, LegalAuditError)
from mx.yr.tornado.forms import LoginForm
from mx.yr.tornado.models import User, Location
from mx.yr.tornado.utils import datetime_to_str
from tornado.web import authenticated

#: -- Handlers -----------------------------------------------------------------

class ApiMainHandler(BaseHandler):
    def get(self):
        self.finish("<pre>YRAPI v1.0.0 Beta</pre>")

#: -----------------------------------------------------------------------------

class ApiRegisterHandler(BaseHandler):
    def get(self):
        if self.settings.get("debug"):
            return self.post()
        self.do_root()
        
    def post(self):
        form_data = RegisterForm(self)
        if not form_data.validate():
            return self.finish(self.get_json_response(1, form_data.errors))
        try:
            error = "The username already exists."
            if User.get_user_by_username(form_data.username.data):
                return self.get_json_response_and_finish(2, error)
            error = "The email already exists."
            if User.get_user_by_email(form_data.email.data):
                return self.get_json_response_and_finish(3, error)
            legal_age = self.settings.get("min_legal_age")
            error = u"Debes ser mayor a %s años." % legal_age
            birthday_year = int(form_data.birthday.data.year)
            birthday_value = datetime.date.today().year - birthday_year
            if birthday_value < legal_age:
                return self.get_json_response_and_finish(4, error)
            error = "The state is incorrect."
            if not Location.get_location(form_data.address_state.data):
                return self.get_json_response_and_finish(5, error)
            user = User()
            user.username = form_data.username.data
            user.password = form_data.password.data
            user.email = form_data.email.data
            user.first_name = form_data.first_name.data
            user.last_name = form_data.last_name.data
            user.birthday = form_data.birthday.data
            user.gender = int(form_data.gender.data)
            user.address_state = form_data.address_state.data
            user.phone_lada = int(form_data.phone_lada.data) or 0
            user.phone_number = int(form_data.phone_number.data) or 0
            user.remote_ip = self.remote_ip
            user.terms = form_data.terms.data
            user.policy = form_data.policy.data
            user.news = form_data.news.data
            user.enabled = True
            user.created = datetime.datetime.now()
            user.save()
            try:
                user_points = Points()
                user_points.user_id = user
                user_points.points = self.settings.get("max_redeem_register")
                user_points.enabled = True
                user_points.created = datetime.datetime.now()
                user_points.save()
                points = user_points.points
            except Exception: pass
            error = "The process is finished correctly."
            self.get_json_response_and_finish(0, error, 
                                              dict(user=user.to_object(), 
                                                   points=points or 0))
        except Exception as E:
            self.get_json_response_and_finish(1000, str(E))

#: -----------------------------------------------------------------------------

class ApiAuthLoginHandler(AuthLoginHandler):
    def get(self):
        if self.settings.get("debug"):
            return self.post("login")
        self.do_root()
    
    def do_login(self):
        data = LoginForm(self)
        if not data.validate():
            return self.get_json_response(1, data.errors)
        try:
            points = 0
            user, auth = User.auth_login(data.username.data, 
                                         data.password.data)
            if not user:
                return self.get_json_response(2, "The username is incorrect.")
            elif not auth:
                return self.get_json_response(3, "The password is incorrect.")
            else:
                user.set_last_login()
                points = Points.get_points_by_user(user)
                self.set_current_user(user, data.remember_me.data)
        except Exception as E:
            return self.get_json_response(1000, str(E))
        return self.get_json_response(0, "The process is finished correctly.", 
                                      dict(next=self.next_url, 
                                           user=user.to_object(),
                                           points=points))
        
#: -----------------------------------------------------------------------------

class ApiAuthForgotPasswordHandler(AuthForgotPasswordHandler):
    def get(self):
        if self.settings.get("debug"):
            return self.post("forgot-password")
        self.do_root()
        
#: -----------------------------------------------------------------------------

class ApiPointsAddHandler(AuthBaseHandler):    
    def get(self, action):
        if self.settings.get("debug"):
            return self.post(action)
        self.do_root()
    
    @authenticated
    def post(self, action):
        if action == "accesory":
            result = self.do_redeem_accessory()
        elif action == "ticket":
            result = self.do_redeem_ticket()
        elif action == "game":
            result = self.do_redeem_game()
        else:
            message = "The action '%s' is undefined." % action
            result = self.get_json_response(100, message)
        self.finish(result)
    
    def do_redeem_accessory(self):
        audit = self.settings.get("max_legal_audit_accesories")
        form_data = RedeemAccessoriesForm(self)
        if not form_data.validate():
            return self.get_json_response(1, form_data.errors)
        try:
            user = self.get_user_model()
            if not user:
                return self.get_json_response(2, u"El usuario no posee "
                                                 u"privilegios.")
            quantity = Code.get_total_by_user_today(user)
            if quantity > self.settings.get("max_redeem_accesories"):
                return self.get_json_response(3, u"Ha superado el máximo de "
                                                 u"redenciones por día.")
            code = form_data.accessory_code.data.upper()
            code_value = Code.get_by_token(code, True)
            if not code_value:
                message = u"[code] El código '%s' no es válido."
                self.do_legal_audit(message % code, audit, True)
                return self.get_json_response(4, u"El código no es válido.")
            code_value.set_status(user, False)
            points = Points.add_points_by_user(user, code_value.points)
            return self.get_json_response(0, "The process is finished "
                                          "correctly.", dict(points=points))
        except LegalAuditError as E:
            message = (u"Su cuenta ha sido deshabilitada por haber alcanzado "
                       u"el limite de %s auditorias.")
            return self.get_json_response(200, message % audit)
        except Exception as E:
            return self.get_json_response(1000, str(E))
    
    def do_redeem_ticket(self):
        form_data = RedeemTicketsForm(self)
        if not form_data.validate():
            return self.get_json_response(1, form_data.errors)
        try:
            user = self.get_user_model()
            if not user:
                return self.get_json_response(2, u"El usuario no posee "
                                                 u"privilegios.")
            quantity = ProductTicket.get_total_by_user_today(user)
            if quantity > self.settings.get("max_redeem_tickets"):
                return self.get_json_response(3, u"Ha superado el máximo de "
                                                 u"redenciones por día.")
            rfc = re.findall(r"([a-z0-9]+)", form_data.ticket_rfc.data,
                             flags=re.IGNORECASE)
            ticket_rfc = "".join(a for a in rfc)
            date = form_data.ticket_date.data.split(",")
            try:
                ticket_date = datetime.datetime(int(date[0]), int(date[1]), 
                                                int(date[2]), int(date[3]), 
                                                int(date[4]), 0, 0)
            except:
                return self.get_json_response(4, u"Por favor, defina "
                                                 u"correctamente la fecha.")
            token_md5 = md5()
            token_md5.update("%s-%s" % (ticket_rfc, 
                                        datetime_to_str(ticket_date)))
            token = token_md5.hexdigest()
            if ProductTicket.get_user_by_token(user, token, True):
                return self.get_json_response(5, u"El ticket no puede ser " 
                                                 u"registrado más de una vez.")
            quantity = ProductTicket.get_total_by_token(token, True)
            quantity_compare = self.settings.get("max_redeem_tickets_token")
            if quantity > quantity_compare:
                message = u"[ticket] El ticket ya fue registrado más de '%s' " \
                          u"veces." % quantity_compare
                self.do_legal_audit(message)
                return self.get_json_response(5, message)
            ticket = ProductTicket()
            ticket.user_id = user
            ticket.token = token
            ticket.rfc = ticket_rfc
            ticket.date_and_time = ticket_date
            ticket.enabled = True
            ticket.created = datetime.datetime.now()
            ticket.save()
            points = 0
            ticket_products = form_data.products_list.data[2:].split(",")
            for a in ticket_products:
                value = a.split(":")
                product_categoty = int(value[0])
                product_quantity = int(value[1])
                if Product.validate_category(product_categoty):
                    if Product.validate_quantity(product_quantity):
                        product = Product()
                        product.ticket_id = ticket
                        product.category = product_categoty
                        product.quantity = product_quantity
                        product.points = product.get_points()*product_quantity 
                        product.enabled = True
                        product.created = datetime.datetime.now()
                        product.save()
                        points += product.points
                    else:
                        message = (u"[ticket] La cantidad de '%s' productos no "
                                   u"esta permitida.")
                        self.do_legal_audit(message % product_quantity)
                else:
                    message = u"[ticket] La categoría '%s' no es correcta."
                    self.do_legal_audit(message % product_categoty)
            points = Points.add_points_by_user(user, points)
            return self.get_json_response(0, "The process is finished "
                                          "correctly.", dict(points=points))
        except LegalAuditError as E:
            message = (u"Su cuenta ha sido deshabilitada por haber alcanzado "
                       u"el limite de %s auditorias.")
            return self.get_json_response(200, message %\
                                          self.settings.get("max_legal_audit"))
        except Exception as E:
            return self.get_json_response(1000, str(E))
    
    def do_redeem_game(self):
        form_data = RedeemGameForm(self)
        if not form_data.validate():
            return self.get_json_response(1, form_data.errors)
        try:
            user = self.get_user_model()
            if not user:
                return self.get_json_response(2, u"El usuario no posee "
                                                 u"privilegios.")
            quantity = GamePoint.get_points_by_user_today(user) 
            quantity_max = self.settings.get("max_redeem_game")
            if quantity >= quantity_max:
                message = u"Ha superado el máximo de %s puntos por día por día."
                return self.get_json_response(3, message % quantity_max)
            game_points = int(form_data.game_points.data)
            if game_points > quantity_max:
                message = u"[game] El puntaje de %s supera los %s puntos de " \
                          u"limite." % (game_points, quantity_max)
                self.do_legal_audit(message)
                return self.get_json_response(4, message)
            game_points_value = quantity + game_points
            if game_points_value > quantity_max:
                game_points = quantity_max - quantity
            game = GamePoint()
            game.user_id = user
            game.points = game_points
            game.enabled = True
            game.created = datetime.datetime.now()
            game.save()
            points = Points.add_points_by_user(user, game.points)
            return self.get_json_response(0, "The process is finished "
                                             "correctly.", dict(points=points))
        except LegalAuditError as E:
            message = (u"Su cuenta ha sido deshabilitada por haber alcanzado "
                       u"el limite de %s auditorias.")
            return self.get_json_response(200, message %\
                                          self.settings.get("max_legal_audit"))
        except Exception as E:
            return self.get_json_response(1000, str(E))
        
#: -----------------------------------------------------------------------------        
        
class ApiUserHandler(AuthBaseHandler):
    def get(self, action):
        if self.settings.get("debug"):
            return self.post(action)
        self.do_root()
    
    @authenticated
    def post(self, action):
        if action == "status":
            result = self.do_get_status()
        elif action == "data":
            result = self.do_get_data()
        elif action == "points":
            result = self.do_get_points()
        else:
            message = "The action '%s' is undefined." % action
            result = self.get_json_response(100, message)
        self.finish(result)
        
    def do_get_status(self):
        try:
            user = self.get_user_model()
            if not user:
                return self.get_json_response(2, u"El usuario no posee "
                                                 u"privilegios.")
            return self.get_json_response(0, "The process is finished "
                                             "correctly.", 
                                             dict(status=user.enabled))
        except Exception as E:
            return self.get_json_response(1000, str(E))
    
    def do_get_data(self):
        try:
            user = self.get_user_model() 
            if not user:
                return self.get_json_response(2, u"El usuario no posee "
                                                 u"privilegios.")
            return self.get_json_response(0, "The process is finished "
                                             "correctly.", user.to_object())
        except Exception as E:
            return self.get_json_response(1000, str(E))
    
    def do_get_points(self):
        try:
            user = self.get_user_model()
            if not user:
                return self.get_json_response(2, u"El usuario no posee "
                                                 u"privilegios.")
            points = Points.get_points_by_user(user)
            return self.get_json_response(0, "The process is finished "
                                             "correctly.", dict(points=points))
        except Exception as E:
            return self.get_json_response(1000, str(E))
                
#: -- handlers_list ------------------------------------------------------------

handlers_list = [
    (r"/api", ApiMainHandler),
    (r"/api/register", ApiRegisterHandler),
    (r"/api/auth/login", ApiAuthLoginHandler),
    (r"/api/auth/forgot-password", ApiAuthForgotPasswordHandler),
    (r"/api/points/add/(.*)", ApiPointsAddHandler),
    (r"/api/user/(.*)", ApiUserHandler),
]

#: -- ui_modules_list ----------------------------------------------------------

ui_modules_list = {}

