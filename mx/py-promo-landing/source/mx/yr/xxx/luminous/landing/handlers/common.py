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
from mx.yr.xxx.luminous.landing.forms import RegisterForm, \
     RedeemAccessoriesForm, RedeemTicketsForm, RedeemGameForm
from mx.yr.xxx.luminous.landing.models import Code, Points, Product, \
     ProductTicket, GamePoint
from mx.yr.tornado.handlers import AuthBaseHandler, LegalAuditError, BaseHandler
from mx.yr.tornado.forms import LoginForm, ForgotPasswordForm
from mx.yr.tornado.models import User, Location
from mx.yr.tornado.security import secret_key, Role, token
from mx.yr.tornado.utils import datetime_to_str
from tornado.auth import FacebookGraphMixin
from tornado.escape import url_escape
from tornado.web import authenticated, asynchronous

#: -- MainHandler --------------------------------------------------------------

class MainHandler(AuthBaseHandler):
    def get(self):
        return self.render("views/index.html")

class AuthLoginHandler(AuthBaseHandler):
    __template = "auth/login.html"
    
    def get(self):
        self.render(self.__template, form=RegisterForm(), errors={})
        
    def post(self):
        form_data = LoginForm(self)
        if not form_data.validate():
            errors = self.get_json_dumps(1, form_data.errors)
            return self.render(self.__template, form=form_data, errors=errors)
        try:
            user, auth = User.auth_login(form_data.username.data, 
                                         form_data.password.data)
            if not user:
                message = u"El nombre de usuario es incorrecto."
                errors = self.get_json_dumps(2, message)
                return self.render(self.__template, 
                                   form=form_data, errors=errors)
            elif not auth:
                message = u"La contraseña es incorrecta."
                errors = self.get_json_dumps(3, message)
                return self.render(self.__template, 
                                   form=form_data, errors=errors)
            else:
                user.set_last_login()
                self.set_current_user(user, form_data.remember_me.data)
                # !~
                points = Points.get_points_by_user(user)
                self.set_user_points(points)
                # !~
                self.do_next_or_root()
        except Exception as E:
            return self.render_error(message=str(E), next=self.next_url)
        
        
class AuthForgotPasswordHandler(AuthBaseHandler):
    __template = "auth/forgot-password.html"
    
    def get(self):
        self.render(self.__template, form=ForgotPasswordForm(), errors={})
        
    def post(self):
        form_data = ForgotPasswordForm(self)
        if not form_data.validate():
            errors = self.get_json_dumps(1, form_data.errors)
            return self.render(self.__template, form=form_data, errors=errors)
        try:
            user = User.auth_forgot_password(form_data.username_or_email.data)
            if not user:
                message = u"El nombre de usuario o email son incorrectos."
                errors = self.get_json_dumps(2, message)
                return self.render(self.__template, 
                                   form=form_data, errors=errors)
            password = token()[0:8]
            user.set_new_password(password)
            mail = self.do_send_mail(
                u"noreply@yr.com", 
                user.email, 
                u"xxx Luminous White, Recupero de Contraseña",
                u"Hola %s,\nTu nueva contraseña es: %s\n\nSaludos,\nA!~" % \
                    (user.first_name, password))
            if not mail:
                message = u"El email no pudo ser enviado."
                errors = self.get_json_dumps(3, message)
                return self.render(self.__template, 
                                   form=form_data, errors=errors)
            message = u"Tu contraseña fue enviada a: %s."
            return self.render_success(message=message % user.email, 
                                       next=self.login_url)
        except Exception as E:
            return self.render_error(message=str(E), next=self.next_url)
        
class AuthLogoutHandler(AuthBaseHandler):
    def get(self):
        self.do_logout()
        self.do_root()

