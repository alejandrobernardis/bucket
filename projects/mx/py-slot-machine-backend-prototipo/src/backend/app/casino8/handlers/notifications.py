#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 03/09/2013 08:24

from casino8.handlers.base import BaseHandler
from casino8.security.sessions import session_verify


class NotificationsListHandler(BaseHandler):
    @session_verify
    def post(self, *args, **kwargs):
        try:
            session = self.session.data
            fbuid = session.get('fbuid', None)
            self.validate_fbuid(fbuid)
            query = self.get_query_with_lowlogic(fbuid=fbuid)
            fields = {'fbfriend': 1, 'value': 1}
            total = 0
            result = dict()
            for item in ('share.bonus', 'send.gift', 'request.gift',):
                cursor = self.db_n8[item]\
                    .find(query, fields).limit(10).sort('created')
                if cursor:
                    key = item.replace('.', '_')
                    result[key] = [document for document in cursor]
                    total += len(result[key])
            return self.get_json_response_and_finish(response={
                'total': total,
                'notifications': result
            })
        except Exception, e:
            return self.get_except_json_response_and_finish(e)


handlers_list = [
    (r'/do/notifications/list/?', NotificationsListHandler),
]
