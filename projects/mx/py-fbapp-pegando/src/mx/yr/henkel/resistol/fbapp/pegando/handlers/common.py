#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Aug 7, 2012, 1:41:44 PM

import datetime, os, sys, json, urllib
from com.ak.tornado.forms import BaseForm
from com.ak.tornado.models.users import User
from com.ak.tornado.security import secret_key, token
from mongoengine import Q
from mx.yr.henkel.resistol.fbapp.pegando.handlers.base import \
     BaseHandler, AuthBaseHandler
from mx.yr.henkel.resistol.fbapp.pegando.models import History
from tornado.auth import FacebookGraphMixin
from tornado.escape import url_escape, json_decode, json_encode
from tornado.web import authenticated, asynchronous
from wtforms import TextField, IntegerField, validators

#: -- MISC ---------------------------------------------------------------------
#: -----------------------------------------------------------------------------
#: -----------------------------------------------------------------------------
#: VARS, CONSTS, ETC
#: -----------------------------------------------------------------------------
#: -----------------------------------------------------------------------------

FILTER_HISTORY_IGNORE = ["id", "email","friend_fbuid","action_token","enabled","availabled"]
COOKIE_TEMP = "facebook_user_temporal"
COOKIE_TEMP_EDIT = 'history_data'
URL_PATCH = "www.resistol.com.mx/facebook/app_new_pegando_historias"
PATH_PATCH = "/facebook/app_new_pegando_historias"
PROTOCOL_PATCH = 'https'

#: -- FRONT --------------------------------------------------------------------
#: -----------------------------------------------------------------------------
#: -----------------------------------------------------------------------------
#: LIST, SEARCH
#: -----------------------------------------------------------------------------
#: -----------------------------------------------------------------------------

class MainHandler(AuthBaseHandler):
    @authenticated
    def get(self):
        self.msie_header_fix()
        return self.render("views/index.html")

    def post(self):
        self.msie_header_fix()
        self.redirect(PATH_PATCH)

class HistoryGetHandler(AuthBaseHandler):
    def get(self, uid=None):
        self.msie_header_fix()
        try:
            if uid:
                user = self.get_current_user()
                history = History.get_by_token(uid)
                if history:
                    h = history.to_object(FILTER_HISTORY_IGNORE)
                    h["edit"] = (user and user['email'] == history.email)
                    return self.get_json_response_and_finish(0, "success", h)
                else:
                    return self.get_json_response_and_finish(1, "No se encontraron resultados.")
        except Exception as E:
            return self.get_json_response_and_finish(1000, "Error no controlado: "+str(E), {'next':PATH_PATCH})

class HistoriesListHandler(AuthBaseHandler):
    def get(self, category=0, page_number=0, page_size=3):
        self.msie_header_fix()
        try:
            _Q = None
            category = int(category)
            if category > 0:
                _Q = Q(history_category=category)
            query = self.get_argument("q", None);
            if query:
                _Qu = Q(email__icontains=query)
                _Q = _Qu if not _Q else _Q&_Qu
            total = History.objects(_Q).count()
            pages = self.do_paginate(int(page_number), int(page_size), total)
            if pages:
                user = self.get_current_user()
                histories = History.get_paginate_enabled(pages.get('page_number'), pages.get('page_size'), _Q)
                result = []
                for a in histories:
                    h = a.to_object(FILTER_HISTORY_IGNORE)
                    h["edit"] = (user and user['email'] == a.email)
                    result.append(h)
                pages["result"] = result
                pages["category"] = category
                pages["query"] = query
                return self.get_json_response_and_finish(0, "success", pages)
            else:
                return self.get_json_response_and_finish(1, "No se encontraron resultados.")
        except Exception as E:
            return self.get_json_response_and_finish(1000, "Error no controlado: "+str(E), {'next':PATH_PATCH})

class HistoryPublishHandler(BaseHandler):
    def get(self, uid=None):
        self.msie_header_fix()
        try:
            if uid:
                history = History.get_by_token(uid)
                if history:
                    fb_history_title = "%s Y %s quedaron pegados con su historia." % (history.my_name, history.friend_name)
                    fb_history_url = "https://apps.facebook.com/pegando_historias/history/view/%s" % history.token
                    return self.render("views/create_view.html",
                                       user_profile=json_encode(history.to_object()),
                                       fb_history_title=fb_history_title,
                                       fb_history_url=fb_history_url)
                else:
                    return self.redirect(PATH_PATCH)
        except Exception: #as E:
            return self.redirect(PATH_PATCH)

    def post(self, uid=None):
        self.msie_header_fix()
        self.get(uid)