class AuthFacebookHandler(AuthBaseHandler, FacebookGraphMixin):
    """
    TODO: Replantear si el usuario puede tener doble forma de loguearse, por
    user/pass o por FBConnect
    """
    @asynchronous
    def get(self):
        terms  = self.get_argument("terms", "0")
        if terms != "1":
            message = u"Para poder participar debes aceptar los Términos y Condiciones."
            return self.render_error(message=message, next=self.login_url)
        policy = self.get_argument("policy", "0")
        if policy != "1":
            message = u"Para poder participar debes aceptar los Políticas de Privacidad."
            return self.render_error(message=message, next=self.login_url)
        news   = self.get_argument("news", "0")
        redirect_uri = "%s://%s/auth/facebook?next=%s&terms=%s&policy=%s&news=%s" % (
                self.request.protocol, 
                self.request.host if self.settings.get("debug")\
                                  else self.settings.get('xxx_domain'),
                url_escape(self.next_url), terms, policy, news)
        extra_params = (u"publish_stream,user_about_me,user_location,"
                        u"user_hometown,user_birthday,user_photos,email")
        extra_fields = ["username","birthday","hometown","location","email"]
        client_id = self.settings.get("facebook_api_key")
        client_secret = self.settings.get("facebook_secret")
        if self.get_argument("code", False):
            self.get_authenticated_user(redirect_uri=redirect_uri,
                client_id=client_id,
                client_secret=client_secret,
                code=self.get_argument("code"),
                callback=self.async_callback(self._on_complete),
                extra_fields=extra_fields)
            return
        self.authorize_redirect(
            redirect_uri=redirect_uri,
            client_id=client_id,
            client_secret=client_secret,
            extra_params={"scope": extra_params})
        
    def _on_complete(self, user):
        if not user:
            error = u"Fecabook denegó el acceso.."
            return self.render_error(message=error, next="/register")
        terms  = self.get_argument("terms", "0")
        if terms != "1":
            message = u"Para poder participar debes aceptar los Términos y Condiciones."
            return self.render_error(message=message, next=self.login_url)
        policy = self.get_argument("policy", "0")
        if policy != "1":
            message = u"Para poder participar debes aceptar los Políticas de Privacidad."
            return self.render_error(message=message, next=self.login_url)
        try:
            user_fb = User.get_user_by_facebook_uid(user.get("id"), True)
            if user_fb:
                self.set_current_user(user_fb, user.get("access_token"))
                # !~
                points = Points.get_points_by_user(user_fb)
                self.set_user_points(points)
                # !~
                return self.do_next_or_root()
            user_fb = User.get_user_by_email(user.get("email"), True)
            if user_fb:
                error = u"El email '%s' ya fue utilizado por otra persona, itenta con otra cuenta."
                return self.render_error(message=error % user_fb.email, 
                                         next="/register")
            legal_age = self.settings.get("min_legal_age")
            user_fb_birthday = user.get("birthday").split("/")
            user_fb_birthday = datetime.date(int(user_fb_birthday[2]),
                                             int(user_fb_birthday[0]),
                                             int(user_fb_birthday[1]))
            if datetime.date.today().year - user_fb_birthday.year < legal_age:
                error = u"Necesitas ser mayor a %s años." % legal_age
                return self.render_error(message=error, next=self.root_url)
            user_fb_gender = str(user.get("gender"))
            if re.match(r"(male|female)", user_fb_gender, re.IGNORECASE):
                user_fb_gender = 1 if user_fb_gender.lower() == "male" else 2
            else:
                user_fb_gender = 0
            try:
                _hometown = user.get("hometown").get("name")
            except Exception: _hometown = ""
            try:
                _location = user.get("location").get("name")
            except Exception: _location = ""
            notes = "hometown=%s|location=%s" % (_hometown, _location)
            news = self.get_argument("news", "0")
            user_fb = User()
            user_fb.facebook_uid = user.get("id")
            user_fb.username = "fb_%s" % user.get("id")
            user_fb.password = secret_key(8)
            user_fb.email = user.get("email")
            user_fb.role = Role.get_role('user').permissions;
            user_fb.first_name = user.get("first_name")
            user_fb.middle_name = user.get("middle_name")
            user_fb.last_name = user.get("last_name")
            user_fb.birthday = user_fb_birthday
            user_fb.gender = user_fb_gender
            user_fb.address_state = 0
            user_fb.phone_lada = 0
            user_fb.phone_number = 0
            user_fb.remote_ip = self.remote_ip
            user_fb.notes = notes
            user_fb.terms = True
            user_fb.policy = True
            user_fb.news = True if news == "1" else False
            user_fb.enabled = True
            user_fb.created = datetime.datetime.now()
            user_fb.save()
            user_fb_points = Points()
            user_fb_points.user_id = user_fb
            user_fb_points.points = self.settings.get("max_redeem_register")
            user_fb_points.enabled = True
            user_fb_points.created = datetime.datetime.now()
            user_fb_points.save()
            # !~
            self.set_user_points(user_fb_points.points)
            # !~
            self.set_current_user(user_fb, user.get("access_token"))
            return self.do_next_or_root()
        except Exception as E:
            return self.render_error(message=str(E), next=self.root_url)

