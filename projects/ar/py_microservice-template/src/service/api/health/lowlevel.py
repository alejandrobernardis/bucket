#!/usr/bin/env python

from functools import partial
from typing import Callable, Union

from core.api import APP_TYPE, pass_app, find_app
from core.counters import CounterManager
from core.datetimex import uptime_calculate
from core.encoding import sanitizer, want_text
from core.services import mariadb, mongodb, redis, jobs

__all__ = [
    'client_counters_check',
    'jobs_check',
    'mariadb_check',
    'mongodb_check',
    'redis_check',
    'service_check',
    'uptime_check',
    'WORKING',
]

WORKING: str = 'WORKING'


async def _check(f: Callable, app: APP_TYPE) -> str:
    """
    Helper de service_check.

    :param f: función a ejecutar
    :param app: aplicación de referencia
    :return: bool
    """
    try:
        await f(app)
        return WORKING

    except Exception as e:
        msg: str = str(e)
        app.logger.error(msg)
        return msg


# (helper) mongo check
mariadb_check = partial(_check, mariadb.check)

# (helper) mongo check
mongodb_check = partial(_check, mongodb.check)

# (helper) redis check
redis_check = partial(_check, redis.check)

# (helper) redis check
jobs_check = partial(_check, jobs.check)

# mapeo de servicios
_services_map: dict = {
    mariadb.NAME: mariadb_check,
    mongodb.NAME: mongodb_check,
    redis.NAME: redis_check,
    jobs.NAME: jobs_check,
}


@pass_app
async def service_check(app: APP_TYPE) -> dict:
    """
    Verifica los servicios conectados.

    :param app: aplicación de referencia
    :return: dict
    """
    ret: dict = dict()
    for k, v in app.cfg.items():
        if k in _services_map and v is not None:
            ret[k] = await _services_map[k](app)
    return ret


# Server

def uptime_check(app: APP_TYPE, sanitize: bool = True) -> Union[dict, str]:
    """
    Verifica el uptime del servicio.

    :param app: aplicación de referencia
    :param sanitize: sanitizar el resultado
    :return: dict or str
    """
    try:
        uptime = uptime_calculate(find_app(app).cfg.initiated, for_humans=False)
        if sanitize is True:
            uptime = sanitizer(uptime, want_text)
        return uptime
    except Exception as e:
        return str(e)


def client_counters_check(app: APP_TYPE) -> Union[dict, str]:
    """
    Verifica los contadores definidos para la aplicación y devuelve
    un diccionario con los valores de los mismos.

    :param app: aplicación de referencia
    :return: dict or str
    """
    try:
        return dict(
            (k, dict((x.name, x.raw) for x in v.values()))
            for k, v in find_app(app).ctr.items()
            if isinstance(v, CounterManager)
        )
    except Exception as e:
        return str(e)
