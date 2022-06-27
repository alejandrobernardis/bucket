#!/usr/bin/env python
import time
from datetime import datetime
from decimal import Decimal
from typing import Union

import msgpack
from aioredis import Redis
from bson import ObjectId
from core import constants as ct

__all__ = [
    'TTL_DEFAULT',
    'decode_as_datetime',
    'decode_as_str',
    'as_datetime',
    'decode_object',
    'encode_object',
    'Cache',
]

TTL_DEFAULT: int = ct.MINUTE * 5
dt_str: str = '%Y%m%dT%H:%M:%S.%f'
dt_key: str = '__datetime__'
oi_key: str = '__objectid__'
as_str: str = 'as_str'


def decode_as_datetime(obj):
    """
    Retorna un objeto datetime
    :param obj: referencia
    :return: datetime
    """
    if as_str in obj:
        obj = obj[as_str]
    return datetime.strptime(obj, dt_str)


def decode_as_str(obj):
    """
    Retorna un objeto string
    :param obj: referencia
    :return: string
    """
    if as_str in obj:
        obj = obj[as_str]
    return obj


def decode_object(obj):
    """
    Msgpack Decoder
    :param obj: referencia
    :return: object
    """
    if dt_key in obj:
        obj = decode_as_datetime(obj)
    elif oi_key in obj:
        obj = ObjectId(obj[as_str])
    return obj


def encode_object(obj):
    """
    Msgpack Encoder
    :param obj: referencia
    :return: object
    """
    if isinstance(obj, datetime):
        return {dt_key: True, as_str: obj.strftime(dt_str)}
    if isinstance(obj, ObjectId):
        return {oi_key: True, as_str: str(obj)}
    if isinstance(obj, Decimal):
        return float(Decimal)
    return obj


as_datetime = decode_as_datetime


class Cache:

    def __init__(self, cli: Redis):
        self.cli: Redis = cli

    async def read(self, req: str, hook=decode_as_str, **kwargs) -> dict:
        """
        Retorna el requerimiento almacenado en cache.

        :param req: identificador del requerimiento
        :param hook: función para el casteo de objetos
        :param kwargs: opcional
        :return: dict
        """
        ret: dict = dict()
        cache = await self.cli.get(req)
        if cache:
            ret = msgpack.unpackb(cache, object_hook=hook)
        return ret

    async def create(
            self,
            req: str,
            data: Union[list, dict],
            ttl: int = TTL_DEFAULT,
            **kwargs
    ) -> dict:
        """
        Almacena en cache el requerimiento.

        :param req: identificador del requerimiento
        :param data: datos del requerimiento
        :param ttl: tiempo de expiración expresado en segundos
        :param kwargs: opcional
        :return: dict
        """
        if not data:
            data = {}
        if 'app' in kwargs:
            ttl = kwargs['app'].cfg.service.sess_time
        msg = msgpack.packb(data, default=encode_object, use_bin_type=True)
        ret = await self.cli.set(req, msg, ex=int(ttl))
        return ret or {}

    async def delete(self, req: str, **kwargs) -> None:
        """
        Elimina el requerimiento almacenado en cache.

        :param req: identificador del requerimiento
        :param kwargs: opcional
        :return: None
        """
        await self.cli.delete(req)

    async def has(self, req: str, **kwargs) -> bool:
        """
        Retorna TRUE en caso de que el requerimiento se encuentre en cache.

        :param req: identificador del requerimiento
        :param kwargs: opcional
        :return: bool
        """
        try:
            ret = await self.cli.exists(req)
            return bool(ret)
        except Exception:
            return False


