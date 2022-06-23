#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 21/06/2013 09:10


import re
import copy
import datetime
import logging
import traceback
from json import dumps as json_dump
from math import ceil
from bson.json_util import dumps as mongo_dump
from casino8.common.utils import datetime_parser, str_complex_type
from casino8.handlers.configurations import DeviceConfiguration
from casino8.machines.configurations import DEVICE_LEVELS, BONUS_TIME, \
    BONUS_TIMES, AI_SESSION_MAXIMUM_BALANCE_BY, AI_SESSION_MAXIMUM_TIME, \
    AI_SESSION_MAXIMUM_BALANCE, AI_SESSION_MAXIMUM_SPINS, \
    AI_SESSION_MAXIMUM_BALANCE_PERC, AI_SESSION_MINIMUM_BALANCE_PERC
from casino8.security.sessions import SessionMixin
from tornado.web import RequestHandler

# Consts

uid_exp = r'(?i)(?<![a-z0-9])[0-f]{32}(?![a-z0-9])'
re_uid = re.compile(uid_exp)

fbuid_exp = r'^[\d]+$'
re_fbuid = re.compile(fbuid_exp)

sid_exp = r'(?i)(?<![a-z0-9])[0-f]{8}(?:-[0-f]{4}){3}-[0-f]{12}(?![a-z0-9])'
re_sid = re.compile(sid_exp)

ignore_regex = re.compile(r'(null|undefined)', re.I)


# Paginator

class Paginator(object):
    def __init__(self, page_number=0, page_size=50, total=0):
        self._page_number = page_number
        self._page_size = page_size
        self._total = total

    @property
    def total(self):
        return int(self._total)

    @property
    def page_total(self):
        return int(ceil(self.total/float(self.page_size)))

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

    def to_object(self):
        return dict(
            total=self.total,
            page_total=self.page_total,
            page_size=self.page_size,
            page_number=self.page_number,
            page_next=self.page_next,
            page_prev=self.page_prev,
        )


# Base Handler

class DataHelper(RequestHandler, SessionMixin):

    # Helper, Data Base

    @property
    def db(self):
        return self.application.db()

    def get_db(self, database):
        return self.application.db(database)

    @property
    def db_t8(self):
        return self.application.db_track()

    @property
    def db_s8(self):
        return self.application.db_social('social')

    @property
    def db_n8(self):
        return self.application.db_social('notify')

    @property
    def db_g8(self):
        return self.application.db('graph')

    def get_query_with_lowlogic(self, **kwargs):
        query = dict(enabled=True, available=True)
        query.update(copy.deepcopy(kwargs))
        return query

    # Helper, Config User

    @property
    def ai_session_enabled(self):
        try:
            return False  # self.session.data.get('ai_session_enabled', False)
        except Exception:
            return False

    def validate_fbuid(self, fbuid=None):
        try:
            if not fbuid:
                fbuid = self.get_argument('fbuid', '')
            if not re_fbuid.search(fbuid):
                raise ValueError('FB UID (!)')
        except Exception, e:
            raise ValueError('FB UID (%s)' % e or 'x')
        return fbuid

    def verify_fbuid(self, fbuid=None):
        try:
            return self.validate_fbuid(fbuid)
        except Exception:
            return False

    def verify_user_config(
            self, session=None, not_cache=True, not_update=False):
        if not session:
            session = self.session.data
        # ai_update = self.verify_user_ai_session(session, True)
        # if ai_update:
        #     session.update(**ai_update)
        gift_update = self.verify_gift_time(session, True)
        if gift_update:
            session.update(**gift_update)
        config, config_cache = self.verify_user_config_device(session)
        if not_update:
            return config if not_cache else config_cache
        session = self.session.data
        time_now = datetime.datetime.utcnow()
        query_update = {'$set': {
            'modified': time_now,
            'sid': session.get('sid'),
            'level': session.get('level'),
            'points': session.get('points'),
            'points_next_level': session.get('points_next_level'),
            'balance': session.get('balance'),
            'gift_total': session.get('gift_total'),
            'gift_award': session.get('gift_award'),
            'gift_available': session.get('gift_available'),
            'gift_time_begin': datetime_parser(session.get('gift_time_begin')),
            'gift_time_finish': datetime_parser(
                session.get('gift_time_finish')),
            # 'ai_session_enabled': session.get('ai_session_enabled'),
            # 'ai_session_spins': session.get('ai_session_spins'),
            # 'ai_session_balance': session.get('ai_session_balance'),
            # 'ai_session_begin': datetime_parser(
            #     session.get('ai_session_begin')),
            # 'ai_session_finish': datetime_parser(
            #     session.get('ai_session_finish')),
        }}
        fbuid = self.get_argument('fbuid', session.get('fbuid', None))
        if fbuid:
            self.db.profiles.update({'_id': fbuid}, query_update)
        else:
            self.db.devices.update({'_id': session.get('uid')}, query_update)
        return config if not_cache else config_cache

    def verify_user_config_device(self, session):
        config = DeviceConfiguration(**session)
        config_cache = config.todict()
        session.update(config=config_cache, **config.update_session())
        for key, value in session.items():
            if isinstance(value, datetime.date) \
                or isinstance(value, datetime.time) \
                    or isinstance(value, datetime.datetime):
                session[key] = value.isoformat()
        self.session.update(**session)
        return config, config_cache

    def verify_user_ai_session(self, session=None, not_update=False):
        if not session:
            session = self.session.data
        session_update = {}
        session_enabled = session.get('ai_session_enabled')
        session_spins = session.get('ai_session_spins')
        session_begin = datetime_parser(session.get('ai_session_begin'))
        session_finish = datetime_parser(session.get('ai_session_finish'))
        session_balance = session.get('ai_session_balance')
        session_balance_min_perc = \
            session_balance * AI_SESSION_MINIMUM_BALANCE_PERC
        session_balance_max_perc = \
            session_balance * AI_SESSION_MAXIMUM_BALANCE_PERC
        session_balance_max_by = \
            session_balance * AI_SESSION_MAXIMUM_BALANCE_BY
        balance = session.get('balance')
        time_now = datetime.datetime.utcnow()
        if not session_enabled and time_now > session_begin \
                and session_spins <= AI_SESSION_MAXIMUM_SPINS \
                and balance <= session_balance_min_perc:
            session_update = {
                'ai_session_enabled': True,
                'ai_session_spins': 0,
                'ai_session_balance': balance,
                'ai_session_begin': time_now,
                'ai_session_finish': time_now + datetime.timedelta(
                    hours=AI_SESSION_MAXIMUM_TIME
                ),
            }
        elif session_enabled \
            and (session_finish > time_now
                 or balance >= session_balance_max_perc
                 or balance >= session_balance_max_by
                 or session_spins >= AI_SESSION_MAXIMUM_SPINS
                 or balance >= AI_SESSION_MAXIMUM_BALANCE):
            new_time = \
                time_now + datetime.timedelta(hours=AI_SESSION_MAXIMUM_TIME/2)
            session_update = {
                'ai_session_enabled': False,
                'ai_session_spins': 0,
                'ai_session_balance': 0,
                'ai_session_begin': new_time,
                'ai_session_finish': new_time + datetime.timedelta(
                    hours=AI_SESSION_MAXIMUM_TIME
                ),
            }
        if not not_update and session_update:
            update = {'$set': session_update}
            fbuid = session.get('fbuid')
            if fbuid:
                self.db.profiles.update({'_id': fbuid}, update)
            else:
                self.db.devices.update({'_id': session.get('uid')}, update)
        return session_update

    def verify_gift_time(self, session=None, not_update=False):
        if not session:
            session = self.session.data
        gift_update = None
        gift_total = session.get('gift_total')
        gift_available = session.get('gift_available')
        gift_time = (
            datetime.datetime.utcnow() >
            datetime_parser(session.get('gift_time_finish'))
        )
        if not gift_available and gift_total >= BONUS_TIMES:
            time_now = datetime.datetime.utcnow()
            gift_update = dict(
                gift_total=0,
                gift_award=0,
                gift_available=False,
                gift_time_begin=time_now,
                gift_time_finish=time_now + datetime.timedelta(
                    hours=BONUS_TIME),
            )
        elif not gift_available and gift_time:
            gift_award = 0 if gift_total >= BONUS_TIMES else \
                DEVICE_LEVELS[session.get('level')-1][5]
            gift_update = dict(
                gift_award=gift_award,
                gift_available=True,
            )
        if not not_update and gift_update:
            update = {'$set': gift_update}
            fbuid = session.get('fbuid')
            if fbuid:
                self.db.profiles.update({'_id': fbuid}, update)
            else:
                self.db.devices.update({'_id': session.get('uid')}, update)
        return gift_update


