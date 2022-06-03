#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Mar 31, 2012, 1:16:42 AM

# -- meta-data -----------------------------------------------------------------

__project_name__ = u"YRCLL"
__project_full_name__ = u"Y&R, xxx, Luminous, Landing"
__project_owner__ = u"Young and Rubicam"
__project_author__ = u"Alejandro M. Bernardis"
__project_version__ = u"0.0.1"
__project_created__ = u"Apr 10, 2012, 10:08:34 PM" 

#: -- bootstrap ----------------------------------------------------------------

import os, sys
p_root = os.path.abspath("../")
sys.path.insert(0, p_root+"/libs")
sys.path.insert(1, p_root+"/src")

#: -- imports ------------------------------------------------------------------

from mongoengine import connect as MongoConnect
from mx.yr.xxx.luminous.landing.handlers import common as CommonHandlers, \
                                                    admin as AdminHandlers
from mx.yr.tornado.security import secret_key, Role
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options, parse_command_line

#: -- define -------------------------------------------------------------------

define("debug", default=True)
define("port", default=8083, type=int)
define("ssl", default=False)
define("cookie_user_session", default="user_session")
define("html_title", default=u"xxx, Luminous")

define("facebook_uid", default=1469798294)
define("facebook_app_id", default=312228602179162)
define("facebook_api_key", default=312228602179162)
define("facebook_secret", default="1ecd283f9cf52201f7d5ea57b96a50ff")
'''
define("facebook_app_id", default=170639637185)
define("facebook_api_key", default=170639637185)
define("facebook_secret", default="f0c1e508947ca41e0b8b91c0bb7da11f")
'''
define("twitter_api_key", default=None)
define("twitter_secret", default=None)

define("google_analytics_id", default="UA-31191468-1")
define("google_analytics_domain", default=None)
define("google_analytics_sdomains", default=None)
define("google_analytics_mdomains", default=None)
define("google_site_verification", default="yJ7smLwQKL_rXDXudocgcS0uFfmrH_vBpLEXej-TFTg")

define("omniture_analytics", default=True)

define("email_smtp", default="smtp.gmail.com")
define("email_port", default=587)
define("email_user", default="mx.yr.mail@gmail.com")
define("email_pass", default="yrNSx09-mx3011")

define("database_user", default="sysadmin")
define("database_pass", default="yrCP+M0nD8!13+")
define("database_host", default="127.0.0.1")
define("database_port", default=27017)
define("database_ddbb", default="xxx_luminous_landing")
define("database_pool", default="xxx_luminous_landing_pool")
define("database_cach", default=10)
define("database_conn", default=100)

define("max_redeem_register", default=3)
define("max_redeem_accesories", default=10)
define("max_redeem_tickets", default=1000)
define("max_redeem_game", default=2000)
define("max_redeem_tickets_token", default=5)
define("max_legal_audit", default=3)
define("max_legal_audit_accesories", default=5)
define("min_legal_age", default=18)

define("xxx_domain", default="www.xxxluminouswhite.com.mx")
define("xxx_domain_inc", default="www.xxx.com.mx")

#: -- application --------------------------------------------------------------

class MainApplication(Application):

    def __init__(self):
        base_dir = os.path.dirname(__file__)
        static_dir = os.path.join(base_dir, "static")
        static_dir_dict = dict(path=static_dir)
        
        #: handlers
        
        handlers = [
            (r"/(crossdomain\.xml)", StaticFileHandler, static_dir_dict),
            (r"/(humans\.txt)", StaticFileHandler, static_dir_dict),
            (r"/(robots\.txt)", StaticFileHandler, static_dir_dict),
            (r"/(xd_receiver\.html)", StaticFileHandler, static_dir_dict),]
        
        handlers.extend(CommonHandlers.handlers_list)
        handlers.extend(AdminHandlers.handlers_list)
        
        #: roles
        
        Role("admin", admin=True)
        Role("user")
        
        #: settings
        
        settings = dict(
            debug=options.debug,
            ssl=options.ssl,
            xsrf_cookies=True,
            cookie_secret=secret_key(64),
            cookie_user_session=options.cookie_user_session,
            hash_secret=secret_key(64),
            login_url="/auth/login",
            html_title=options.html_title,
            path=base_dir,
            static_path=static_dir,
            template_path=os.path.join(base_dir, "templates"),
            backup_path=os.path.join(base_dir, "backup"),
            upload_path=os.path.join(base_dir, "upload"),
            download_path=os.path.join(base_dir, "download"),
            ssl_path=os.path.join(base_dir, "CA"),
            
            facebook_uid=options.facebook_uid,
            facebook_app_id=options.facebook_app_id,
            facebook_api_key=options.facebook_api_key,
            facebook_secret=options.facebook_secret,
            
            twitter_api_key=options.twitter_api_key,
            twitter_secret=options.twitter_secret,
            
            google_analytics_id=options.google_analytics_id,
            google_analytics_domain=options.google_analytics_domain,
            google_analytics_sdomains=options.google_analytics_sdomains,
            google_analytics_mdomains=options.google_analytics_mdomains,
            google_site_verification=options.google_site_verification,
            
            email_smtp=options.email_smtp,
            email_port=options.email_port,
            email_user=options.email_user,
            email_pass=options.email_pass,
            
            roles=Role.get_roles(),
            
            max_redeem_register=options.max_redeem_register,
            max_redeem_accesories=options.max_redeem_accesories,
            max_redeem_tickets=options.max_redeem_tickets,
            max_redeem_game=options.max_redeem_game,
            max_redeem_tickets_token=options.max_redeem_tickets_token,
            max_legal_audit=options.max_legal_audit,
            max_legal_audit_accesories=options.max_legal_audit_accesories,
            min_legal_age=options.min_legal_age,
            
            xxx_domain=options.xxx_domain,
            xxx_domain_inc=options.xxx_domain_inc,)
        
        Application.__init__(self, handlers, **settings)
        
        MongoConnect(
            options.database_ddbb,
            host=options.database_host,
            port=options.database_port,
            username=options.database_user,
            password=options.database_pass)
        
    def ssl_config(self):
        if not self.settings.get("ssl"):
            return None
        
        CA_dir = self.settings.get("ssl_path")
        return dict(certfile=os.path.join(CA_dir, "server.crt"), 
                    keyfile=os.path.join(CA_dir, "server.key"))

#: -- main ---------------------------------------------------------------------

def main():
    try:
        parse_command_line()
        
        app = MainApplication()
        http_server = HTTPServer(app, xheaders=True, 
                                 ssl_options=app.ssl_config())
        http_server.listen(options.port)
        IOLoop.instance().start()
        
    except KeyboardInterrupt:
        print "::: Server Stop :::", __project_full_name__

if __name__ == "__main__":
    main()

