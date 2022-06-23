#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-12-06

import asyncio
from typing import Optional, AsyncGenerator

from aetcd3 import Etcd3Client
from aetcd3.exceptions import ConnectionFailedError, ConnectionTimeoutError
from pydantic import BaseModel, Field

from core.counters import Counter
from core.dotted.collection import DottedDict
from core.web import Application

__all__ = ['NAME', 'check', 'init']

NAME: str = 'etcd'


class _DBx(BaseModel):
    host: str = 'localhost'
    port: int = 2379
    user: Optional[str] = Field(None, alias='username')
    password: Optional[str] = None
    ca_cert: Optional[str] = None
    cert_key: Optional[str] = None
    cert_cert: Optional[str] = None
    timeout: Optional[int] = None
    grpc_options: Optional[str] = Field(None, alias='arguments')


async def check(app: Application) -> None:
    """
    Verifica que la conexión al servicio sea correcta.

    :param app: aplicación de referencia.
    :return: None
    """

    async with app.cli[NAME] as cnx:
        k, v = '/key-test', b'value-test'
        await cnx.put(k, v)
        vv, _ = await cnx.get(k)
        await cnx.delete(k)

    app.logger.debug(f'{NAME} cnx-check -> {v}, {vv}')
    assert vv == v, 'cache not match'


async def init(app: Application) -> AsyncGenerator[None, None]:
    """
    Inicia el servicio de ETCD.

    :param app: aplicación de referencia.
    :return: AsyncGenerator
    """

    cfg: DottedDict = app.cfg[NAME]
    counter: Counter = Counter(NAME)

    while 1:
        try:
            cnx: _DBx = _DBx.parse_obj(cfg)
            app.logger.debug(f'{NAME} cnx-str -> {counter.raw} : {cnx}')

            pool = Etcd3Client(**cnx.dict())
            app.cli[NAME] = pool

            if app.cfg.service.verify:
                await check(app)
            app.logger.info(f'{NAME} cnx-status -> ok')
            break

        except (ConnectionFailedError, ConnectionTimeoutError) as e:
            app.logger.error(f'{NAME} cnx-error -> {e}')

            if counter >= cfg.try_policy:
                raise SystemExit()

            await asyncio.sleep(cfg.try_sleep)
            counter.increment()

        except Exception as e:
            app.logger.error(f'{NAME} cnx-exit -> {e}')
            raise SystemExit()

    yield

    await pool.close()


if __name__ == '__main__':
    from core.test import make_run, make_init
    make_run(make_init, {
        NAME: {
            'host': 'etcd0',
            'port': 2379,
            # 'username': 'frank',
            # 'password': 'frank',
            'try_policy': 3,
            'try_sleep': .5,
        }
    }, cleanup_ctx=[init])
