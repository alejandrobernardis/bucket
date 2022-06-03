#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Jan 7, 2013 10:33:43 AM

#: imports
import functools, urllib, urlparse
from com.ak.common.roles import Role
from tornado.web import HTTPError

#: utils
def authenticated_plus(*roles):
    def wrap(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if self.request.method in ("GET", "POST", "HEAD"):
                if not self.current_user:
                    url = self.get_login_url()
                    if "?" not in url:
                        if urlparse.urlsplit(url).scheme:
                            next_url = self.request.full_url()
                        else:
                            next_url = self.request.uri
                        url += "?" + urllib.urlencode(dict(next=next_url))
                    self.redirect(url)
                    return
                else:
                    user = self.get_user_value("role_id")
                    perms = Role.get_role_by_value(user).name
                    if perms in roles:
                        return method(self, *args, **kwargs)
            raise HTTPError(403)
        return wrapper
    return wrap

def roles(*roles):
    def wrap(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if self.current_user:
                user = self.get_user_value("role_id")
                perms = Role.get_role_by_value(user).name
                if perms in roles:
                    return method(self, *args, **kwargs)
            raise HTTPError(403)
        return wrapper
    return wrap