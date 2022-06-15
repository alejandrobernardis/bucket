#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-03

import time
from datetime import datetime, timedelta, date
from typing import Any, NewType, Optional

import pytz
from core import constants as ct

__all__ = ['week_range', 'uptime_calculate', 'timing', 'timing_iter',
           'now', 'now_delta', 'epoch', 'now_to_sql', 'now_to_iso',
           'Date', 'DateTime', 'TimeDelta']


ZERO = timedelta(0)
SQL_TIME = '%Y-%m-%d %H:%M:%S'
utc = pytz.utc

Date = NewType('Date', date)
DateTime = NewType('DateTime', datetime)
TimeDelta = NewType('TimeDelta', timedelta)


def week_range(value: Optional[date] = None) -> tuple[datetime, datetime]:
    """
    Calcula el rango de la semana a partir de valor pasado como argumento. Si
    el valor es distinto de `date`, utilizará la fecha actual.

    >>> week_range(date('2021-06-06'))
    >>> # (datetime(2021, 6, 6, 0, 0), datetime(2021, 6, 12, 0, 0))

    :param value: fecha de referencia
    :return: tuple
    """

    if not isinstance(value, date):
        value = date.today()

    value = datetime(value.year, value.month, value.day)
    year, week, dow = value.isocalendar()

    ws = value if dow == 7 else value - timedelta(dow)
    we = ws + timedelta(6)

    return ws, we


def uptime_calculate(
        start: float,
        check: float = None,
        for_humans: bool = True
) -> dict:
    """
    Calcula el tiempo estimado de uptime a partir de dos fechas.

    :param start: fecha de inicio
    :param check: fecha de muestra
    :param for_humans: formato para humanos
    :return: dict
    """

    if check is None:
        check = time.time()

    uptime = check - start

    days, seconds = \
        uptime // ct.SECONDS_PER_DAY, \
        uptime % ct.SECONDS_PER_DAY

    hours, seconds = \
        seconds // ct.SECONDS_PER_HOUR, \
        seconds % ct.SECONDS_PER_HOUR

    minutes, seconds = \
        seconds // ct.SECONDS_PER_MINUTE, \
        seconds % ct.SECONDS_PER_MINUTE

    ret = {
        'uptime': {
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        },
        'epoch': {
            'start': start,
            'check': check,
            'uptime': uptime
        }
    }

    if for_humans is True:
        ret['human'] = {
            'start': datetime.utcfromtimestamp(start),
            'check': datetime.utcfromtimestamp(check)
        }

    return ret


def timing(start: float) -> float:
    """
    Retorna un delta entre el tiempo actual y el de inicio.

    :param start: timestamp de inicio
    :return: float
    """

    return time.time() - start


def timing_iter(
        f: Any,
        args: tuple = None,
        kwargs: dict = None,
        x: int = 1000,
        y: int = 100
) -> float:
    """
    Calcula el tiempo transcurrido desde el inicio hasta el final
    de las iteraciones.

    :param f: función de referencia
    :param args: argumentos
    :param kwargs: key-value argumentos
    :param x: cantidad de ejecuciones
    :param y: cantidad de ciclos
    :return: float
    """

    args = args or []
    kwargs = kwargs or {}
    start: float = time.process_time()

    _ = [f(*args, **kwargs) for _ in range(y) for _ in range(x)]

    return time.process_time() - start


def now(time_zone=None) -> datetime:
    if time_zone is None:
        return datetime.utcnow()
    return datetime.now(time_zone)


def now_delta(time_zone=None, **kwargs) -> datetime:
    return now(time_zone) + timedelta(**kwargs)


def epoch(time_zone=None) -> str:
    return now(time_zone).strftime('%s')


def now_to_sql(time_zone=None, template=SQL_TIME) -> str:
    return date_to_sql(now(time_zone), template)


def date_to_sql(value, template=SQL_TIME) -> str:
    return value.strftime(template)


def now_to_iso(time_zone=None) -> str:
    if time_zone is None:
        value = datetime.utcnow()
    else:
        value = datetime.now(time_zone)
    return value.isoformat()
