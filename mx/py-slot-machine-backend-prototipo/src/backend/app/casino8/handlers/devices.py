#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 05/09/2013 20:21

import re
import datetime
from casino8.common.utils import hash_uid, datetime_parser
from casino8.handlers.base import BaseHandler
from casino8.machines.configurations import DEVICE_LEVELS, BONUS_TIME, \
    BONUS_TIMES, DEFAULT_BALANCE, DEFAULT_LEVEL, DEFAULT_POINTS_NEXT_LEVEL, \
    DEFAULT_FACEBOOK_SYNC  #, AI_SESSION_MAXIMUM_TIME
from casino8.security.base import token
from casino8.security.iron_man import IronMan
from casino8.security.sessions import session_verify
from settings import LANGUAGES_DEFAULT


re_gift_time = re.compile(r'\d{1,2}:\d{2}:\d{2}(\.\d+)?')


class MainHandler(BaseHandler):
    def get(self):
        self.get_json_response_and_finish(
            e_message='success',
            response={'name': 'Casino8', 'status': True}
        )


class GetUserConfigHandler(BaseHandler):
    def post(self, *args, **kwargs):
        try:
            not_update = False
            uid = self.get_argument('uid', None)

            if uid and not self.session_verify():
                self.session_start()

            elif not uid:
                not_update = True
                i = self.get_argument('i', None)
                fbuid = self.get_argument('fbuid', None)
                device = self.get_argument('device', None)
                lang = self.get_argument('lang', LANGUAGES_DEFAULT)

                self.validate_arguments(i, device)

                device = str(device).lower()

                if device not in self.settings.get('platforms', []):
                    raise ValueError('Device (?)')

                elif not IronMan.defense(i):
                    raise ValueError('Iron Man (?)')

                uid = token()
                balance = DEFAULT_BALANCE
                time_now = datetime.datetime.utcnow()

                query_device = dict(
                    _id=uid,
                    fbuid=fbuid,
                    device=device,
                    lang=lang,
                    level=DEFAULT_LEVEL,
                    points=0,
                    points_next_level=DEFAULT_POINTS_NEXT_LEVEL,
                    balance=balance,
                    gift_total=0,
                    gift_award=0,
                    gift_available=False,
                    gift_time_begin=time_now,
                    gift_time_finish=time_now + datetime.timedelta(
                        hours=BONUS_TIME
                    ),
                    last_login=time_now,
                    created=time_now,
                    modified=time_now,
                    enabled=True,
                    available=True,
                    # ai_session_enabled=False,
                    # ai_session_balance=balance,
                    # ai_session_begin=time_now,
                    # ai_session_finish=time_now + datetime.timedelta(
                    #     hours=AI_SESSION_MAXIMUM_TIME
                    # ),
                    # ai_session_spins=0
                )

                if self.verify_fbuid(fbuid):
                    uid_fbuid = hash_uid(uid, fbuid)
                    profile = self.db.profiles.find_one({'_id': fbuid})

                    if not profile:
                        query_profile = query_device.copy()
                        balance += DEFAULT_FACEBOOK_SYNC

                        for key in ('fbuid', 'device',):
                            del query_profile[key]

                        query_profile['_id'] = fbuid
                        query_profile['devices'] = [uid_fbuid]
                        query_profile['balance'] = balance
                        # query_profile['ai_session_balance'] = balance
                        self.db.profiles.insert(query_profile)

                    elif uid_fbuid not in profile.get('devices'):
                        query_profile = self.get_query_with_lowlogic(
                            _id=fbuid, devices={'$ne': uid_fbuid}
                        )

                        self.db.profiles.update(query_profile, {
                            '$inc': {'balance': balance},
                            '$push': {'devices': uid_fbuid}
                        })

                    self.request.arguments['fbuid'] = [fbuid]

                self.db.devices.insert(query_device)
                self.request.arguments['uid'] = [uid]
                self.session_start()

            return self.get_json_response_and_finish(
                response=self.verify_user_config(
                    not_cache=False, not_update=not_update
                )
            )

        except Exception, e:
            return self.get_except_json_response_and_finish(e, 100)