class HistoryViewHandler(BaseHandler):
    def get(self, uid=None):
        self.msie_header_fix()
        try:
            if uid:
                history = History.get_by_token(uid)
                if history:
                    fb_history_title = "%s Y %s quedaron pegados con su historia." % (history.my_name, history.friend_name)
                    fb_history_url = "https://apps.facebook.com/pegando_historias/history/view/%s" % history.token
                    return self.render("views/view.html",
                                       user_profile=json_encode(history.to_object(FILTER_HISTORY_IGNORE)),
                                       fb_history_title=fb_history_title,
                                       fb_history_url=fb_history_url)
                else:
                    return self.redirect(PATH_PATCH)
        except Exception: #as E:
            return self.redirect(PATH_PATCH)

    def post(self, uid=None):
        self.msie_header_fix()
        self.get(uid)

#: -- BACK ---------------------------------------------------------------------
#: -----------------------------------------------------------------------------
#: -----------------------------------------------------------------------------
#: Auth
#: -----------------------------------------------------------------------------
#: -----------------------------------------------------------------------------

class AuthFacebookTermsHandler(AuthBaseHandler):
    def get(self):
        self.msie_header_fix()
        return self.render("views/auth.html")

    def post(self):
        self.msie_header_fix()
        try:
            cookie = self.get_secure_cookie(COOKIE_TEMP)
            if not cookie:
                message = (u"Disculpe las molestias pero de momento no podemos procesar su registro.\n"
                           u"Por favor, vuelva a intentarlo más tarde.\n\nGracias.")
                return self.get_json_response_and_finish(1, message, {'next':PATH_PATCH})
            #terms  = self.get_argument("terms", "0")
            #if terms != "1":
            #    message = u"Para poder participar debes aceptar los Términos y Condiciones."
            #    return self.get_json_response_and_finish(1, message, {'next':PATH_PATCH})
            policy = self.get_argument("policy", "0")
            if policy != "1":
                message = u"Para poder participar debes aceptar los Políticas de Privacidad."
                return self.get_json_response_and_finish(1, message, {'next':PATH_PATCH})
            news = self.get_argument("news", "0")
            user = json_decode(cookie)
            location = user.get("location")
            location = location.get("name") if location else ""
            user_fb = User()
            user_fb.token = token(32)
            user_fb.facebook_uid = user.get("id")
            user_fb.username = user.get("username")
            user_fb.password = secret_key(8)
            user_fb.email = user.get("email") or ("%s@facebookfake.com" % user.get("username"))
            user_fb.first_name = user.get("first_name") or ""
            user_fb.middle_name = user.get("middle_name")  or ""
            user_fb.last_name = user.get("last_name")  or ""
            user_fb.birthday = None
            user_fb.address_state = 0
            user_fb.phone_lada = 0
            user_fb.phone_number = 0
            user_fb.remote_ip = self.remote_ip
            user_fb.terms = True
            user_fb.policy = True
            user_fb.news = True if news == "1" else False
            user_fb.location = location
            user_fb.availabled = True
            user_fb.enabled = True
            user_fb.created = datetime.datetime.now()
            user_fb.save()
            self.set_current_user(user_fb, facebook=user, access_token=user.get("access_token"),1)
            #self.set_secure_cookie(COOKIE_TEMP, "", 0)
            return self.get_json_response_and_finish(0, "success", {'next':PATH_PATCH+'/history/create'})
        except Exception as E:
            return self.get_json_response_and_finish(1000, "Error no controlado: "+str(E), {'next':PATH_PATCH})

