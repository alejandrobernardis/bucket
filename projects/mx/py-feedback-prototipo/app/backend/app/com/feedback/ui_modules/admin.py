#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 24/Mar/2014 17:29

import cgi
from com.feedback.core.utils import SuperObject, mexico_time_zone
from com.feedback.security.roles import role_admin, role_user, role_guest
from com.feedback.ui_modules.utils import helper_provider, helper_dispatch, \
    helper_rate, helper_rate_label, helper_answer_mode
from tornado.web import UIModule

# levels
level_admin = role_admin.key.title()
level_user = role_user.key.title()
level_guest = role_guest.key.title()
LEVELS_LIST = (level_admin, level_user,)
DISPATCH_LIST = ('Cada semana', 'Cada 2 semanas', 'Cada 4 semanas',)


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

    def normalize_provider(self, value):
        return helper_provider(value)

    def normalize_last_login(self, value):
        return mexico_time_zone(value)

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
            '<li class="%s"><a class="js-button ladda-button" '
            'href="javascript:void(0);" data-action="change-level" '
            'data-token="%s" data-style="zoom-in">'
            '<span class="ladda-label">%s</span></a></li>'
            % ('' if item != level else 'active', uid, item)
            for item in LEVELS_LIST
        ])

    def normalize_dispatch(self, value):
        return helper_dispatch(value)

    def get_dispatch_list(self, value, uid):
        level = self.normalize_dispatch(value)
        return ''.join([
            '<li class="%s"><a class="js-button ladda-button" '
            'href="javascript:void(0);" data-action="change-dispatch" '
            'data-token="%s" data-style="zoom-in">'
            '<span class="ladda-label">%s</span></a></li>'
            % ('' if item != level else 'active', uid, item)
            for item in DISPATCH_LIST
        ])

    def check_session(self, value):
        try:
            return not not self.handler.application.\
                session_client().get(str(value))
        except:
            return False


class ViewRegisterModule(ViewUsersModule):
    def render(self, form, users):
        return self.render_string(
            "ui_modules/admin/view_register.html",
            form=form or {},
            users=users or {},
            helpers=self
        )


class ViewEvaluationsModule(UIModule):
    def render(self, form, evaluations):
        return self.render_string(
            "ui_modules/admin/view_evaluations.html",
            form=form or {},
            evaluations=evaluations or {},
            helpers=self
        )
        
    def normalize_mode(self, value):
        return helper_answer_mode(value)

    def normalize_rate(self, value):
        return helper_rate(value)

    def normalize_rate_label(self, value):
        return helper_rate_label(value)

    def normalize_provider(self, value):
        return helper_provider(value)

    def normalize_description(self, value, style=''):
        if len(value):
            value = '</p><p class="{0}">' \
                .format(style).join(cgi.escape(value).split('\n'))
            return '<p class="%s">%s</p>' % (style, value)
        # return '<p class="text-muted %s">' \
        #        '<span class="fa fa-exclamation-circle text-muted"></span>&nbsp;' \
        #        'Sin comentarios.</p>' % style
        return ''

    def normalize_created_date(self, value):
        return mexico_time_zone(value)


class ViewExecutivesModule(UIModule):
    def render(self, form, executives):
        return self.render_string(
            "ui_modules/admin/view_executives.html",
            form=form,
            executives=executives or [],
            helpers=self
        )

    def normalize_user(self, value):
        if isinstance(value, dict):
            return SuperObject(**value)
        return value
