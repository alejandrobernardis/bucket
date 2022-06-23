#!/usr/bin/env python

from http import HTTPStatus

from aiohttp import web, hdrs
from aiohttp.web import RouteTableDef
from core.config import mask_password

from service.api.health.lowlevel import \
    client_counters_check, \
    service_check, \
    uptime_check, \
    WORKING

__all__ = [
    'api',
    'get_config',
    'get_counters',
    'get_health',
    'get_ping',
    'get_uptime'
]

api: RouteTableDef = RouteTableDef()


@api.get('/health')
async def get_health(req: web.Request) -> web.Response:
    """
    Retorna el estado de salud del microservice, validando todos los componentes
    que integran al mismo.

    En caso de que algún componente este fallando, se verá reflejado el menseja
    de error del mismo y el código de estatus cambiará a 503. En caso contrario,
    se verá la palabra WORKING en cada componente y el código de estatus tendrá
    el valor de 200.

    >>> {
    >>>   "mongodb": "WORKING",
    >>>   "redis": "WORKING",
    >>>   "...": "..."
    >>> }

    :param req: Información del request
    :return: json
    """
    ret: dict = await service_check(req)
    sts: int = HTTPStatus.SERVICE_UNAVAILABLE \
        if [x for x in ret.values() if x != WORKING] else HTTPStatus.OK
    hdr: dict = {}
    if req.method != hdrs.METH_HEAD and sts == HTTPStatus.OK:
        hdr = {'x-health-response': WORKING}
    return web.json_response(ret, status=sts, headers=hdr)


@api.get('/uptime', allow_head=False)
async def get_uptime(req: web.Request) -> web.Response:
    """
    Retorna la información referente al tiempo trasncurrido desde la fecha
    y hora de inicio de microservice.

    >>> {
    >>>   "uptime": {
    >>>     "days": 0,
    >>>     "hours": 0,
    >>>     "minutes": 1,
    >>>     "seconds": 32.06352400779724
    >>>   },
    >>>   "epoch": {
    >>>     "start": 1618334298.868699,
    >>>     "check": 1618334390.932223,
    >>>     "uptime": 92.06352400779724
    >>>   }
    >>> }

    :param req: información del request
    :return: json
    """
    return web.json_response(uptime_check(req))


@api.get('/counters', allow_head=False)
async def get_counters(req: web.Request) -> web.Response:
    """
    Retorna la información referente a los contadores establecidos.

    >>> {
    >>>   "main": {
    >>>     "req": 2,
    >>>     "err": 0
    >>>   },
    >>>   "others": {
    >>>     "req": 0,
    >>>     "err": 0,
    >>>     "log": 0
    >>>   }
    >>> }

    :param req: información del request
    :return: json
    """
    return web.json_response(client_counters_check(req))


@api.get('/ping')
async def get_ping(req: web.Request) -> web.Response:
    """
    Retorna el mensaje "pong" como respuesta.

    >>> {"message": "pong"}

    :param req: información del request
    :return: json
    """
    hdr = {}
    if req.method == hdrs.METH_HEAD:
        hdr = {'x-ping-response': 'pong'}
    return web.json_response({'message': 'pong'}, headers=hdr)


@api.get('/config', allow_head=False)
async def get_config(req: web.Request) -> web.Response:
    """
    Retorna la configuración del microservice. Este endpoint Sólo podrá
    ser accedido en la medida que el servidor se encuentre en modo DEBUG.

    >>> {
    >>>   "root": ".../src/service",
    >>>   "initiated": 1618333093.8524368,
    >>>   "mariadb": {
    >>>     "host": "localhost",
    >>>     "port": 3306,
    >>>     "database": "database",
    >>>     "username": "username",
    >>>     "password": "******",
    >>>     "arguments": null,
    >>>     "try_policy": 3,
    >>>     "try_sleep": 0.5
    >>>   },
    >>>   "mongodb": ...
    >>> }

    :param req: información del request
    :return: json
    """
    cfg = req.app.cfg
    if cfg.service.debug:
        ret: dict = cfg.to_python()
        ret['root'] = str(cfg.root)
        return web.json_response(mask_password(ret))
    raise web.HTTPNotFound()