class AuthFacebookHandler(AuthBaseHandler, FacebookGraphMixin):

    @asynchronous
    def get(self):
        self.msie_header_fix()
        next_url = self.get_argument("next", PATH_PATCH)
        redirect_uri = "%s://%s/auth/login?next=%s" % (
                PROTOCOL_PATCH or self.request.protocol, URL_PATCH, url_escape(next_url))
        extra_params = ("publish_stream,user_about_me,user_location,user_photos,email,"
                        "friends_about_me,friends_location,friends_photos,read_friendlists")
        extra_fields = ["username","location","email"]
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
        self.msie_header_fix()
        if not user:
            error = u"Fecabook denegó el acceso."
            return self.render_error(message=error, next=PATH_PATCH)
        try:
            self.set_secure_cookie(COOKIE_TEMP, json_encode(user), 2)
            user_fb = User.get_by_facebook_uid(user.get("id"))
            if user_fb:
                next_url = self.get_argument("next", PATH_PATCH)
                self.set_current_user(user_fb, user, user.get("access_token"), 1)
                return self.redirect(PATH_PATCH+next_url)
            else:
                return self.redirect(PATH_PATCH+"/auth/terms")
        except Exception as E:
            return self.render_error(message=str(E), next=PATH_PATCH)

#: -----------------------------------------------------------------------------
#: -----------------------------------------------------------------------------
#: Create!
#: -----------------------------------------------------------------------------
#: -----------------------------------------------------------------------------

_validators_optional = validators.Optional()

class HistoryCreateSaveForm(BaseForm):
    my_name = TextField(u"Tu nombre", [
        validators.Required(message=u"Tu nombre es requerido.")], default="")
    my_location = TextField(u"Tu ubicación", [
        validators.Required(message=u"Tu ubicación es requerida.")], default="")
    my_photo = TextField(u"Tu foto", [
        validators.Required(message=u"Tu foto es requerida.")], default="")
    friend_name = TextField(u"Tu amigo(a)", [
        validators.Required(message=u"El nombre de tu amigo(a) es requerido.")], default="")
    friend_location = TextField(u"La ubicación de tu amigo(a)", [
        validators.Required(message=u"La ubicación de tu amigo(a) es requerida.")], default="")
    friend_photo = TextField(u"La foto de tu amigo(a)", [
        validators.Required(message=u"La foto de tu amigo(a) es requerida.")], default="")
    friend_fbuid = TextField("Facebook User ID", [_validators_optional], default="")
    history_category = IntegerField(u"¿Qué relación los une?", [
        validators.Required(message=u"¿Qué relación los une?"),
        validators.NumberRange(1,3,message=u"Su relación no es válida.")], default=0)
    history_location = TextField(u"¿Dónde se conocieron?", [
        validators.Required(message=u"¿Dónde se conocieron?")], default="")
    history_detail = TextField(u"¿Qué es lo que más los une?", [
        validators.Required(message=u"¿Qué es lo que más los une?")], default="")
    image_01 = TextField(u"Imagen 1", [_validators_optional], default="")
    image_02 = TextField(u"Imagen 2", [_validators_optional], default="")
    image_03 = TextField(u"Imagen 3", [_validators_optional], default="")
    action_token = TextField(u"ActionKey", [
        validators.Required(message=u"Tu ActionKey es requerida.")], default="")

