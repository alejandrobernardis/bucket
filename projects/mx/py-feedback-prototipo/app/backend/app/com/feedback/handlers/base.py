#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 02/Dec/2013 17:58

import copy
import datetime
import math
from bson.json_util import dumps as mongo_dump
from com.feedback.core.utils import str_complex_type, trace_error
from com.feedback.security.auth import IdentityMixin
from com.feedback.security.session import SessionMixin
from tasks import push__audits, push__logs
from json import dumps as json_dump
from tornado.web import RequestHandler


class Paginator(object):
    def __init__(self, page_number=0, page_size=50, total=0, query=None):
        self._page_number = page_number
        self._page_size = page_size
        self._total = total
        self._query = query

    @property
    def total(self):
        return int(self._total)

    @property
    def page_total(self):
        return int(math.ceil(self.total/float(self.page_size)))

    @property
    def page_number(self):
        return int(self._page_number)

    @property
    def page_size(self):
        return int(self._page_size)

    @property
    def page_next(self):
        if self.page_number < self.page_total:
            return self.page_number + 1
        else:
            return self.page_total

    @property
    def page_prev(self):
        if self.page_number > 1:
            return self.page_number - 1
        else:
            return 1

    @property
    def page_query(self):
        return self._query

    def to_object(self):
        return {
            'total': self.total,
            'page_total': self.page_total,
            'page_size': self.page_size,
            'page_number': self.page_number,
            'page_next': self.page_next,
            'page_prev': self.page_prev,
            'page_query': self.page_query
        }

    def to_json(self):
        return json_dump(self.to_object())


class BaseHandler(RequestHandler, IdentityMixin, SessionMixin):
    @property
    def debug(self):
        return self.settings.get('debug', False)

    @property
    def track(self):
        return self.settings.get('track', False)

    @property
    def remote_ip(self):
        try:
            ip = self.request.headers.get('X-Real-Ip', self.request.remote_ip)
        except Exception:
            ip = self.request.remote_ip
        return self.request.headers.get('X-Forwarded-For', ip)

    def get_arguments_list(self, args=None):
        result = dict()
        for key in args:
            result[key] = self.get_argument(key, None)
        return result

    def validate_arguments(self, *args):
        for arg in args:
            if not arg:
                raise KeyError('Arguments (?)')

    def paginate(self, page_number=0, page_size=50, total=0, query=None):
        return Paginator(page_number, page_size, total, query)

    def goto_root(self):
        self.redirect(self.root_url)

    def goto_next_or_root(self):
        self.redirect(self.next_url)

    @property
    def root_url(self):
        return self.settings.get('site_root', '/')

    @property
    def next_url(self):
        return self.get_argument(
            'next', self.get_argument('next_url', self.root_url))

    def get_current_user(self):
        try:
            return self.session.data
        except Exception:
            return {}

    @property
    def db(self):
        return self.application.database('default')

    @property
    def mongo(self):
        return self.application.raw_pymongo('default')

    def database(self, name, configuration=None):
        return self.application.database(name, configuration)

    def pymongo(self, connection):
        return self.application.raw_pymongo(connection)

    @property
    def sql_db(self):
        return self.application.sql_database()

    def logic_low(self, enabled=True, available=True, **kwargs):
        query = {'enabled': enabled, 'available': available}
        if kwargs:
            query.update(copy.deepcopy(kwargs))
        return query

    def base_record(self, date=None, enabled=True, available=True, **kwargs):
        if not date:
            date = datetime.datetime.utcnow()
        query = self.logic_low(enabled, available, **kwargs)
        query['created'] = date
        query['modified'] = date
        return query

    def audit_push(self, message, activity=None, user=None):
        self._audit_log_helper(push__audits, activity, message, user)

    def log_push(self, message, activity=None, user=None):
        self._audit_log_helper(push__logs, activity, message, user)

    def _audit_log_helper(self, func, activity, message, user):
        if not self.track:
            return
        try:
            if not activity:
                activity = self.request.uri
            try:
                self.verify_session()
                session = self.session.sid
                user = self.session.data.get('username')
            except Exception:
                session = None
                user = user
            func.delay(**{
                'activity': activity,
                'message': message,
                'session': session,
                'user': user,
                'remote_ip': self.remote_ip,
            })
        except Exception:
            pass

    def set_header_for_json(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

    def get_object_response(self, e_id=None, e_message=None, response=None):
        data = {
            'error': {
                'id': e_id or 0,
                'message': e_message or 'success'
            }
        }
        if response:
            data['response'] = response
        return data

    def get_json_response(self, **kwargs):
        data = self.get_object_response(**kwargs)
        return json_dump(data, default=str_complex_type).replace("</", "<\\/")

    def get_json_response_and_finish(self, **kwargs):
        self.set_header_for_json()
        self.finish(self.get_json_response(**kwargs))

    def get_obj_json_response_and_finish(self, **kwargs):
        self.set_header_for_json()
        self.finish(
            json_dump(kwargs, default=str_complex_type).replace("</", "<\\/")
        )

    def get_mongo_json_response_and_finish(self, cursor, **kwargs):
        if not kwargs:
            kwargs = {}
        kwargs['response'] = [document for document in cursor]
        self.set_header_for_json()
        self.finish(
            mongo_dump(
                self.get_object_response(**kwargs)
            ).replace("</", "<\\/")
        )

    def get_mongoengine_json_response_and_finish(self, cursor, **kwargs):
        if not kwargs:
            kwargs = {}
        kwargs['response'] = [document.to_json() for document in cursor]
        self.set_header_for_json()
        self.finish(
            mongo_dump(
                self.get_object_response(**kwargs)
            ).replace("</", "<\\/")
        )

    def get_except_json_response_and_finish(self, e_message, e_id=10000):
        trace_error(self.request.arguments)
        self.get_json_response_and_finish(
            e_id=e_id, e_message=e_message.encode('utf-8'))

    def get_error_json_response_and_finish(self, e_id, e_message):
        self.get_json_response_and_finish(
            e_id=e_id, e_message=e_message.encode('utf-8'))


class CommonBaseHandler(BaseHandler):
    _form = None
    _template = None

    def render(self, **kwargs):
        if not kwargs:
            kwargs = {}
        if not self._form or 'form' not in kwargs:
            kwargs['form'] = self._form()
        super(CommonBaseHandler, self).render(self._template, **kwargs)