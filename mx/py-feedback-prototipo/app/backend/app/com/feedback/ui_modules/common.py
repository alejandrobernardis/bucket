#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 20/Feb/2014 15:04

from com.feedback.core.regex import regex_normalize_email
from com.feedback.ui_modules.admin import ViewEvaluationsModule
from tornado.web import UIModule


class ViewErrorsModule(UIModule):
    def render(self, errors):
        return self.render_string(
            "ui_modules/common/view_errors.html",
            errors=errors or {}
        )


class ViewSearchResultModule(UIModule):
    def __init__(self, handler):
        super(ViewSearchResultModule, self).__init__(handler)

    def render(self, form, recordset):
        return self.render_string(
            "ui_modules/common/view_search_result.html",
            form=form or {},
            recordset=recordset or {},
            helpers=self
        )

    def normalize_email(self, value):
        if not value:
            return '-'
        return regex_normalize_email.sub('@...', value).lower()

    def normalize_phone(self, value):
        if not value or len(value) < 8:
            return '-'
        return 'xxxx-%s' % value[-4:]


class ViewMyEvaluationsModule(ViewEvaluationsModule):
    def render(self, form, evaluations):
        return self.render_string(
            "ui_modules/common/view_evaluations.html",
            form=form or {},
            evaluations=evaluations or {},
            helpers=self
        )


class ViewMyEvaluationsPendingModule(ViewEvaluationsModule):
    def render(self, pending):
        return self.render_string(
            "ui_modules/common/view_evaluations_pending.html",
            pending=pending,
            helpers=self
        )