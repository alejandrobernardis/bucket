#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-20
# --

import logging
from functools import wraps
from http import HTTPStatus
from typing import Union, Any, Optional

from aetcd3 import Etcd3Client
from aiohttp import web
from aioredis.connection import ConnectionPool
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database

from core.services import etcd, mariadb, mongodb, redis
from core.web import Application

__all__ = ['APP_TYPE', 'log', 'find_app', 'pass_app', 'find_nosql',
           'pass_nosql', 'find_cache', 'pass_cache', 'find_sql', 'pass_sql',
           'find_etcd', 'pass_etcd', 'APIError', 'find_status_code',
           'find_message', 'pass_datalayer', 'pass_cnx']


# Constants

APP_TYPE = Union[Application, web.Application, web.Request]
"""Objetos considerados como Aplicación"""

log = logging.getLogger('low-level')


# Helpers

def find_app(obj: APP_TYPE) -> Application:
    """
    Busca el objeto Application dentro del argumento obj.

    :param obj: objeto a evaluar
    :return: Application
    """

    if isinstance(obj, web.Request):
        return obj.app

    if not isinstance(obj, Application):
        log.error(f'Object must be an Application: {obj}')
        raise web.HTTPInternalServerError()

    return obj


def find_sql(obj: APP_TYPE, throw: bool = True) -> Any:
    """
    Busca en el objeto Applications el cliente de MARIADB y devuelve
    la base de datos por default.

    :param obj: objeto a evaluar.
    :param throw: define el tipo de respuesta.
    :return: Database
    """

    app = find_app(obj)

    if mariadb.NAME not in app.cli and not app.cli[mariadb.NAME]:
        log.error(f'Client "{mariadb.NAME}" not found')
        if throw is True:
            raise web.HTTPInternalServerError()
        return None

    return app.cli[mariadb.NAME]


def find_nosql(
        obj: APP_TYPE,
        throw: bool = True,
        client: bool = False
) -> Union[Database, AsyncIOMotorClient]:
    """
    Busca en el objeto Applications el cliente de MONGODB y devuelve
    la base de datos por default.

    :param obj: objeto a evaluar.
    :param throw: define el tipo de respuesta.
    :param client: define el tipo de retorno.
    :return: Database
    """

    app = find_app(obj)

    if mongodb.NAME not in app.cli \
            and not isinstance(app.cli[mongodb.NAME], AsyncIOMotorClient):
        log.error(f'Client "{mongodb.NAME}" not found')
        if throw is True:
            raise web.HTTPInternalServerError()
        return None

    cnx = app.cli[mongodb.NAME]

    if client is False:
        return cnx[app.cfg[mongodb.NAME].database]

    return cnx


def find_cache(obj: APP_TYPE, throw: bool = True) -> Optional[ConnectionPool]:
    """
    Busca en el objeto Applications el cliente de REDIS y devuelve
    la base de datos por default.

    :param obj: objeto a evaluar.
    :param throw: define el tipo de respuesta.
    :return: Database
    """

    app = find_app(obj)

    if redis.NAME not in app.cli \
            and not isinstance(app.cli[redis.NAME], ConnectionPool):
        log.error(f'Client "{redis.NAME}" not found')
        if throw is True:
            raise web.HTTPInternalServerError()
        return None

    return app.cli[redis.NAME]


def find_etcd(obj: APP_TYPE, throw: bool = True) -> Optional[Etcd3Client]:
    """
    Busca en el objeto Applications el cliente de ETCD y devuelve
    el cliente de conexión.

    :param obj: objeto a evaluar.
    :param throw: define el tipo de respuesta.
    :return: Database
    """

    app = find_app(obj)

    if etcd.NAME not in app.cli \
            and not isinstance(app.cli[etcd.NAME], Etcd3Client):
        log.error(f'Client "{etcd.NAME}" not found')
        if throw is True:
            raise web.HTTPInternalServerError()
        return None

    return app.cli[etcd.NAME]


# Wrappers