class RegisterHandler(AuthBaseHandler):
    __template = "views/register.html"
    
    def get(self):
        self.render(self.__template, form=RegisterForm(), errors={})
        
    def post(self):
        form_data = RegisterForm(self)
        if not form_data.validate():
            errors = self.get_json_dumps(1, form_data.errors)
            return self.render(self.__template, form=form_data, errors=errors)
        try:
            if User.get_user_by_username(form_data.username.data):
                message = u"Este usuario ya existe."
                errors = self.get_json_dumps(2, message)
                return self.render(self.__template, 
                                   form=form_data, errors=errors)
            if User.get_user_by_email(form_data.email.data):
                message = u"Este email ya fue utilizado por otra persona.."
                errors = self.get_json_dumps(3, message)
                return self.render(self.__template, 
                                   form=form_data, errors=errors)
            legal_age = self.settings.get("min_legal_age")
            birthday_value = datetime.date.today().year - \
                             form_data.birthday_year.data
            if birthday_value < legal_age:
                message = u"Debes ser mayor a %s años." % legal_age
                errors = self.get_json_dumps(4, message)
                return self.render(self.__template, 
                                   form=form_data, errors=errors)
            if not Location.get_location(form_data.address_state.data):
                message = "Selecciona un estado."
                errors = self.get_json_dumps(5, message)
                return self.render(self.__template, 
                                   form=form_data, errors=errors)
            birthday = datetime.date(int(form_data.birthday_year.data),
                                     int(form_data.birthday_month.data),
                                     int(form_data.birthday_day.data))
            user = User()
            user.username = form_data.username.data
            user.password = form_data.password.data
            user.email = form_data.email.data
            user.role = Role.get_role('user').permissions;
            user.first_name = form_data.first_name.data
            user.last_name = form_data.last_name.data
            user.birthday = birthday
            user.gender = int(form_data.gender.data)
            user.address_state = form_data.address_state.data
            user.phone_lada = int(form_data.phone_lada.data or 0)
            user.phone_number = int(form_data.phone_number.data or 0)
            user.remote_ip = self.remote_ip
            user.terms = form_data.terms.data
            user.policy = form_data.policy.data
            user.news = form_data.news.data
            user.enabled = True
            user.created = datetime.datetime.now()
            user.save()
            user_points = Points()
            user_points.user_id = user
            user_points.points = self.settings.get("max_redeem_register")
            user_points.enabled = True
            user_points.created = datetime.datetime.now()
            user_points.save()
            # !~
            self.set_user_points(user_points.points)
            # !~
            return self.render_success(message=(u"Tu registro ha sido creado. "
                                                u"Ahora ingresa a tu cuenta."), 
                                       next=self.login_url)
        except Exception as E:
            return self.render_error(message=str(E), 
                                     next=self.next_url)
            
#: -- authenticated ------------------------------------------------------------        
        
