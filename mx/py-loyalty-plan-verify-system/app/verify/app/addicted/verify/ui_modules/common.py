#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 20/Feb/2014 15:04

from addicted.verify.core.regex import regex_normalize_email
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

    def normalize_card(self, value):
        if not value:
            return '-'
        return '%s...%s' % (value[0:1], value[-4:])

    def normalize_card_level(self, value):
        try:
            return {
                'a': 'Clear',
                'b': 'Platinum',
                'c': 'Black'
            }[value.lower()[0:1]]
        except Exception:
            return 'Clear'

    def normalize_email(self, value):
        if not value:
            return '-'
        return regex_normalize_email.sub('@...', value).lower()

    def normalize_phone(self, value):
        if not value or len(value) < 8:
            return '-'
        return 'xxxx-%s' % value[-4:]