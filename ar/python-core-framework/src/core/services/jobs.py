#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-10

import asyncio
from typing import AsyncGenerator

from aiojobs import create_scheduler

from core.counters import CounterManager, Counter
from core.dotted.collection import DottedDict
from core.web import Application

__all__ = ['NAME', 'check', 'init']

NAME: str = 'jobs'


async def check(app: Application) -> None:
    """
    Verifica el funcionamiento de las tareas en segundo plano.

    :param app: aplicación de referencia.
    :return: None
    """

    async def _check(_x, _y, _z):
        await asyncio.sleep(_z)
        _x.logger.debug(f'{NAME} jobs-execute -> ok')
        _y['result'] = 7

    t, v = 1, dict()
    await app.cli.jobs.spawn(_check(app, v, t))
    await asyncio.sleep((t * 2) + 1)

    app.logger.debug(f'{NAME} jobs-check -> {v}')
    assert 'result' in v, 'data not match'


async def init(app: Application) -> AsyncGenerator[None, None]:
    """
    Inicia el servicio de JOBS provisto por AIOHTTP, en caso de requerirse
    un modelo más complejo, optar por celery.

    :param app: aplicación de referencia.
    :return: AsyncGenerator
    """

    cfg: DottedDict = app.cfg[NAME]
    app.logger.debug(f'{NAME} config -> {cfg}')

    jobs = await create_scheduler(**cfg)

    app.cli[NAME] = jobs
    app.ctr[NAME] = CounterManager(
        NAME,
        Counter('run'),
        Counter('don'),
        Counter('err'),
    )

    if app.cfg.service.verify:
        await check(app)
    app.logger.info(f'{NAME} started -> ok')

    yield

    await jobs.close()
