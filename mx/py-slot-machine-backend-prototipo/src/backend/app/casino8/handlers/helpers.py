#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 20/09/2013 09:33

import json
import datetime
from casino8.common.utils import str_complex_type
from casino8.handlers.base import BaseHandler


class AdminDebugHandler(BaseHandler):
    def get(self, *args, **kwargs):
        data = {}
        action = args[0]
        self.set_header_for_json()

        if action == 'game':
            self.session.update(game=2)

        elif action == 'reset':
            self.session.update(
                balance=2000000,
                level=1,
                points=0,
            )
            self.verify_user_config()

        elif action == 'reset-cero':
            self.session.update(
                balance=200,
                level=1,
                points=0,
            )
            self.verify_user_config()

        elif action == 'balance':
            balance = self.get_argument('balance', 2000000)
            self.session.update(balance=float(balance))
            self.verify_user_config()

        elif action == 'level':
            self.session.update(points=1000000)
            self.verify_user_config()

        elif action == 'bonus':
            self.session.update(
                gift_time_begin='2013-09-09T02:02:52.239000',
                gift_time_finish='2013-09-09T05:02:52.239000'
            )
            self.verify_user_config()

        elif action == 'bonus-cero':
            self.session.update(
                gift_total=0,
                gift_award=50,
                gift_available=True,
                gift_time_begin='2013-09-09T02:02:52.239000',
                gift_time_finish='2013-09-09T05:02:52.239000'
            )
            self.verify_user_config()

        elif action == 'bonus-plus':
            self.session.update(
                gift_award=50,
                gift_available=True,
                gift_time_begin='2013-09-09T02:02:52.239000',
                gift_time_finish='2013-09-09T05:02:52.239000'
            )
            self.verify_user_config()

        elif action == 'bonus-roulette':
            self.session.update(
                gift_total=2,
                gift_award=1,
                gift_available=True,
                gift_time_begin='2013-09-09T02:02:52.239000',
                gift_time_finish='2013-09-09T05:02:52.239000'
            )
            self.verify_user_config()

        elif action == 'bonus-roulette-2m':
            time_now = datetime.datetime.utcnow()
            time_begin = time_now - datetime.timedelta(hours=2, minutes=58)
            time_finish = time_now + datetime.timedelta(minutes=2)
            self.session.update(
                gift_total=2,
                gift_award=50,
                gift_available=False,
                gift_time_begin=str_complex_type(time_begin),
                gift_time_finish=str_complex_type(time_finish)
            )
            self.verify_user_config()

        elif action == 'sid-cero':
            self.session.update(sid='c4d28871-0000-0000-0000-fdfe22309933')

        elif action == 'config':
            data = self.session.data['config']
            self.write(json.dumps(data, indent=4, default=str_complex_type))
            return self.finish()

        elif action == 'session':
            data = self.session.data

        elif action == 'verify':
            self.verify_user_config()

        else:
            data = {
                'action': action,
                'help': {
                    'game':
                        u'Activa un juego en la sesión con un factor de 2',
                    'reset':
                        u'Reinicia la máquina, con un balance de 2,000,000',
                    'reset-cero':
                        u'Reinicia la máquina, con un balance de 200',
                    'balance':
                        u'Altera el balance de la máquina <?balance=(int)>',
                    'level':
                        u'Libera todas las máquinas',
                    'bonus':
                        u'Activa un bono',
                    'bonus-cero':
                        u'Reinicia el bono a cero',
                    'bonus-plus':
                        u'Activa un bono para ser cobrado',
                    'bonus-roulette':
                        u'Activa la ruleta',
                    'sid-cero':
                        u'Cambai el ID de sesión',
                    'config':
                        u'Imprime los datos  configuración actual',
                    'session':
                        u'Imprime los datos la sesión actual',
                },
            }

            self.write(json.dumps(data, indent=4, sort_keys=True))
            return self.finish()

        if not data:
            data = self.session.data
        if 'config' in data:
            del data['config']
        self.write(json.dumps(
            data, indent=4, default=str_complex_type, sort_keys=True))
        self.finish()


class AdminClientHandler(BaseHandler):
    def get(self):
        self.render('client.html')


handlers_list = [
    (r'/a/debug/?(.+)?', AdminDebugHandler),
    (r'/a/client', AdminClientHandler),
]