def pass_app(f):
    """
    Wrapper de la función "find_app".

    >>> @pass_app
    >>> def endpoint(app, **kwargs) -> None:
    >>>     pass
    """

    @wraps(f)
    async def wrapper(*args, **kwargs):
        extras = [] if len(args) == 1 else args[1:]
        return await f(find_app(args[0]), *extras, **kwargs)

    return wrapper


def pass_sql(f):
    """
    Wrapper de la función "find_sql".

    >>> @pass_sql
    >>> def endpoint(app, sql, **kwargs) -> None:
    >>>     pass
    """

    @wraps(f)
    async def wrapper(*args, **kwargs):
        app = find_app(args[0])
        extras = [] if len(args) == 1 else args[1:]
        return await f(app, *extras, sql=find_sql(app), **kwargs)

    return wrapper


def pass_nosql(f):
    """
    Wrapper de la función "find_nosql".

    >>> @pass_nosql
    >>> def endpoint(app, nosql, **kwargs) -> None:
    >>>     pass
    """

    @wraps(f)
    async def wrapper(*args, **kwargs):
        app = find_app(args[0])
        extras = [] if len(args) == 1 else args[1:]
        return await f(app, *extras, nosql=find_nosql(app), **kwargs)

    return wrapper


def pass_cache(f):
    """
    Wrapper de la función "find_cache".

    >>> @pass_cache
    >>> def endpoint(app, cache, **kwargs) -> None:
    >>>     pass
    """

    @wraps(f)
    async def wrapper(*args, **kwargs):
        app = find_app(args[0])
        extras = [] if len(args) == 1 else args[1:]
        return await f(app, *extras, cache=find_cache(app), **kwargs)

    return wrapper


def pass_etcd(f):
    """
    Wrapper de la función "find_etcd".

    >>> @pass_etcd
    >>> def endpoint(app, etcd, **kwargs) -> None:
    >>>     pass
    """

    @wraps(f)
    async def wrapper(*args, **kwargs):
        app = find_app(args[0])
        extras = [] if len(args) == 1 else args[1:]
        return await f(app, *extras, etcd=find_etcd(app), **kwargs)

    return wrapper


def _pass_all(app: APP_TYPE, client: bool = False) -> dict:
    ret = dict(
        sql=find_sql,
        nosql=find_nosql,
        cache=find_cache,
        etcd=find_etcd
    )
    for k, v in ret.items():
        try:
            args = [app, False]
            if k == 'nosql':
                args.append(client)
            v = v(*args)
        except Exception:
            v = None
        finally:
            ret[k] = v
    return ret


def pass_datalayer(f):
    """
    Wrapper de todas las funciones de la capa de datos.

    >>> @pass_datalayer
    >>> def endpoint(app, sql, nosql, cache, cache, etcd, **kwargs) -> None:
    >>>     pass
    """

    @wraps(f)
    async def wrapper(*args, **kwargs):
        app = find_app(args[0])
        extras = [] if len(args) == 1 else args[1:]
        return await f(app, *extras, **_pass_all(app), **kwargs)

    return wrapper


def pass_cnx(f):
    """
    Wrapper de todas las funciones de la capa de datos.

    >>> @pass_cnx
    >>> def endpoint(app, sql, nosql, cache, cache, etcd, **kwargs) -> None:
    >>>     pass
    """

    @wraps(f)
    async def wrapper(*args, **kwargs):
        app = find_app(args[0])
        extras = [] if len(args) == 1 else args[1:]
        return await f(app, *extras, **_pass_all(app, True), **kwargs)

    return wrapper


# Error

class APIError(web.HTTPException):
    """Custom API Error"""

    def __init__(
            self,
            reason: str,
            code: int = HTTPStatus.BAD_REQUEST,
            **kwargs
    ) -> None:
        super().__init__(reason=reason, **kwargs)
        self.status_code = code


def find_status_code(o: Any, default=HTTPStatus.BAD_REQUEST) -> Any:
    for x in ('status_code', 'status', 'code'):
        if hasattr(o, x):
            return getattr(o, x, default)
    return default


def find_message(o: Any, default='Uncontrolled') -> Any:
    for x in ('errors', 'reason', 'message'):
        if hasattr(o, x):
            return getattr(o, x, default)
    return default