class HistoryCreateSaveHandler(AuthBaseHandler):
    def get_geocode(self, address=""):
        api = "http://maps.googleapis.com/maps/api/geocode/json"
        args = dict(sensor="false", address=address.encode("utf-8"))
        url = api+"?"+urllib.urlencode(args)
        try:
            result = json.load(urllib.urlopen(url))
            if result.get("status") == "OK":
                return result
            else: raise
        except: return False

    def check_xsrf(self):
        token = (self.get_argument("_xsrf", None)
                 or self.request.headers.get("X-Xsrftoken")
                 or self.request.headers.get("X-Csrftoken"))
        if not token:
            return False
        if self.xsrf_token != token:
            return False
        return True

    @authenticated
    def post(self):
        try:
            if not self.check_xsrf():
                return self.get_json_response_and_finish(1, u"Las claves de validación no concuerdan.")
            form_data = HistoryCreateSaveForm(self)
            if not form_data.validate():
                return self.get_json_response_and_finish(2, dict(errors=form_data.errors))
            my_location = self.get_geocode(form_data.my_location.data)
            if not my_location:
                return self.get_json_response_and_finish(1, u"Tu ubicación no es correcta.")
            friend_location = self.get_geocode(form_data.friend_location.data)
            if not friend_location:
                return self.get_json_response_and_finish(1, u"La ubicación de tu amigo no es correcta.")
            my_location = my_location.get("results")[0].get("geometry").get("location")
            friend_location = friend_location.get("results")[0].get("geometry").get("location")
            history = History()
            history.action_token = form_data.action_token.data
            history.email = self.get_user_value("email")
            history.token = token(32)
            history.my_name = form_data.my_name.data
            history.my_location_x = my_location.get("lat")
            history.my_location_y = my_location.get("lng")
            history.my_location = form_data.my_location.data
            history.my_photo = form_data.my_photo.data
            history.friend_fbuid = form_data.friend_fbuid.data
            history.friend_name = form_data.friend_name.data
            history.friend_location_x = friend_location.get("lat")
            history.friend_location_y = friend_location.get("lng")
            history.friend_location = form_data.friend_location.data
            history.friend_photo = form_data.friend_photo.data
            history.history_category = form_data.history_category.data
            history.history_category_name = history.get_category(form_data.history_category.data)
            history.history_detail = form_data.history_detail.data
            history.history_location = form_data.history_location.data
            history.image_01 = form_data.image_01.data
            history.image_02 = form_data.image_02.data
            history.image_03 = form_data.image_03.data
            history.created = datetime.datetime.now()
            history.enabled = True
            history.availabled = True
            history.save()
            self.get_json_response_and_finish(0, "success", history.to_object())
        except Exception as E:
            return self.get_json_response_and_finish(1000, "Error no controlado: "+str(E))

class HistoryCreateHandler(AuthBaseHandler, FacebookGraphMixin):

    @authenticated
    @asynchronous
    def get(self):
        self.msie_header_fix()
        self.facebook_request("/me/friends",
                              access_token=self.get_user_value("access_token"),
                              callback=self.async_callback(self._on_complete))

    def post(self):
        self.msie_header_fix()
        self.redirect(PATH_PATCH+'/history/create')

    def _on_complete(self, response):
        self.msie_header_fix()
        cookie = self.get_secure_cookie(COOKIE_TEMP)
        try:
            user = json_decode(cookie)
            facebook_name = user.get("name")
            facebook_user_id = user.get("id")
            facebook_picture = "https://graph.facebook.com/"+user.get("id")+"/picture?type=large"
            facebook_location = user.get("location")
            facebook_location = facebook_location.get("name") if facebook_location else ""
            facebook_access_token = self.get_user_value("access_token")
            facebook_friends_list = []
            facebook_friends_list_objects = response.get("data") or []
            action_token = "%s_%s" % (token(64),facebook_user_id)
            for a in facebook_friends_list_objects:
                try:
                    facebook_friends_list.append(a.get("name"))
                except: pass
            self.render("views/create.html",
                action_token=action_token,
                facebook_access_token=facebook_access_token,
                facebook_name=facebook_name,
                facebook_user_id=facebook_user_id,
                facebook_picture=facebook_picture,
                facebook_location=facebook_location,
                facebook_friends_list=json_encode(facebook_friends_list),
                facebook_friends_list_objects=json_encode(facebook_friends_list_objects)
            )
        except Exception: #as E:
            #return self.get_json_response_and_finish(1000, "Error no controlado: "+str(E))
            #return self.redirect(PATH_PATCH+'/history/create')
            return self.redirect(PATH_PATCH)