class RedeemHandler(AuthBaseHandler):
    __actions = ["codes", "tickets"] 
    
    @authenticated
    def get(self, action=None):
        if not action:
            return self.render("views/redeem.html")
        if self.validate_action(action): 
            return 
        self.render(self.__template, form=self.__form(), errors={})
        
    @authenticated
    def post(self, action=None):
        if self.validate_action(action): 
            return 
        if action == "codes":
            self.do_reddem_code()
        else:
            self.do_reddem_ticket()
    
    def validate_action(self, action):
        if not action in self.__actions:
            self.__template = None
            self.__form = None
            message = u"No puedes realizar esta acción."
            return self.render_error(message=message, next=self.next_url)
        self.__template = "views/redeem-%s.html" % action
        self.__form = RedeemAccessoriesForm if action == "codes" else \
                      RedeemTicketsForm
        return False
    
    def do_reddem_code(self):
        audit = self.settings.get("max_legal_audit_accesories")
        form_data = RedeemAccessoriesForm(self)
        if not form_data.validate():
            errors = self.get_json_dumps(1, form_data.errors)
            return self.render(self.__template, form=form_data, errors=errors)
        try:
            user = self.get_user_model()
            if not user:
                message = u"El usuario no posee privilegios."
                errors = self.get_json_dumps(2, message)
                return self.render(self.__template, 
                                   form=form_data, errors=errors)
            quantity = Code.get_total_by_user_today(user)
            if quantity > self.settings.get("max_redeem_accesories"):
                message = u"Has llegado al límite del día."
                errors = self.get_json_dumps(3, message)
                return self.render(self.__template, 
                                   form=form_data, errors=errors)
            code = form_data.accessory_code.data.upper()
            code_value = Code.get_by_token(code, True)
            if not code_value:
                message = u"[code] El código '%s' no es válido."
                self.do_legal_audit(message % code, audit, True)
                message = u"El código no es válido."
                errors = self.get_json_dumps(4, message)
                self.render(self.__template, form=form_data, errors=errors)
                return
            code_value.set_status(user, False)
            points = Points.add_points_by_user(user, code_value.points)
            # !~
            self.set_user_points(points)
            # !~
            return self.render_success(template='views/redeem-success.html',
                                       next=self.next_url, points=points)
        except LegalAuditError as E:
            message = (u"Su cuenta ha sido deshabilitada por haber alcanzado "
                       u"el limite de %s auditorias. Por favor, pongase en "
                       u"contacto con Soporte (soporte@xxxluminouswhite.com.mx) para "
                       u"iniciar el proceso de recuperación.") % \
                       self.settings.get("max_legal_audit")
            self.render_error(message=message % audit, next=self.next_url)
            return
        except Exception as E:
            self.render_error(message=str(E), next=self.next_url)
            return 
    
    def do_reddem_ticket(self):
        form_data = RedeemTicketsForm(self)
        if not form_data.validate():
            errors = self.get_json_dumps(1, form_data.errors)
            return self.render(self.__template, form=form_data, errors=errors)
        try:
            user = self.get_user_model()
            if not user:
                message = u"El usuario no posee privilegios."
                errors = self.get_json_dumps(2, message)
                return self.render(self.__template, 
                                   form=form_data, errors=errors)
            quantity = ProductTicket.get_total_by_user_today(user)
            if quantity > self.settings.get("max_redeem_tickets"):
                message = u"Has superado el máximo de tickets por día."
                errors = self.get_json_dumps(3, message)
                return self.render(self.__template, 
                                   form=form_data, errors=errors)
            rfc = re.findall(r"([a-z0-9]+)", form_data.ticket_rfc.data,
                             flags=re.IGNORECASE)
            ticket_rfc = "".join(a for a in rfc)
            try:
                ticket_date = datetime.datetime(form_data.ticket_year.data,
                                                form_data.ticket_month.data,
                                                form_data.ticket_day.data,
                                                form_data.ticket_hour.data,
                                                form_data.ticket_minutes.data, 
                                                0, 0)
            except:
                message = u"Teclea tu fecha de compra."
                errors = self.get_json_dumps(4, message)
                return self.render(self.__template, 
                                   form=form_data, errors=errors)
            token_md5 = md5()
            token_md5.update("%s-%s" % (ticket_rfc, 
                                        datetime_to_str(ticket_date)))
            token = token_md5.hexdigest()
            if ProductTicket.get_user_by_token(user, token, True):
                message = u"El ticket no puede ser registrado más de una vez."
                errors = self.get_json_dumps(5, message)
                return self.render(self.__template, 
                                   form=form_data, errors=errors)
            quantity = ProductTicket.get_total_by_token(token, True)
            quantity_compare = self.settings.get("max_redeem_tickets_token")
            if quantity > quantity_compare:
                message = u"[ticket] El ticket ya fue registrado más de '%s' " \
                          u"veces." % quantity_compare
                self.do_legal_audit(message)
                message = u"El ticket ya fue registrado más de '%s' veces."
                errors = self.get_json_dumps(5, message % quantity_compare)
                return self.render(self.__template, 
                                   form=form_data, errors=errors)
            products = int(form_data.product_pasta.data)\
                         + int(form_data.product_cepillo.data)\
                         + int(form_data.product_enjuague.data)
            if products < 1:
                message = u"Por favor, debes definir la cantinda de almenos un producto."
                errors = self.get_json_dumps(7, message)
                return self.render(self.__template, 
                                   form=form_data, errors=errors)
            try:
                ticket = ProductTicket()
                ticket.user_id = user
                ticket.token = token
                ticket.rfc = ticket_rfc
                ticket.date_and_time = ticket_date
                ticket.enabled = True
                ticket.created = datetime.datetime.now()
                ticket.save()
            except:
                message = u"El ticket no pudo ser registrado."
                errors = self.get_json_dumps(6, message % quantity_compare)
                return self.render(self.__template, 
                                   form=form_data, errors=errors)
            points = 0
            ticket_products = [(2,form_data.product_pasta), 
                               (1,form_data.product_cepillo), 
                               (3,form_data.product_enjuague)]
            for _k, _v in ticket_products:
                product_categoty = _k
                product_quantity = int(_v.data)
                if Product.validate_category(product_categoty):
                    if product_quantity == 0:
                        pass
                    elif Product.validate_quantity(product_quantity):
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
            # !~
            self.set_user_points(points)
            # !~
            return self.render_success(template='views/redeem-success.html',
                                       points=points, next=self.next_url)
        except LegalAuditError as E:
            message = (u"Su cuenta ha sido deshabilitada por haber alcanzado "
                       u"el limite de %s auditorias. Por favor, pongase en "
                       u"contacto con Soporte (soporte@xxxluminouswhite.com.mx) para "
                       u"iniciar el proceso de recuperación.") % \
                       self.settings.get("max_legal_audit")
            return self.render_error(message=message, 
                                     next=self.next_url)
        except Exception as E:
            return self.render_error(message=str(E), next=self.next_url)
        