class VerifyDeviceHandler(BaseHandler):
    def post(self, *args, **kwargs):
        try:
            i = self.get_argument('i', None)
            uid = self.get_argument('uid', None)
            sid = self.get_argument('sid', None)
            fbuid = self.get_argument('fbuid', None)
            self.validate_arguments(i, uid, sid)

            if not IronMan.defense(i):
                raise ValueError('Iron Man (?)')

            elif fbuid and not self.verify_fbuid(fbuid):
                raise ValueError('Facebook User ID (!)')

            elif not self.session_verify():
                if not self.session.is_empty:
                    self.session.revoke()
                self.session_start()

            return self.get_json_response_and_finish(
                response=self.verify_user_config(not_cache=False))

        except Exception, e:
            return self.get_except_json_response_and_finish(e, 101)


class SyncDeviceHandler(BaseHandler):
    @session_verify
    def post(self, *args, **kwargs):
        try:
            i = self.get_argument('i', None)
            fbuid = self.get_argument('facebookid', None)
            self.validate_arguments(i, fbuid)
            self.validate_fbuid(fbuid)
            session = self.session.data

            if not IronMan.defense(i):
                raise ValueError('Iron Man (?)')

            elif session.get('fbuid', None):
                raise ValueError('Sync Facebook User ID (!)')

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
                'gift_time_begin': datetime_parser(
                    session.get('gift_time_begin')),
                'gift_time_finish': datetime_parser(
                    session.get('gift_time_finish'))
            }}

            uid_fbuid = hash_uid(session['uid'], fbuid)
            profile = self.db.profiles.find_one({'_id': fbuid})

            if not profile:
                balance = session.get('balance') + DEFAULT_FACEBOOK_SYNC
                query_update['$set']['_id'] = fbuid
                query_update['$set']['devices'] = [uid_fbuid]
                query_update['$set']['enabled'] = True
                query_update['$set']['available'] = True
                query_update['$set']['created'] = time_now
                query_update['$set']['balance'] = balance
                query_update['$set']['lang'] = session.get('lang')
                query_update['$set']['last_login'] = \
                    datetime_parser(session.get('last_login'))
                # query_update['$set']['ai_session_enabled'] = \
                #     session.get('ai_session_enabled')
                # query_update['$set']['ai_session_spins'] = \
                #     session.get('ai_session_spins')
                # query_update['$set']['ai_session_balance'] = \
                #     session.get('ai_session_balance')
                # query_update['$set']['ai_session_begin'] = datetime_parser(
                #     session.get('ai_session_begin'))
                # query_update['$set']['ai_session_finish'] = datetime_parser(
                #     session.get('ai_session_finish'))
                self.db.profiles.insert(query_update['$set'])

            elif len(profile.get('devices')) >= 100:
                raise ValueError('Can\'t Sync Device (x > 100)')

            else:
                if uid_fbuid not in profile.get('devices'):
                    query_update['$push'] = {'devices': uid_fbuid}

                session_balance = session.get('balance') - 200
                balance = 0 if session_balance < 0 else session_balance

                query_update['$set']['balance'] = float(
                    balance + profile.get('balance')
                )

                points = profile.get('points')

                if points > session.get('points'):
                    query_update['$set']['points'] = points

                level = profile.get('level')

                if level > session.get('level'):
                    query_update['$set']['level'] = level

                gift_total = profile.get('gift_total')

                if gift_total > session.get('gift_total'):
                    query_update['$set']['gift_total'] = gift_total

                gift_available = profile.get('gift_available')

                if gift_available:
                    query_update['$set']['gift_award'] = \
                        profile.get('gift_award')
                    query_update['$set']['gift_available'] = \
                        gift_available

                gift_time_finish = profile.get('gift_time_finish')
                gift_time_finish_session = \
                    datetime_parser(session.get('gift_time_finish'))

                if gift_available \
                        or gift_time_finish > gift_time_finish_session:
                    query_update['$set']['gift_time_begin'] = \
                        profile.get('gift_time_begin')
                    query_update['$set']['gift_time_finish'] = \
                        gift_time_finish

                self.db.profiles.update({'_id': fbuid}, query_update)

            del self.request.arguments['facebookid']

            self.session.revoke()
            self.request.arguments['fbuid'] = [fbuid]
            self.request.arguments['device'] = [session.get('device')]
            self.session_start()

            return self.get_json_response_and_finish(
                response=self.verify_user_config(not_cache=False)
            )

        except Exception, e:
            return self.get_except_json_response_and_finish(e, 102)


