#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-08

# TODO(berna): para a cnx-str

import asyncio
from typing import AsyncGenerator

import aioredis

from core.counters import Counter
from core.dotted.collection import DottedDict
from core.web import Application

__all__ = ['NAME', 'check', 'init']

NAME: str = 'redis'


async def check(app: Application) -> None:
    """
    Verifica que la conexión al servicio sea correcta.

    :param app: aplicación de referencia.
    :return: None
    """

    cnx: aioredis.Redis = app.cli[NAME]
    k, v = 'key-test', b'value-test'
    await cnx.execute_command('set', k, v)
    vv = await cnx.execute_command('get', k)
    await cnx.execute_command('del', k)

    app.logger.debug(f'{NAME} cnx-check -> {v}, {vv}')
    assert vv == v, 'cache not match'


async def init(app: Application) -> AsyncGenerator[None, None]:
    """
    Inicia el servicio de REDIS.

    :param app: aplicación de referencia.
    :return: AsyncGenerator
    """

    cfg: DottedDict = app.cfg[NAME]
    counter: Counter = Counter(NAME)

    while 1:
        try:
            pwd: str = f':{cfg.password}@' if cfg.password else ''
            cnx: str = f'redis://{pwd}{cfg.host}:{cfg.port}/{cfg.database}'
            app.logger.debug(f'{NAME} cnx-str -> {counter.raw} : {cnx}')

            pool = aioredis.ConnectionPool.from_url(cnx, max_connections=10)
            pcli = aioredis.Redis(connection_pool=pool)
            app.cli[NAME] = pcli

            if app.cfg.service.verify:
                await check(app)
            app.logger.info(f'{NAME} cnx-status -> ok')
            break

        except (OSError, ConnectionRefusedError) as e:
            app.logger.error(f'{NAME} cnx-error -> {e}')

            if counter >= cfg.try_policy:
                raise SystemExit()

            await asyncio.sleep(cfg.try_sleep)
            counter.increment()

        except Exception as e:
            app.logger.error(f'{NAME} cnx-exit -> {e}')
            raise SystemExit()

    yield

    await pcli.close()
    await pool.disconnect()


if __name__ == '__main__':
    from core.test import make_run, make_init
    make_run(make_init, {
        NAME: {
            'host': 'redis',
            # 'port': 6379,
            'port': 14600,
            'username': 'frank',
            'password': 'frank',
            'database': '1',
            'try_policy': 3,
            'try_sleep': .5,
        }
    }, cleanup_ctx=[init])
