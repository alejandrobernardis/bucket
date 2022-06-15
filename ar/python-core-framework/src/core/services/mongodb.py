#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-08

# TODO(berna): para a cnx-str

import asyncio
from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError

from core.counters import Counter
from core.dotted.collection import DottedDict
from core.web import Application

__all__ = ['NAME', 'check', 'init']

NAME: str = 'mongo'


async def check(app: Application) -> None:
    """
    Verifica que la conexión al servicio sea correcta.

    :param app: aplicación de referencia.
    :return: None
    """

    db = app.cli[NAME].test

    v = {'check': '1'}
    await db.check.insert_one(v)
    vv = await db.check.find_one()
    await app.cli[NAME].test.command('dropDatabase')

    app.logger.debug(f'{NAME} cnx-check -> {v}, {vv}')
    assert vv == v, 'data not match'


async def init(app: Application) -> AsyncGenerator[None, None]:
    """
    Inicia el servicio de MONGODB.

    :param app: aplicación de referencia.
    :return: AsyncGenerator
    """

    cfg: DottedDict = app.cfg[NAME]
    counter: Counter = Counter(NAME)

    while 1:
        try:
            arg: str = f'?{cfg.arguments}' if cfg.arguments else ''
            cnx: str = f'mongodb://{cfg.username}:{cfg.password}' \
                       f'@{cfg.host}:{cfg.port}/{arg}'
            app.logger.debug(f'{NAME} cnx-str -> {counter.raw} : {cnx}')

            pool = AsyncIOMotorClient(cnx)
            app.cli[NAME] = pool

            if app.cfg.service.verify:
                await check(app)
            app.logger.info(f'{NAME} cnx-status -> ok')
            break

        except (OperationFailure, ServerSelectionTimeoutError) as e:
            app.logger.error(f'{NAME} cnx-error -> {e}')

            if counter >= cfg.try_policy:
                raise SystemExit()

            await asyncio.sleep(cfg.try_sleep)
            counter.increment()

        except Exception as e:
            app.logger.error(f'{NAME} cnx-exit -> {e}')
            raise SystemExit()

    yield

    pool.close()


if __name__ == '__main__':
    from core.test import make_run, make_init
    make_run(make_init, {
        NAME: {
            'host': 'mongo',
            'port': 27017,
            'username': 'frank',
            'password': 'frank',
            'database': '',
            'arguments': '',
            'try_policy': 3,
            'try_sleep': .5,
        }
    }, cleanup_ctx=[init])
