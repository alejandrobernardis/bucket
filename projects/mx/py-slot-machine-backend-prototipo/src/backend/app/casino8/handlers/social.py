#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 02/09/2013 08:40

import datetime
from celery_tasks import push_social_actions, push_social_activity, \
    push_pull_notifications
from casino8.common.utils import week_range
from casino8.handlers.base import BaseHandler, ignore_regex
from casino8.security.sessions import session_verify


SHARE_BONUS = 200
SEND_GIFT_TOTAL = 2000
SEND_GIFT_FRIEND = 200
REQUEST_GIFT_TOTAL = 2000
REQUEST_GIFT_FRIEND = 200
INVITE_TOTAL = 2000
INVITE_FRIEND = 10


class SocialShareBonusHandler(BaseHandler):
    @session_verify
    def post(self, *args, **kwargs):
        try:
            action = 'share.bonus'
            session = self.session.data
            fbuid = session.get('fbuid', None)
            balance = self.get_argument('balance', None)
            friends = self.get_argument('friends', None)
            self.validate_arguments(balance, friends)
            self.validate_fbuid(fbuid)
            date = datetime.datetime.utcnow()
            today = datetime.datetime(date.year, date.month, date.day)

            if friends.startswith(','):
                friends = friends[1:]
            elif ignore_regex.search(friends):
                raise ValueError('Friends List (!)')

            friends_set = set(friends.split(','))

            if not len(friends_set):
                raise ValueError('Friends List (x)')

            profile_reset = False
            profile_query = self.get_query_with_lowlogic(fbuid=fbuid)
            profile = self.db_s8.share.bonus.find_one(profile_query)

            if profile:
                if profile.get('today') != today:
                    profile_reset = True
                elif friends_set.intersection(set(profile.get('friends', []))):
                    raise ValueError('Friends (x)')

            friends_list = list(friends_set)
            total = len(friends_list)

            if total < 5:
                raise ValueError('Friends List ( F < 5 )')

            balance = float(balance)
            percentage = 10 if total < 10 else 20
            balance_share = (balance * percentage) / 100

            push_pull_notifications.delay(
                action, fbuid, friends_list, SHARE_BONUS
            )

            if profile:
                if not profile_reset:
                    op_atomic = {
                        '$pushAll': {
                            'friends': friends_list
                        }
                    }
                    profile_query.update(today=today)
                else:
                    op_atomic = {
                        '$set': {
                            'today': today,
                            'friends': friends_list
                        }
                    }
                push_social_actions.delay(action, op_atomic, profile_query)

            else:
                profile_query.update(friends=friends_list, today=today)
                push_social_actions.delay(action, profile_query)

            session['balance'] += balance_share
            self.verify_user_config(session)
            session = self.session.data

            try:
                if self.settings.get('track', True):
                    push_social_activity.delay(
                        uid=session.get('uid'),
                        fbuid=fbuid,
                        activity=action,
                        friends=friends_list,
                        value=balance_share,
                        today=today
                    )

            except Exception:
                pass

            return self.get_json_response_and_finish(response={
                'balance': session.get('balance')
            })

        except Exception, e:
            return self.get_except_json_response_and_finish(e)


class SocialShareBonusBalanceHandler(BaseHandler):
    @session_verify
    def post(self, *args, **kwargs):
        try:
            session = self.session.data
            fbuid = session.get('fbuid', None)
            self.validate_fbuid(fbuid)
            date = datetime.datetime.utcnow()
            today = datetime.datetime(date.year, date.month, date.day)

            profile = self.db_s8.share.bonus.find_one({
                'fbuid': fbuid, 'today': today}) or {}

            return self.get_json_response_and_finish(response={
                'friends': profile.get('friends', []),
            })

        except Exception, e:
            return self.get_except_json_response_and_finish(e)


