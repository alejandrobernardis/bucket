#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 24/Mar/2014 17:29

from dateutil import tz
from addicted.verify.core.utils import SuperObject
from addicted.verify.security.roles import role_admin, role_user, role_guest
from tornado.web import UIModule

# time zones
time_zone_utc = tz.gettz('UTC')
time_zone_mexico = tz.gettz('America/Mexico_City')

# levels
level_admin = role_admin.key.title()
level_user = role_user.key.title()
level_guest = role_guest.key.title()
LEVELS_LIST = (level_admin, level_user, level_guest,)


class ViewUsersModule(UIModule):
    def render(self, form, users):
        return self.render_string(
            "ui_modules/admin/view_users.html",
            form=form or {},
            users=users or {},
            helpers=self
        )

    def normalize_user(self, value):
        if isinstance(value, dict):
            return SuperObject(**value)
        return value

    def normalize_last_login(self, value):
        utc = value.replace(tzinfo=time_zone_utc)
        return utc.astimezone(time_zone_mexico).strftime('%Y-%m-%d %H:%M:%S')

    def normalize_level(self, value):
        keys = value.keys()
        if role_admin.key in keys:
            return level_admin
        if role_user.key in keys:
            return level_user
        return level_guest

    def get_level_list(self, value, uid):
        level = self.normalize_level(value)
        return ''.join([
            '<li class="{0}"><a class="js-button ladda-button" '
            'href="javascript:void(0);" data-action="change-level" '
            'data-token="{1}" data-style="zoom-in">'
            '<span class="ladda-label">{2}</span></a></li>'
            .format('' if item != level else 'active', uid, item)
            for item in LEVELS_LIST
        ])


class ViewRegisterModule(ViewUsersModule):
    def render(self, form, users):
        return self.render_string(
            "ui_modules/admin/view_register.html",
            form=form or {},
            users=users or {},
            helpers=self
        )