class HistoryCreateImageUploadHandler(AuthBaseHandler):
    def is_image(self, content_type):
        return content_type in ["image", "image/png","image/jpeg","image/pjpeg","image/jpg","image/gif"]

    def get_size_image(self, body):
        size = sys.getsizeof(body)
        return (size / 1024) <= 300

    def write_image(self, file_name, file_boby):
        try:
            f = open(file_name, 'w+')
            f.write(file_boby)
        except:
            return False
        finally:
            return True

    def get(self):
        if self.settings["debug"]:
            self.xsrf_force()
            self.render("views/upload.html", action_token=token(64))
        else:
            return self.redirect(PATH_PATCH)

    def post(self):
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        textplain_response = "json;%s"
        aid = self.get_argument("aid", None)
        action_token = self.get_argument("action_token", None)
        if not action_token:
            message = self.get_json_dumps(1, u"La clave de acceso no está definida.")
            return self.finish(textplain_response % message)
        files = self.request.files
        if not files:
            message = self.get_json_dumps(1, u"Por favor, debe seleccionar de uno a tres imégenes.")
            return self.finish(textplain_response % message)
        if len(files.keys()) > 3:
            message = self.get_json_dumps(1, u"Solo se permite un máximo de 3 archivos.")
            return self.finish(textplain_response % message)
        result = []
        PATH_WWW_IMG = "/static/img/histories"
        PATH_OS_IMG = self.settings.get("img_path")+"/histories"
        try:
            if not aid:
                file_pos = 0
                for fl in files:
                    fe = files[fl][0]
                    if not self.is_image(fe.content_type):
                        message = self.get_json_dumps(1, u"Solo se permiten subir imágenes.")
                        return self.finish(textplain_response % message)
                    if not self.get_size_image(fe.body):
                        message = self.get_json_dumps(1, u"El peso de las imágenes no puede ser mayor a 300KB.")
                        return self.finish(textplain_response % message)
                    file_pos += 1
                    file_extension =  str(os.path.splitext(fe.filename)[1]).lower()
                    file_name_new = "%s_%s%s" % (action_token, file_pos, file_extension)
                    file_path_new = "%s/%s" % (PATH_OS_IMG, file_name_new)
                    if self.write_image(file_path_new, fe.body):
                        result.append(PATH_WWW_IMG+"/"+file_name_new+"?ac="+token(8))
                if file_pos == 0:
                    message = self.get_json_dumps(1, u"No hay imágenes disponibles.")
                    return self.finish(textplain_response % message)
            else:
                if aid not in ["my", "friend"]:
                    message = self.get_json_dumps(1, u"El identificador '%s', no es válido." % aid)
                    return self.finish(textplain_response % message)
                fe = files["image"][0]
                if not self.is_image(fe.content_type):
                    message = self.get_json_dumps(1, u"Solo se permiten subir imágenes.")
                    return self.finish(textplain_response % message)
                if not self.get_size_image(fe.body):
                    message = self.get_json_dumps(1, u"El peso de las imágenes no puede ser mayor a 300KB.")
                    return self.finish(textplain_response % message)
                file_extension =  str(os.path.splitext(fe.filename)[1]).lower()
                file_name_new = "%s_%s%s" % (action_token, aid, file_extension)
                file_path_new = "%s/%s" % (PATH_OS_IMG, file_name_new)
                if self.write_image(file_path_new, fe.body):
                    result = dict(type=aid, id=PATH_WWW_IMG+"/"+file_name_new+"?ac="+token(8))
                else:
                    message = self.get_json_dumps(1, u"No hay imágenes disponibles.")
                    return self.finish(textplain_response % message)
            images = self.get_json_dumps(0, "success", result)
            self.finish(textplain_response % images)
        except Exception as E:
            message = self.get_json_dumps(1000, u"Error no controlado: "+str(E))
            return self.finish(textplain_response % message)

class HistoryEditSaveHandler(HistoryCreateSaveHandler):
    @authenticated
    def post(self):
        try:
            if not self.check_xsrf():
                return self.get_json_response_and_finish(1, u"Las claves de validación no concuerdan.")
            form_data = HistoryCreateSaveForm(self)
            if not form_data.validate():
                return self.get_json_response_and_finish(2, dict(errors=form_data.errors))
            email = self.get_user_value("email")
            if not email:
                return self.get_json_response_and_finish(1, u"El usurio no es válido.")
            history = History.get_by_action_token(form_data.action_token.data)
            if not history:
                return self.get_json_response_and_finish(1, u"La historia no existe.")
            if history.email != email:
                return self.get_json_response_and_finish(1, u"El usuario no posee privilegios.")
            my_location = self.get_geocode(form_data.my_location.data)
            if not my_location:
                return self.get_json_response_and_finish(1, u"Tu ubicación no es correcta.")
            my_location = my_location.get("results")[0].get("geometry").get("location")
            friend_location = self.get_geocode(form_data.friend_location.data)
            if not friend_location:
                return self.get_json_response_and_finish(1, u"La ubicación de tu amigo no es correcta.")
            friend_location = friend_location.get("results")[0].get("geometry").get("location")
            update_data = dict(
                set__my_name = form_data.my_name.data,
                set__my_location_x = my_location.get("lat"),
                set__my_location_y = my_location.get("lng"),
                set__my_location = form_data.my_location.data,
                set__my_photo = form_data.my_photo.data,
                set__friend_fbuid = form_data.friend_fbuid.data,
                set__friend_name = form_data.friend_name.data,
                set__friend_location_x = friend_location.get("lat"),
                set__friend_location_y = friend_location.get("lng"),
                set__friend_location = form_data.friend_location.data,
                set__friend_photo = form_data.friend_photo.data,
                set__history_category = form_data.history_category.data,
                set__history_category_name = history.get_category(form_data.history_category.data),
                set__history_detail = form_data.history_detail.data,
                set__history_location = form_data.history_location.data,
                set__image_01 = form_data.image_01.data,
                set__image_02 = form_data.image_02.data,
                set__image_03 = form_data.image_03.data,
                set__modified = datetime.datetime.now()
            )
            history.update(**update_data)
            history.reload()
            self.get_json_response_and_finish(0, "success", history.to_object())
        except Exception as E:
            return self.get_json_response_and_finish(1000, "Error no controlado: "+str(E))

