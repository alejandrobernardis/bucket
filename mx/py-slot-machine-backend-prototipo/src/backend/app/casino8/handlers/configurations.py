#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 24/08/2013 21:06


import os
import re
import json
import datetime
import settings
from math import floor
from casino8.common.utils import datetime_parser
from casino8.machines.configurations import DEVICE_LEVELS, DEFAULT_BETS_ASC

re_gift_time = re.compile(r'\d{1,2}:\d{2}:\d{2}(\.\d+)?')

if settings.DEBUG:
    S3_URL = 'http://dev.casino-8.net/static/{}'
else:
    S3_URL = 'http://s3-us-west-2.amazonaws.com/media-casino-8-net/static/{}'


class DeviceConfiguration(object):
    _gift_coef = 3

    _commands = [
        'SPIN',
        'SPIN_GAME',
        'SPIN_GAME_BONUS',
        'GET_USER_CONFIG',
        'GET_USER_SYNC_TOKEN',
        'GET_ADD_USER_SYNC'
    ]

    _podium = (
        'http://app.casino-8.net/static/data/podium/1.json',
    )

    def __init__(self, device, uid, sid, level=1, **kwargs):
        if settings.DEBUG:
            file_name = os.path.join(settings.STATIC_PATH, 'data/machines.json')
            with open(file_name, 'r') as config_file:
                _tmp = json.load(config_file, 'utf-8')
                self._version = _tmp.get('version', -1)
                self._sale_status = _tmp.get('sales', False)
                self._snow = _tmp.get('snow', False)
                self._machine_data = _tmp.get('machines', [])

        else:
            self._version = 1.11
            self._sale_status = False
            self._snow = False
            self._machine_data = [{
                'id': 100,
                'name': 'Banda Ancha',
                'version': 1.4,
                'enabled': True,
                'lines': 10,
                'required_level': 1,
                'assets': S3_URL + '/machines/{}/100.zip'
            }, {
                'id': 101,
                'name': 'Fiesta Animal',
                'version': 1.4,
                'enabled': False,
                'lines': 15,
                'required_level': 2,
                'assets': S3_URL + '/machines/{}/101.zip'
            }, {
                'id': 102,
                'name': 'La Taberna del Monstruo',
                'version': 1.4,
                'enabled': False,
                'lines': 20,
                'required_level': 4,
                'assets': S3_URL + '/machines/{}/102.zip'
            }, {
                'id': 103,
                'name': 'Rockeros',
                'version': 1.4,
                'enabled': False,
                'lines': 20,
                'required_level': 6,
                'assets': S3_URL + '/machines/{}/103.zip'
            }, {
                'id': 104,
                'name': u'Ataque Alienígena',
                'version': 1.4,
                'enabled': False,
                'lines': 25,
                'required_level': 8,
                'assets': S3_URL + '/machines/{}/104.zip'
            }, {
                'id': 105,
                'name': 'Lucha Machine',
                'version': 1.4,
                'enabled': False,
                'lines': 25,
                'required_level': 10,
                'assets': S3_URL + '/machines/{}/105.zip'
            }, {
                'id': 106,
                'name': 'Vikingos',
                'version': 1.4,
                'enabled': False,
                'lines': 30,
                'required_level': 12,
                'assets': S3_URL + '/machines/{}/106.zip'
            }, {
                'id': 107,
                'name': 'Sr. Ardilla',
                'version': 1.4,
                'enabled': False,
                'lines': 30,
                'required_level': 14,
                'assets': S3_URL + '/machines/{}/107.zip'
            }, {
                'id': 109,
                'name': 'Zombies',
                'version': 1.4,
                'enabled': False,
                'lines': 25,
                'required_level': 16,
                'assets': S3_URL + '/machines/{}/109.zip'
            }, {
                'id': 108,
                'name': 'Navi Punk',
                'version': 1.4,
                'enabled': False,
                'lines': 30,
                'required_level': 18,
                'assets': S3_URL + '/machines/{}/108.zip'
            }, {
                'id': 110,
                'name': 'Mariachis',
                'version': 1.4,
                'enabled': False,
                'lines': 30,
                'required_level': 20,
                'assets': S3_URL + '/machines/{}/110.zip'
            }, {
                'id': 111,
                'name': u'Mundo Mágico',
                'version': 1.4,
                'enabled': False,
                'lines': 25,
                'required_level': 22,
                'assets': S3_URL + '/machines/{}/111.zip'
            }]

        self._urls = {
            'version': S3_URL + '/data/version.json',
            'coins': S3_URL + '/data/get_coins.json',
            'apps': S3_URL + '/data/get_apps.json'
        }

        self._profile = {
            'internal_machine': True,
            'gifts': {
                'max': 3,
                'total': 0,
                'time': '03:00:00'
            },
            'sales': {
                'status': False
            },
            'level': {
                'id': 1,
                'value': 0,
                'value_next': 0,
                'value_prev': 0
            },
            'bet': None,
            'balance': 0,
            'uid': None,
            'sid': None,
            'fbuid': None,
            'device': None,
            'lang': None
        }

        self.uid = uid
        self.sid = sid
        self.fbuid = kwargs.get('fbuid', 0)
        self.level_id = level
        self.level_value = int(kwargs.get('points', 0))
        self.balance = kwargs.get('balance', 200)
        self.device = device
        lang = kwargs.get('lang', settings.LANGUAGES_DEFAULT)
        self.lang = settings.LANGUAGES_DEFAULT \
            if lang not in settings.LANGUAGES else lang
        self.bet = None
        self.level_value_next = 0
        self.sale_status = self._sale_status
        self.gift_time = '00:00:00'
        self._total_machines = 0
        self._assets = None
        time_begin = datetime.datetime.utcnow()
        self._gift_time_begin = \
            datetime_parser(kwargs.get('gift_time_begin', time_begin))
        time_finish = \
            self._gift_time_begin + datetime.timedelta(hours=self._gift_coef)
        self._gift_time_finish = \
            datetime_parser(kwargs.get('gift_time_finish', time_finish))
        self.gift_total = kwargs.get('gift_total', 0)
        self._machines_cache = self._get_machines()
        self.set_urls()
        self.set_level_by_points()
        self.set_points_next_level()
        self.set_machines_by_level()
        self.set_bets_by_level()
        self.set_bonus_time()
        self.set_machine_assets()

    def _get_machines(self):
        _total_machines = 0
        for item in self._machine_data:
            item['assets'] = item.get('assets').format(self.lang, self.device)
            item_level = item.get('required_level')
            device_level = DEVICE_LEVELS[item_level-1]
            if device_level[0] == item_level and item_level <= self.level_id:
                item['enabled'] = True
                _total_machines += 1
        self._total_machines = _total_machines
        return self._machine_data

    def activate_machine(self, *args):
        self._status_machine(True, *args)

    def deactivate_machine(self, *args):
        self._status_machine(False, *args)

    def _status_machine(self, status, *args):
        for machine in self._machines_cache:
            if machine.get('id') in args:
                machine['enabled'] = status

    def set_urls(self):
        for k, v in self._urls.items():
            self._urls[k] = v.format(self.lang)

    def set_machine_assets(self, device=None, lang=None):
        assets = S3_URL + '/machines/{}/assets.zip'
        self._assets = assets.format(
            lang or self.lang, device or self.device
        )

    def set_machines_by_level(self, level=None):
        if not level:
            level = self.level_id
        _total_machines = 0
        for machine in self._machines_cache:
            machine_level = machine.get('required_level')
            device_level = DEVICE_LEVELS[machine_level-1]
            if device_level[0] == machine_level and machine_level <= level:
                machine['enabled'] = True
                _total_machines += 1
        self._total_machines = _total_machines

    def set_bets_by_level(self, level=None):
        if not level:
            level = self.level_id
        index = 5
        device_level = DEVICE_LEVELS[level-1]
        if device_level[0] == level:
            max_bet = device_level[3]
            low, high = 0, len(DEFAULT_BETS_ASC)-1
            while low <= high:
                mid = int(floor((low+high)/2))
                value = DEFAULT_BETS_ASC[mid]
                if value < max_bet:
                    low = mid + 1
                elif value > max_bet:
                    high = mid - 1
                else:
                    index = mid + 1
                    break
        self.bet = DEFAULT_BETS_ASC[0:index]

    def set_points_next_level(self, level=None):
        if not level:
            level = self.level_id
        device_total = len(DEVICE_LEVELS)
        if level > device_total:
            level = device_total
        elif level < 0:
            level = 1
        device_level = DEVICE_LEVELS[level-1]
        device_next_level = level
        if device_level[0] == level and device_next_level <= device_total:
            device_level = DEVICE_LEVELS[device_next_level]
        self.level_value_prev = 0 if level == 1 else DEVICE_LEVELS[level-1][1]
        self.level_value_next = device_level[1]

    def set_level_by_points(self, points=None):
        if not points:
            points = self.level_value or 0
        if points == 0 and points < DEVICE_LEVELS[1][1]:
            self.level_id = 1
            self.level_value = points
            return
        elif DEVICE_LEVELS[self.level_id-1][1] \
                < points < DEVICE_LEVELS[self.level_id+1][1]:
            self.level_value = points
            return
        index = 0
        low, high = 0, len(DEVICE_LEVELS)-1
        while low <= high:
            mid = int(floor((low+high)/2))
            value = DEVICE_LEVELS[mid][1]
            if value < points:
                low = mid + 1
                index = mid
            elif value > points:
                high = mid - 1
                index = mid
            else:
                index = mid
                break
        if points < DEVICE_LEVELS[index][1]:
            index -= 1
        self.level_id = DEVICE_LEVELS[index][0]

    def set_bonus_time(self, time_finish=None):
        if not time_finish:
            time_finish = self._gift_time_finish
        time_now = datetime.datetime.utcnow()
        time_finish = datetime_parser(time_finish)
        value = re_gift_time.match(str(time_finish - time_now))
        self.gift_time = '00:00:00' \
            if not value else str(value.group()).split('.')[0]

    @property
    def gift_total(self):
        return self._profile['gifts']['total']

    @gift_total.setter
    def gift_total(self, value):
        self._profile['gifts']['total'] = value

    @property
    def gift_time(self):
        return self._profile['gifts']['time']

    @gift_time.setter
    def gift_time(self, value):
        self._profile['gifts']['time'] = value

    @property
    def sale_status(self):
        return self._profile['sales']['status']

    @sale_status.setter
    def sale_status(self, value):
        self._profile['sales']['status'] = value

    @property
    def level_id(self):
        return self._profile['level']['id']

    @level_id.setter
    def level_id(self, value):
        self._profile['level']['id'] = value

    @property
    def level_value(self):
        return self._profile['level']['value']

    @level_value.setter
    def level_value(self, value):
        self._profile['level']['value'] = value

    @property
    def level_value_next(self):
        return self._profile['level']['value_next']

    @level_value_next.setter
    def level_value_next(self, value):
        self._profile['level']['value_next'] = value

    @property
    def level_value_prev(self):
        return self._profile['level']['value_prev']

    @level_value_prev.setter
    def level_value_prev(self, value):
        self._profile['level']['value_prev'] = value

    @property
    def balance(self):
        return self._profile['balance']

    @balance.setter
    def balance(self, value):
        self._profile['balance'] = value

    @property
    def bet(self):
        return self._profile['bet']

    @bet.setter
    def bet(self, value):
        self._profile['bet'] = value

    @property
    def sid(self):
        return self._profile['sid']

    @sid.setter
    def sid(self, value):
        self._profile['sid'] = value

    @property
    def uid(self):
        return self._profile['uid']

    @uid.setter
    def uid(self, value):
        self._profile['uid'] = value

    @property
    def fbuid(self):
        return self._profile['fbuid']

    @fbuid.setter
    def fbuid(self, value):
        self._profile['fbuid'] = value

    @property
    def device(self):
        return self._profile['device']

    @device.setter
    def device(self, value):
        self._profile['device'] = str(value).lower()

    @property
    def lang(self):
        return self._profile['lang']

    @lang.setter
    def lang(self, value):
        self._profile['lang'] = str(value).lower()

    def todict(self):
        return dict(
            snow=self._snow,
            profile=self._profile,
            assets=self._assets,
            urls=self._urls,
            machines=self._machines_cache,
            commands=self._commands,
            podium=self._podium,
            version=self._version
        )

    def update_session(self):
        return dict(
            level=self.level_id,
            points_next_level=self.level_value_next,
            total_machines=self._total_machines
        )
