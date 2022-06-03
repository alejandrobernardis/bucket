#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 26/09/2013 22:44

from celery_tasks import delete_pull_notifications, push_pull_notifications_set
from bson.objectid import ObjectId
from casino8.handlers.base import BaseHandler
from casino8.security.sessions import session_verify


class SocialBulkRedeemHandler(BaseHandler):
    @session_verify
    def post(self, *args, **kwargs):
        try:
            session = self.session.data
            fbuid = session.get('fbuid', None)
            share_bonus = self.get_argument('share_bonus', None)
            send_gift = self.get_argument('send_gift', None)
            request_gift = self.get_argument('request_gift', None)
            share_bonus_reject = self.get_argument('share_bonus_reject', None)
            send_gift_reject = self.get_argument('send_gift_reject', None)
            request_gift_reject = self.get_argument('request_gift_reject', None)
            self.validate_fbuid(fbuid)

            redeems = {
                'share.bonus': share_bonus,
                'send.gift': send_gift,
                'request.gift': request_gift
            }

            for key, value in redeems.items():

                if not value:
                    continue

                elif value.startswith(','):
                    value = value[1:]

                if value != '':
                    redeems_set = set(value.split(','))
                    redeems_list = [ObjectId(_id) for _id in redeems_set]

                    query = self.get_query_with_lowlogic(
                        _id={'$in': redeems_list}, fbuid=fbuid
                    )

                    coll = self.db_n8[key]

                    records = coll.find(query, {
                        'fbuid': 1, 'fbfriend': 1, 'value': 1
                    })

                    if not records:
                        raise ValueError('Redeems (x)')

                    elif len(redeems_list) != records.count():
                        raise ValueError('Redeems Count (~)')

                    elif key != 'request.gift':
                        redeems_balance = \
                            [int(record.get('value')) for record in records]
                        session['balance'] += sum(redeems_balance)

                    elif key == 'request.gift':
                        notify = [{
                            'fbuid': record.get('fbfriend'),
                            'fbfriend': record.get('fbuid'),
                            'value': record.get('value')
                        } for record in records]
                        push_pull_notifications_set.delay('send.gift', notify)

                    else:
                        raise ValueError('Key (x)')

                    coll.update(query, {
                        '$set': {
                            'enabled': False
                        }
                    }, multi=True, w=0, j=False)

                    query['enabled'] = False
                    delete_pull_notifications.delay(key, query)

            redeems = {
                'share.bonus': share_bonus_reject,
                'send.gift': send_gift_reject,
                'request.gift': request_gift_reject
            }

            for key, value in redeems.items():
                if value.startswith(','):
                    value = value[1:]

                if value != '':
                    redeems_set = set(value.split(','))
                    redeems_list = [ObjectId(_id) for _id in redeems_set]
                    query = {'_id': {'$in': redeems_list}, 'fbuid': fbuid}

                    coll = self.db_n8[key]
                    coll.update(query, {
                        '$set': {
                            'enabled': False
                        }
                    }, multi=True, w=0, j=False)

                    query['enabled'] = False
                    delete_pull_notifications.delay(key, query)

            config = self.verify_user_config(session, not_cache=False)
            return self.get_json_response_and_finish(response=config)

        except Exception, e:
            return self.get_except_json_response_and_finish(e)


handlers_list = [
    (r'/do/redeem/?', SocialBulkRedeemHandler),
]