class HistoryEditGetHandler(AuthBaseHandler, FacebookGraphMixin):

    @authenticated
    @asynchronous
    def get(self, uid=None):
        self.msie_header_fix()
        return self.facebook_request("/me/friends",
                                     access_token=self.get_user_value("access_token"),
                                     callback=self.async_callback(self._on_complete))

    def post(self, uid=None):
        self.msie_header_fix()
        self.redirect(PATH_PATCH+'/history/edit/'+uid)

    def _on_complete(self, response):
        self.msie_header_fix()
        cookie = self.get_secure_cookie(COOKIE_TEMP)
        try:
            uri = self.request.uri
            uid = uri.split("/")[-1]
            if uid:
                email = self.get_user_value("email")
                if not email:
                    return self.redirect(PATH_PATCH)
                history = History.get_by_token(uid)
                if not history:
                    return self.redirect(PATH_PATCH)
                if history.email != email:
                    return self.redirect(PATH_PATCH)
                user = json_decode(cookie)
                facebook_user_id = user.get("id")
                action_token = history.action_token
                history_data = history.to_object(["id"])
                facebook_access_token = self.get_user_value("access_token")
                facebook_friends_list = []
                facebook_friends_list_objects = response.get("data") or []
                for a in facebook_friends_list_objects:
                    try:
                        facebook_friends_list.append(a.get("name"))
                    except: pass
                self.render("views/edit.html",
                    action_token=action_token,
                    history_data=history_data,
                    facebook_user_id=facebook_user_id,
                    facebook_access_token=facebook_access_token,
                    facebook_friends_list=json_encode(facebook_friends_list),
                    facebook_friends_list_objects=json_encode(facebook_friends_list_objects))
            else:
                return self.redirect(PATH_PATCH)
        except Exception: #as E:
            return self.redirect(PATH_PATCH)
            #return self.get_json_response_and_finish(1001, "error", str(E))

#: -- Share --------------------------------------------------------------------
#: -----------------------------------------------------------------------------
#: -----------------------------------------------------------------------------
#: Handlers List, UI Modules List
#: -----------------------------------------------------------------------------
#: -----------------------------------------------------------------------------

handlers_list = [
    (r"/", MainHandler),
    (r"/auth/login", AuthFacebookHandler),
    (r"/auth/terms", AuthFacebookTermsHandler),
    (r"/history/([a-z0-9]{32})", HistoryGetHandler),
    (r"/history/create", HistoryCreateHandler),
    (r"/history/create/save", HistoryCreateSaveHandler),
    (r"/history/create/image/upload", HistoryCreateImageUploadHandler),
    (r"/history/edit/([a-z0-9]{32})", HistoryEditGetHandler),
    (r"/history/edit/save", HistoryEditSaveHandler),
    (r"/history/view/([a-z0-9]+)", HistoryViewHandler),
    (r"/history/publish/([a-z0-9]+)", HistoryPublishHandler),
    (r"/histories/list/(\d+)/(\d+)/(\d+)", HistoriesListHandler),
]

ui_modules_list = {}
