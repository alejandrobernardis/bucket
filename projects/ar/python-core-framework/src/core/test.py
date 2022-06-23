#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-09

import asyncio
import logging
from typing import Callable

import uvloop
from aiohttp import web

from core.dotted.collection import DottedDict
from core.web import Application


async def make_init(
        cfg: dict = None,
        cleanup_ctx: list = None
) -> Application:

    app = Application(DottedDict(cfg))

    if cleanup_ctx is not None:
        app.cleanup_ctx.extend(cleanup_ctx)

    return app


def make_run(f: Callable, cfg: dict = None, **kwargs) -> None:
    logging.basicConfig(level=logging.DEBUG)
    uvloop.install()
    loop = asyncio.get_event_loop()
    task = loop.create_task(f(cfg, **kwargs))
    app = loop.run_until_complete(task)
    web.run_app(app, port=app.cfg.get('port', 14000))
