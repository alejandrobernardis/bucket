#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-08

# TODO(berna): para a cnx-str

import asyncio
from typing import AsyncGenerator

import aiomysql
from pydantic import BaseModel, Field

from core.counters import Counter
from core.dotted.collection import DottedDict
from core.web import Application

__all__ = ['NAME', 'check', 'init']

NAME: str = 'maria'


class _DBx(BaseModel):
    host: str = 'localhost'
    port: int = 3306
    user: str = Field('root', alias='username')
    password: str = ''
    db: str = Field('mysql', alias='database')


async def check(app: Application) -> None:
    """
    Verifica que la conexión al servicio sea correcta.

    :param app: aplicación de referencia.
    :return: None
    """

    async with app.cli[NAME].acquire() as dnx:
        async with dnx.cursor() as cur:
            v = 7
            await cur.execute(f'SELECT {v};')
            (vv,) = await cur.fetchone()

    app.logger.debug(f'{NAME} cnx-check -> {v}, {vv}')
    assert vv == v, 'data not match'


async def init(app: Application) -> AsyncGenerator[None, None]:
    """
    Inicia el servicio de MARIADB.

    :param app: aplicación de referencia.
    :return: AsyncGenerator
    """

    cfg: DottedDict = app.cfg[NAME]
    counter: Counter = Counter(NAME)

    while 1:
        try:
            cnx: _DBx = _DBx.parse_obj(cfg)
            app.logger.debug(f'{NAME} cnx-str -> {counter.raw} : {cnx}')

            pool = await aiomysql.create_pool(**cnx.dict())
            app.cli[NAME] = pool

            if app.cfg.service.verify:
                await check(app)
            app.logger.info(f'{NAME} cnx-status -> ok')
            break

        except (OSError, aiomysql.OperationalError) as e:
            app.logger.error(f'{NAME} cnx-error -> {e}')

            if e.args[0] != 2003 or counter >= cfg.try_policy:
                raise SystemExit()

            await asyncio.sleep(cfg.try_sleep)
            counter.increment()

        except Exception as e:
            app.logger.error(f'{NAME} cnx-exit -> {e}')
            raise SystemExit()

    yield

    pool.close()
    await pool.wait_closed()


if __name__ == '__main__':
    from core.test import make_run, make_init
    make_run(make_init, {
        NAME: {
            'host': 'maria',
            'port': 3306,
            'username': 'frank',
            'password': 'frank',
            'database': 'frank',
            'try_policy': 3,
            'try_sleep': .5,
        }
    }, cleanup_ctx=[init])
