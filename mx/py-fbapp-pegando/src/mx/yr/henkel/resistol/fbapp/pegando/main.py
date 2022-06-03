#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Aug 7, 2012, 12:30:32 PM

# -- meta-data -----------------------------------------------------------------

__project_name__ = u"YRHRPH"
__project_full_name__ = u"Y&R, Henkel, Resistol, Pegando Historias"
__project_owner__ = u"Young and Rubicam"
__project_author__ = u"Alejandro M. Bernardis"
__project_version__ = u"0.0.1"
__project_created__ = u"Aug 7, 2012, 12:30:32 PM"

#: -- bootstrap ----------------------------------------------------------------

import os, sys
p_root = os.path.abspath("../")
sys.path.insert(0, p_root+"/libs")
sys.path.insert(1, p_root+"/src")

#: -- imports ------------------------------------------------------------------

from com.ak.tornado.security import secret_key, Role
from mongoengine import connect as MongoConnect
from mx.yr.henkel.resistol.fbapp.pegando.handlers.common \
    import handlers_list as CommonHandlers
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options, parse_command_line

#: -- define -------------------------------------------------------------------

#: sys
define("debug", default=True)
define("port", default=8084, type=int)
define("ssl", default=False)
define("cookie_user_session", default="user_session")

#: facebook

if not options.debug:
    define("facebook_uid", default=1469798294)
    define("facebook_app_id", default=478746198811594)
    define("facebook_api_key", default=478746198811594)
    define("facebook_secret", default="3942d99ff1c86c6b947fb620888aafb3")
    define("facebook_login", "/facebook/app_new_pegando_historias/auth/login")

else:
    print '### DEBUG MODE ###'
    define("facebook_uid", default=1469798294)
    define("facebook_app_id", default=170639637185)
    define("facebook_api_key", default=170639637185)
    define("facebook_secret", default="f0c1e508947ca41e0b8b91c0bb7da11f")
    define("facebook_login", "/auth/login")

#: google
define("google_analytics_id", default="")
define("google_analytics_domain", default=None)
define("google_analytics_sdomains", default=None)
define("google_analytics_mdomains", default=None)
define("google_site_verification", default="")

#: email
define("email_smtp", default="smtp.gmail.com")
define("email_port", default=587)
define("email_user", default="mx.yr.mail@gmail.com")
define("email_pass", default="yrNSx09-mx3011")

#: database
define("database_user", default="sysadmin")
define("database_pass", default="yrHK+R1nD0M0!71+")
define("database_host", default="127.0.0.1")
define("database_port", default=27017)
define("database_ddbb", default="henkel_resistol_fbapp0001")
define("database_pool", default="henkel_resistol_fbapp0001_pool")
define("database_cach", default=10)
define("database_conn", default=100)

#: config

define("site_domain", default="www.resistol.com.mx/facebook/app_new_pegando_historias")

#: -- application --------------------------------------------------------------

class MainApplication(Application):
    def __init__(self):

        #: paths

        base_dir = os.path.dirname(__file__)
        static_dir = os.path.join(base_dir, "static")
        static_dir_dict = dict(path=static_dir)

        #: handlers

        handlers = [
            (r"/(crossdomain\.xml)", StaticFileHandler, static_dir_dict),
            (r"/(humans\.txt)", StaticFileHandler, static_dir_dict),
            (r"/(robots\.txt)", StaticFileHandler, static_dir_dict),
            (r"/(xd_receiver\.html)", StaticFileHandler, static_dir_dict),
            (r"/(channel\.html)", StaticFileHandler, static_dir_dict),]

        handlers.extend(CommonHandlers)

        #: roles

        Role("admin", admin=True)
        Role("moderator", write=True)
        Role("user")

        #: settings

        settings = dict(
            debug=options.debug,
            ssl=options.ssl,
            xsrf_cookies=True,
            cookie_secret=secret_key(64),
            cookie_user_session=options.cookie_user_session,
            hash_secret=secret_key(64),
            login_url=options.facebook_login,
            path=base_dir,
            static_path=static_dir,
            template_path=os.path.join(base_dir, "templates"),
            backup_path=os.path.join(base_dir, "backup"),
            tmp_path=os.path.join(base_dir, "tmp"),
            img_path=os.path.join(static_dir, "img"),
            upload_path=os.path.join(base_dir, "upload"),
            download_path=os.path.join(base_dir, "download"),
            ssl_path=os.path.join(base_dir, "CA"),
            facebook_uid=options.facebook_uid,
            facebook_app_id=options.facebook_app_id,
            facebook_api_key=options.facebook_api_key,
            facebook_secret=options.facebook_secret,
            google_analytics_id=options.google_analytics_id,
            google_analytics_domain=options.google_analytics_domain,
            google_analytics_sdomains=options.google_analytics_sdomains,
            google_analytics_mdomains=options.google_analytics_mdomains,
            google_site_verification=options.google_site_verification,
            email_smtp=options.email_smtp,
            email_port=options.email_port,
            email_user=options.email_user,
            email_pass=options.email_pass,
            #: misc
            site_domain=options.site_domain,)

        Application.__init__(self, handlers, **settings)

        self.db_mongo = MongoConnect(
            options.database_ddbb,
            host=options.database_host,
            port=options.database_port,
            username=options.database_user,
            password=options.database_pass,)

    def ssl_config(self):
        if not self.settings.get("ssl"):
            return None

        CA_dir = self.settings.get("ssl_path")
        return dict(certfile=os.path.join(CA_dir, "server.crt"),
                    keyfile=os.path.join(CA_dir, "server.key"))

#: -- main ---------------------------------------------------------------------

if __name__ == "__main__":
    try:
        parse_command_line()

        app = MainApplication()
        http_server = HTTPServer(app, xheaders=True,
                                 ssl_options=app.ssl_config())
        http_server.listen(options.port)
        IOLoop.instance().start()

    except KeyboardInterrupt:
        print "::: Server Stop :::", __project_full_name__

