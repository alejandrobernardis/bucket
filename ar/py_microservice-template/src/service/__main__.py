#!/usr/bin/env python

import asyncio
import logging
import time

import sentry_sdk
import uvloop
from aiohttp import web
from core.pathx import Path
from core.services import etcd, mariadb, mongodb, redis, jobs
from core.web import Application
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from service import api
from service.config import ConfigModel

ROOT: Path = Path(__file__).parent


async def serve() -> Application:
    """
    Configuración de la aplicación.

    :return: Application
    """

    # definición de la aplicación

    app: Application = Application()
    
    app.cfg['root'] = ROOT
    app.cfg['initiated'] = time.time()
    app.discover_config(ConfigModel)

    # verificación de la configuración

    if 'service' not in app.cfg:
        raise SystemExit('Service configuration not found')

    # configuración del nivel de logging.

    if app.cfg.service.debug:
        level = 'DEBUG'

    else:
        level = app.cfg.service.log_level.upper()

    logging.basicConfig(level=level)
    app.logger.warning(f'app -> logging level: {level}')

    # configuración de sentry

    sentry_sdk.init(
      dsn=app.cfg.CFG_SENTRY_SDK,
      integrations=[AioHttpIntegration()]
    )

    # configuración de la api

    api.init(app)

    # asignación de servicios

    x: dict = {
        etcd.NAME: etcd.init,
        mariadb.NAME: mariadb.init,
        mongodb.NAME: mongodb.init,
        redis.NAME: redis.init,
        jobs.NAME: jobs.init,
    }

    app.cleanup_ctx.extend([
        x[k] for k, v in app.cfg.items() if k in x and v is not None
    ])

    # retorno de la instancia de la aplicación

    return app


def main() -> bool:
    """
    Inicialización del servicio para `docker swarm`/`kubernetes`.

    :return: bool
    """

    # definición del componente de loop

    uvloop.install()

    # configuración de la tarea

    loop = asyncio.get_event_loop()
    task = loop.create_task(serve())
    app = loop.run_until_complete(task)

    # inicio de la aplicación

    try:
        web.run_app(
            app,
            host=app.cfg.container.host,
            port=app.cfg.container.port,
            access_log_format=app.cfg.service.log_format
        )

    except Exception as e:
        app.logger.fatal(f'main loop -> {e}')
        return True


if __name__ == '__main__
    while main():
        pass