class SocialSendGiftHandler(BaseHandler):
    @session_verify
    def post(self, *args, **kwargs):
        try:
            action = 'send.gift'
            session = self.session.data
            fbuid = session.get('fbuid', None)
            friends = self.get_argument('friends', None)
            self.validate_arguments(friends)
            self.validate_fbuid(fbuid)
            date = datetime.datetime.utcnow()
            today = datetime.datetime(date.year, date.month, date.day)

            if friends.startswith(','):
                friends = friends[1:]
            elif ignore_regex.search(friends):
                raise ValueError('Friends List (!)')

            friends_set = set(friends.split(','))

            if not len(friends_set):
                raise ValueError('Friends List (x)')

            profile_reset = False
            profile_query = self.get_query_with_lowlogic(fbuid=fbuid)
            profile = self.db_s8.send.gift.find_one(profile_query)

            if profile:
                if profile.get('today') != today:
                    profile_reset = True
                elif friends_set.intersection(set(profile.get('friends', []))):
                    raise ValueError('Friends (x)')

            friends_list = list(friends_set)
            friends_len = len(friends_list)
            friends_balance = friends_len * SEND_GIFT_FRIEND

            push_pull_notifications.delay(
                action, fbuid, friends_list, SEND_GIFT_FRIEND)

            if profile:
                op_atomic = {'$inc': {'balance': friends_balance}}
                if not profile_reset:
                    op_atomic['$pushAll'] = {'friends': friends_list}
                    profile_query.update(today=today)
                else:
                    op_atomic['$set'] = {
                        'today': today,
                        'friends': friends_list
                    }
                push_social_actions.delay(action, op_atomic, profile_query)
            else:
                profile_query.update(
                    friends=friends_list, today=today, balance=friends_balance
                )
                push_social_actions.delay(action, profile_query)

            try:
                if self.settings.get('track', True):
                    push_social_activity.delay(
                        uid=session.get('uid'),
                        fbuid=fbuid,
                        activity=action,
                        created=today,
                        friends=friends_list,
                        balance=friends_balance,
                        gift=SEND_GIFT_FRIEND,
                        gift_total=SEND_GIFT_TOTAL,
                        today=today
                    )

            except Exception:
                pass

            return self.get_json_response_and_finish()

        except Exception, e:
            return self.get_except_json_response_and_finish(e)


class SocialSendGiftBalanceHandler(BaseHandler):
    @session_verify
    def post(self, *args, **kwargs):
        try:
            session = self.session.data
            fbuid = session.get('fbuid', None)
            self.validate_fbuid(fbuid)
            date = datetime.datetime.utcnow()
            today = datetime.datetime(date.year, date.month, date.day)

            profile = self.db_s8.send.gift.find_one({
                'fbuid': fbuid, 'today': today}) or {}

            return self.get_json_response_and_finish(response={
                'balance': profile.get('balance', 0),
                'friends': profile.get('friends', []),
                'amount': SEND_GIFT_FRIEND,
                'total': SEND_GIFT_TOTAL,
            })

        except Exception, e:
            return self.get_except_json_response_and_finish(e)


class SocialRequestGiftHandler(BaseHandler):
    @session_verify
    def post(self, *args, **kwargs):
        try:
            action = 'request.gift'
            session = self.session.data
            fbuid = session.get('fbuid', None)
            friends = self.get_argument('friends', None)
            self.validate_arguments(friends)
            self.validate_fbuid(fbuid)
            date = datetime.datetime.utcnow()
            today = datetime.datetime(date.year, date.month, date.day)

            if friends.startswith(','):
                friends = friends[1:]
            elif ignore_regex.search(friends):
                raise ValueError('Friends List (!)')

            friends_set = set(friends.split(','))

            if not len(friends_set):
                raise ValueError('Friends List (x)')

            profile_reset = False
            profile_query = self.get_query_with_lowlogic(fbuid=fbuid)
            profile = self.db_s8.request.gift.find_one(profile_query)

            if profile:
                if profile.get('today') != today:
                    profile_reset = True
                elif friends_set.intersection(set(profile.get('friends', []))):
                    raise ValueError('Friends (x)')

            friends_list = list(friends_set)
            friends_len = len(friends_list)
            friends_balance = friends_len * REQUEST_GIFT_FRIEND

            push_pull_notifications.delay(
                action, fbuid, friends_list, REQUEST_GIFT_FRIEND)

            if profile:
                op_atomic = {'$inc': {'balance': friends_balance}}
                if not profile_reset:
                    op_atomic['$pushAll'] = {'friends': friends_list}
                    profile_query.update(today=today)
                else:
                    op_atomic['$set'] = {
                        'today': today,
                        'friends': friends_list
                    }
                push_social_actions.delay(action, op_atomic, profile_query)
            else:
                profile_query.update(
                    friends=friends_list, today=today, balance=friends_balance
                )
                push_social_actions.delay(action, profile_query)

            try:
                if self.settings.get('track', True):
                    push_social_activity.delay(
                        uid=session.get('uid'),
                        fbuid=fbuid,
                        activity=action,
                        created=today,
                        friends=friends_list,
                        balance=friends_balance,
                        gift=REQUEST_GIFT_FRIEND,
                        gift_total=REQUEST_GIFT_TOTAL,
                        today=today
                    )

            except Exception:
                pass

            return self.get_json_response_and_finish()

        except Exception, e:
            return self.get_except_json_response_and_finish(e)


class SocialRequestGiftBalanceHandler(BaseHandler):
    @session_verify
    def post(self, *args, **kwargs):
        try:
            session = self.session.data
            fbuid = session.get('fbuid', None)
            self.validate_fbuid(fbuid)
            date = datetime.datetime.utcnow()
            today = datetime.datetime(date.year, date.month, date.day)

            profile = self.db_s8.request.gift.find_one({
                'fbuid': fbuid, 'today': today}) or {}

            return self.get_json_response_and_finish(response={
                'balance': profile.get('balance', 0),
                'friends': profile.get('friends', []),
                'amount': REQUEST_GIFT_FRIEND,
                'total': REQUEST_GIFT_TOTAL,
            })

        except Exception, e:
            return self.get_except_json_response_and_finish(e)