class BaseHandler(DataHelper):
    # Helper, Debug

    def get(self, *args, **kwargs):
        if self.settings.get('debug', False):
            return self.post()
        return self.send_error(404)

    def head(self, *args, **kwargs):
        return self.send_error(404)

    def delete(self, *args, **kwargs):
        return self.send_error(404)

    def patch(self, *args, **kwargs):
        return self.send_error(404)

    def put(self, *args, **kwargs):
        return self.send_error(404)

    def options(self, *args, **kwargs):
        return self.send_error(404)

    # Helper, Properties

    @property
    def remote_ip(self):
        try:
            ip = self.request.headers.get('X-Real-Ip', self.request.remote_ip)
        except Exception:
            ip = self.request.remote_ip
        return self.request.headers.get('X-Forwarded-For', ip)

    # Helper, Arguments

    def get_arguments_list(self, args=None):
        result = dict()
        for key in args:
            result[key] = self.get_argument(key, None)
        return result

    def validate_arguments(self, *args):
        for arg in args:
            if not arg:
                raise KeyError('Arguments (?)')

    def do_paginate(self, page_number=0, page_size=50, total=0):
        return Paginator(page_number, page_size, total)

    # Helper, Response

    def get_object_response(self, e_id=0, e_message=None, response=None):
        return dict(error=dict(id=e_id, message=e_message), response=response)

    def get_json_response(self, **kwargs):
        data = self.get_object_response(**kwargs)
        return json_dump(data, default=str_complex_type)

    def get_json_response_and_finish(self, **kwargs):
        self.set_header_for_json()
        self.finish(self.get_json_response(**kwargs))

    def get_obj_json_response_and_finish(self, **kwargs):
        self.set_header_for_json()
        self.finish(json_dump(kwargs, default=str_complex_type))

    def get_mongo_json_response_and_finish(self, cursor, **kwargs):
        if not kwargs:
            kwargs = dict()
        kwargs['response'] = [document for document in cursor]
        self.set_header_for_json()
        self.finish(mongo_dump(self.get_object_response(**kwargs)))

    def get_except_json_response_and_finish(self, e_message, e_id=10000):
        logging.error(traceback.format_exc())
        logging.error(json_dump(
            self.request.arguments, default=str_complex_type, indent=2))
        self.get_json_response_and_finish(
            e_id=e_id, e_message='ERROR: %s' % e_message)

    def get_error_json_response_and_finish(self, e_id, e_message):
        self.get_json_response_and_finish(
            e_id=e_id, e_message='ERROR: %s' % e_message)

    def set_header_for_json(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
