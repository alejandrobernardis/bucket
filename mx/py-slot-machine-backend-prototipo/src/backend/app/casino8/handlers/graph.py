#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 02/Oct/2013 14:27

from casino8.handlers.base import BaseHandler, ignore_regex
from casino8.security.sessions import session_verify


class GraphRelationshipsListHandler(BaseHandler):
    @session_verify
    def post(self, *args, **kwargs):
        try:
            session = self.session.data
            fbuid = session.get('fbuid', None)
            friends = self.get_argument('friends', None)
            self.validate_arguments(fbuid)

            if not friends:
                return self.get_json_response_and_finish(response=[])

            friends_set = set(friends.split(','))

            if not len(friends_set):
                raise ValueError('Friends List (x)')

            elif ignore_regex.search(friends):
                raise ValueError('Friends List (!)')

            friends_set.add(fbuid)
            query = self.get_query_with_lowlogic(_id={'$in': list(friends_set)})
            values = {'level': 1, 'points': 1, 'balance': 1}

            cursor = self.db.profiles.find(query, values) \
                .sort([('level', -1), ('points', -1)]) \
                .limit(100) \
                .skip(0)

            result = [document for document in cursor]
            return self.get_json_response_and_finish(response=result)

        except Exception, e:
            return self.get_except_json_response_and_finish(e)


handlers_list = [
    (r'/do/graph/relationship/list/?', GraphRelationshipsListHandler)
]