class SocialInviteHandler(BaseHandler):
    @session_verify
    def post(self, *args, **kwargs):
        try:
            action = 'invite'
            session = self.session.data
            fbuid = session.get('fbuid', None)
            friends = self.get_argument('friends', None)
            self.validate_arguments(friends)
            self.validate_fbuid(fbuid)
            start_date, end_date = week_range()
            date = datetime.datetime.utcnow()
            today = datetime.datetime(date.year, date.month, date.day)

            if friends.startswith(','):
                friends = friends[1:]
            elif ignore_regex.search(friends):
                raise ValueError('Friends List (!)')

            friends_set = set(friends.split(','))

            if not len(friends_set):
                raise ValueError('Friends List (x)')

            profile_reset = False
            profile_query = self.get_query_with_lowlogic(fbuid=fbuid)
            profile = self.db_s8.invite.find_one(profile_query)

            if profile:
                if today > end_date or profile.get('today') != today:
                    profile_reset = True
                elif friends_set.intersection(set(profile.get('friends', []))):
                    raise ValueError('Friends (x)')
                balance = profile.get('balance')
            else:
                balance = 0

            friends_list = list(friends_set)
            friends_len = len(friends_list)
            friends_balance = friends_len * INVITE_FRIEND

            push_pull_notifications.delay(
                action, fbuid, friends_list, INVITE_FRIEND
            )

            if profile:
                op_atomic = {}
                if not profile_reset:
                    if balance < INVITE_TOTAL:
                        reward_diff = INVITE_TOTAL - balance
                        op_atomic['$set'] = {'balance': min(
                            INVITE_TOTAL, (
                                friends_balance + reward_diff
                            )
                        )}
                        reward = min(reward_diff, friends_balance)
                    else:
                        reward = 0
                    op_atomic['$pushAll'] = {'friends': friends_list}
                    profile_query.update(today=today)
                else:
                    reward = min(friends_balance, INVITE_TOTAL)
                    op_atomic['$set'] = {
                        'today': today,
                        'friends': friends_list,
                        'balance': reward,
                        'start_date': start_date,
                        'end_date': end_date,
                    }
                push_social_actions.delay(action, op_atomic, profile_query)
            else:
                reward = min(friends_balance, INVITE_TOTAL)
                profile_query.update(
                    today=today,
                    friends=friends_list,
                    balance=reward,
                    start_date=start_date,
                    end_date=end_date,
                )
                push_social_actions.delay(action, profile_query)

            try:
                if self.settings.get('track', True):
                    push_social_activity.delay(
                        uid=session.get('uid'),
                        fbuid=fbuid,
                        activity=action,
                        friends=friends_list,
                        balance=reward,
                        gift=INVITE_FRIEND,
                        gift_total=INVITE_TOTAL,
                        start_date=start_date,
                        end_date=end_date,
                        today=today
                    )

            except Exception:
                pass

            balance = session.get('balance') + reward
            session.update(balance=balance)
            self.verify_user_config(session, not_cache=True)

            return self.get_json_response_and_finish(response={
                'balance': balance
            })

        except Exception, e:
            return self.get_except_json_response_and_finish(e)


class SocialInviteBalanceHandler(BaseHandler):
    @session_verify
    def post(self, *args, **kwargs):
        try:
            session = self.session.data
            fbuid = session.get('fbuid', None)
            self.validate_fbuid(fbuid)
            date = datetime.datetime.utcnow()
            today = datetime.datetime(date.year, date.month, date.day)

            profile = self.db_s8.invite.find_one({
                'fbuid': fbuid, 'today': today
            }) or {}

            return self.get_json_response_and_finish(response={
                'balance': profile.get('balance', 0),
                'friends': profile.get('friends', []),
                'amount': INVITE_FRIEND,
                'total': INVITE_TOTAL,
            })

        except Exception, e:
            return self.get_except_json_response_and_finish(e)

################################################################################


handlers_list = [
    (r'/do/share/bonus/?', SocialShareBonusHandler),
    (r'/do/share/bonus/balance/?', SocialShareBonusBalanceHandler),
    (r'/do/send/gift/?', SocialSendGiftHandler),
    (r'/do/send/gift/balance/?', SocialSendGiftBalanceHandler),
    (r'/do/request/gift/?', SocialRequestGiftHandler),
    (r'/do/request/gift/balance/?', SocialRequestGiftBalanceHandler),
    (r'/do/invite/?', SocialInviteHandler),
    (r'/do/invite/balance/?', SocialInviteBalanceHandler),
]
