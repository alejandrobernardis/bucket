#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-07-31

from http import HTTPStatus

import aiohttp_cors
from aiohttp import web
from core.api import find_app, find_status_code, find_message
from core.pathx import Path
from core.web import Application
from pydantic.error_wrappers import ValidationError

from service.api import health
from service.api.lowlevel import default_response, default_handler

__all__ = ['init', ]

SERVICES: tuple = (health, )


@web.middleware
async def handler_middleware(req: web.Request, handler) -> web.Response:
    """
    Captura los request y devuelve una respuesta formateada.

    :param req: información del request
    :param handler: función a ejecutar
    :return: Response
    """
    app: Application = find_app(req)

    try:
        app.ctr.main.req.increment()
        res = await handler(req)

    except Exception as e:
        app.ctr.main.err.increment()

        if app.cfg.service.debug:
            app.logger.exception('-- EXCEPT --')

        # En caso de que el schema sea incorrecto.
        if isinstance(e, ValidationError):
            err: dict = dict(
                code=HTTPStatus.BAD_REQUEST,
                message=e.errors()
            )

        # En caso de cualquier error que surja
        else:
            err: dict = dict(
                code=find_status_code(e, -1),
                message=find_message(e)
            )

        cod: int = err['code']
        sta: int = cod \
            if HTTPStatus.CONTINUE <= cod <= \
                HTTPStatus.NETWORK_AUTHENTICATION_REQUIRED \
            else HTTPStatus.BAD_REQUEST
        res = default_response(err, sta)

    res.headers['Server'] = app.cfg.service.name
    return res


def init(app: Application, **kwargs) -> None:
    """
    Inicia los endpoints del microservice.

    :param app: aplicación de referencia
    :return: None
    """

    # asignación del middleware

    app.middlewares.append(handler_middleware)

    # asignación de los endpoints

    for routes in SERVICES:
        table = getattr(routes, 'api', None)

        if table is not None:
            app.add_routes(table)
            app.logger.info(f'{routes.__name__} -> route table added')

            if hasattr(routes, 'init') and callable(routes.init):
                routes.init(app, **kwargs)

    # asignación de defaults

    static_path: Path = app.cfg.root.parent / 'static'

    app.router.add_get('/', default_handler)
    app.router.add_static('/static/', path=static_path)

    # activación de CORS

    if app.cfg.service.get('cors', False):
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_methods="*",
                allow_headers="*",
                max_age=3600
            )
        })

        for route in app.router.routes():
            cors.add(route)