class GameHandler(AuthBaseHandler):
    __template = "views/game.html"
    
    @authenticated
    def get(self):
        self.render(self.__template)
    
    @authenticated
    def post(self):
        form_data = RedeemGameForm(self)
        if not form_data.validate():
            message = u"Lo sentimos, tus datos son incorrectos."
            return self.render_error(message=message, next=self.request.uri)
        try:
            user = self.get_user_model()
            if not user:
                message = u"El usuario no posee privilegios."
                return self.render_error(message=message, next=self.next_url)
            game_points = int(form_data.points.data)
            if game_points < 1:
                message = u"Lo sentimos, pero no has obtenido puntos."
                return self.render_error(message=message, next=self.next_url)
            quantity = GamePoint.get_points_by_user_today(user) 
            quantity_max = self.settings.get("max_redeem_game")
            if quantity >= quantity_max:
                message = u"Has superado el máximo de puntos por día."
                return self.render_error(message=message, 
                                         next=self.next_url)
            if game_points > quantity_max:
                message = u"[game] El puntaje de %s supera los %s puntos de " \
                          u"limite." % (game_points, quantity_max)
                self.do_legal_audit(message)
                return self.render_error(message=message, next=self.next_url)
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
            # !~
            self.set_user_points(points)
            # !~
            return self.render_success(template='views/redeem-success.html',
                                       points=points, next=self.next_url)
        except LegalAuditError as E:
            message = (u"Su cuenta ha sido deshabilitada por haber alcanzado "
                       u"el limite de %s auditorias. Por favor, pongase en "
                       u"contacto con Soporte (soporte@xxxluminouswhite.com.mx) para "
                       u"iniciar el proceso de recuperación.") % \
                       self.settings.get("max_legal_audit")
            return self.render_error(message=message, 
                                     next=self.next_url)
        except Exception as E:
            return self.render_error(message=str(E), next=self.next_url)
        
class TermsHandler(BaseHandler):
    def get(self):
        self.render("views/terms.html")

#: -- handlers_list ------------------------------------------------------------

handlers_list = [
    (r"/", MainHandler),
    (r"/auth/login", AuthLoginHandler),
    (r"/auth/logout", AuthLogoutHandler),
    (r"/auth/facebook", AuthFacebookHandler),
    (r"/auth/forgot-password", AuthForgotPasswordHandler),
    (r"/register", RegisterHandler),
    (r"/redeem", RedeemHandler),
    (r"/redeem/(.*)", RedeemHandler),
    (r"/game", GameHandler),
    (r"/terms", TermsHandler),
]

#: -- ui_modules_list ----------------------------------------------------------

ui_modules_list = {}