class DisconnectDeviceHandler(BaseHandler):
    @session_verify
    def post(self, *args, **kwargs):
        try:
            i = self.get_argument('i', None)
            fbuid = self.get_argument('fbuid', None)

            self.validate_arguments(i, fbuid)
            self.validate_fbuid(fbuid)

            session = self.session.data
            session_fbuid = session.get('fbuid', None)

            if not IronMan.defense(i):
                raise ValueError('Iron Man (?)')

            elif not session_fbuid or session_fbuid != fbuid:
                raise ValueError('Sync Facebook User ID (!)')

            elif not self.session.is_empty:
                self.session_destroy()

            time_now = datetime.datetime.utcnow()

            try:
                time_finish = time_now + datetime.timedelta(hours=BONUS_TIME)
                # ai_time_finish = time_now + datetime.timedelta(
                #     hours=AI_SESSION_MAXIMUM_TIME
                # )
                self.db.devices.update({
                    '_id': self.get_argument('uid')
                }, {
                    '$set': {
                        'fbuid': None,
                        'level': DEFAULT_LEVEL,
                        'points': 0,
                        'points_next_level': DEFAULT_POINTS_NEXT_LEVEL,
                        'balance': DEFAULT_BALANCE,
                        'gift_total': 0,
                        'gift_award': 0,
                        'gift_available': False,
                        'gift_time_begin': time_now,
                        'gift_time_finish': time_finish,
                        'last_login': time_now,
                        'modified': time_now,
                        # 'ai_session_enabled': False,
                        # 'ai_session_balance': DEFAULT_BALANCE,
                        # 'ai_session_begin': time_now,
                        # 'ai_session_finish': ai_time_finish,
                        # 'ai_session_spins': 0,
                    }
                })
            except:
                raise ValueError('Can\'t reset device data')

            self.request.arguments['fbuid'] = []
            self.session_start()

            return self.get_json_response_and_finish(
                response=self.verify_user_config(not_cache=False)
            )

        except Exception, e:
            return self.get_except_json_response_and_finish(e, 103)


class TimeDeviceHandler(BaseHandler):
    def post(self, *args, **kwargs):
        try:
            i = self.get_argument('i', None)
            uid = self.get_argument('uid', None)
            fbuid = self.get_argument('fbuid', None)

            self.validate_arguments(i, uid)

            session_enabled = \
                (not self.session.is_empty and self.session_verify())

            if not IronMan.defense(i):
                raise ValueError('Iron Man (x)')

            elif fbuid and not self.verify_fbuid(fbuid):
                raise ValueError('Facebook User ID (x)')

            elif session_enabled:
                profile = self.session.data

            elif fbuid:
                profile = self.db.profiles.find_one(
                    {'_id': fbuid, 'devices': hash_uid(uid, fbuid)}
                )

            elif uid:
                profile = self.db.devices.find_one({'_id': uid})

            else:
                raise ValueError('Can\'t not process data (x)')

            time_now = datetime.datetime.utcnow()
            gift_update = None
            gift_total = profile.get('gift_total')
            gift_available = profile.get('gift_available')
            gift_time_finish = datetime_parser(profile.get('gift_time_finish'))
            gift_time = (time_now > gift_time_finish)

            if not gift_available and gift_total >= BONUS_TIMES:
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
                    DEVICE_LEVELS[profile.get('level')-1][5]
                gift_update = dict(
                    gift_award=gift_award,
                    gift_available=True,
                )

            if gift_update:
                update = {'$set': gift_update}
                if fbuid:
                    self.db.profiles.update({'_id': fbuid}, update)
                else:
                    self.db.devices.update({'_id': uid}, update)
                if session_enabled:
                    self.session.update(**gift_update)

            value = re_gift_time.match(str(gift_time_finish - time_now))
            result = '00:00:00' \
                if not value else str(value.group()).split('.')[0]
            return self.get_json_response_and_finish(response=result)

        except Exception, e:
            return self.get_except_json_response_and_finish(e, 104)


handlers_list = [
    (r'/', MainHandler),
    (r'/do/device/config/?', GetUserConfigHandler),
    (r'/do/device/verify/?', VerifyDeviceHandler),
    (r'/do/device/sync/?', SyncDeviceHandler),
    (r'/do/device/disconnect/?', DisconnectDeviceHandler),
    (r'/do/device/time/?', TimeDeviceHandler),
    (r'/do/device/push/notification/?', TimeDeviceHandler),

]
