#!/usr/bin/env python

from http import HTTPStatus
from typing import Union

from aiohttp import web
from bson import ObjectId
from core import json
from core.api import APIError, log
from core.dotted.collection import DottedDict
from core.encoding import want_text

__all__ = [
    'DATA_TYPE',
    'REQ_TYPE',
    'log_exception',
    'ResourceReturnedError',
    'ResourceNotFoundError',
    'ResourcePendingError',
    'default_handler',
    'default_response'
]

DATA_TYPE = Union[dict, DottedDict]
REQ_TYPE = Union[str, dict]


# -- logs --

def log_exception(key: str, err: Exception):
    log.error(f'{key} => ({err.__class__.__name__}) {err}', err)


# -- errors --

class ResourceNotFoundError(APIError):
    def __init__(self, message: str = 'Recurso no disponible', **kwargs):
        super().__init__(message, HTTPStatus.NOT_FOUND, **kwargs)


class ResourcePendingError(APIError):
    def __init__(self, message: str = 'Recurso pendiente', **kwargs):
        super().__init__(message, HTTPStatus.PAYMENT_REQUIRED, **kwargs)


class ResourceReturnedError(APIError):
    def __init__(self, message: str = 'Recurso devuelto', **kwargs):
        super().__init__(message, HTTPStatus.FORBIDDEN, **kwargs)


# -- default response --

def default_response(
        data: dict = None,
        status=HTTPStatus.OK,
        **kwargs
) -> web.Response:
    """
    Retorno por default para JSON.

    :param data: estructura de referencia
    :param status: estado de la respuesta
    :param kwargs: opcionales
    :return: Response
    """

    def _hook(_o):
        if isinstance(_o, (bytes, ObjectId)):
            return want_text(_o)
        return _o

    return web.Response(
        text=json.dumps(data, default=_hook).decode() if data else None,
        status=status,
        content_type='application/json',
        **kwargs
    )


# -- default handler --

async def default_handler(_: web.Request) -> web.Response:
    """
    Default handler.

    :param _: información del request
    :return: web.Response
    """
    return web.Response(text='Astor PIAZZOLLA')
