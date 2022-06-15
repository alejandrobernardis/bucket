#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-03-31

import asyncio
from abc import ABC, abstractmethod
from functools import cache
from http import HTTPStatus
from typing import Optional, Generator, Any

from aiohttp import ClientSession, hdrs, ClientResponse
from aiohttp.typedefs import StrOrURL
from yarl import URL

from core.counters import CounterManager, Counter
from core.web import Application

__all__ = ['RequestContextError', 'RequestContext', 'ApiClientABC']

RETRY_SLEEP: int = 3
RETRY_ATTEMPTS: int = 5


class RequestContextError(Exception):
    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(message)


class RequestContext:

    def __init__(
            self,
            client: 'ApiClientABC',
            method: str,
            url: StrOrURL,
            **kwargs
    ) -> None:
        """
        Contexto de ejecución del request.

        :param client: cliente de referencia.
        :param method: método de referencia.
        :param url: url de referencia.
        :param kwargs: argumentos key-value opcionales
        """

        self._client = client
        self._method = method
        self._url = url
        self._kwargs = kwargs
        self._res: Optional[ClientResponse] = None
        self._retry = Counter('retry')
        self._retry_sleep = RETRY_SLEEP

    async def do(self, retry: bool = False) -> ClientResponse:
        """
        Inicia el request, en caso de que el cliente no haya iniciado la sesión,
        intentará iniciarla y luego volverá a realizar la petición.

        :return: ClientResponse
        """

        if retry is True and not await self._client.login(True):
            if not self._retry.increment() % (RETRY_ATTEMPTS + 1):
                raise RequestContextError(f'Reject connection (after '
                                          f'{RETRY_ATTEMPTS} attempts)')
            await asyncio.sleep(self._retry_sleep)

        self._client.counters.req.increment()

        self._res = await self._client.sess.request(
            self._method,
            self._client.check_url(self._url),
            **self._kwargs
        )

        code: int = self._res.status

        if code != HTTPStatus.OK:
            self._client.counters.err.increment()

        if code == HTTPStatus.UNAUTHORIZED:
            return await self.do(True)

        return self._res

    def __await__(self) -> Generator[Any, None, ClientResponse]:
        return self.__aenter__().__await__()

    async def __aenter__(self) -> ClientResponse:
        return await self.do()

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._res is not None:
            if not self._res.closed:
                self._res.close()


class ApiClientABC(ABC):

    def __init__(
            self,
            name: str,
            app: Application,
            endpoint: Optional[StrOrURL] = None,
            auth_endpoint: Optional[StrOrURL] = None,
            session: Optional[ClientSession] = None,
            headers: Optional[dict] = None
    ) -> None:
        """
        Cliente REST base.

        :param name: nombre del cliente.
        :param app: aplicación de referencia.
        :param endpoint: endpoint base.
        :param auth_endpoint: endpoint de autenticación.
        :param session: sesión existente de referencia.
        :param headers: cabeceras base
        """

        self._name: str = name.lower()
        self._app: Application = app

        self._counters: CounterManager = CounterManager(
            self.name,
            Counter('req'),
            Counter('err'),
            Counter('log'),
            Counter('log_err'),
        )

        self._endpoint: URL = self.check_url(endpoint)
        self._auth_endpoint: URL = self.check_url(auth_endpoint)

        if headers is None:
            headers = {
                hdrs.ACCEPT: 'application/json',
                hdrs.CONTENT_TYPE: 'application/json;charset=UTF-8'
            }

        if session is not None and headers is not None:
            session.headers.update(headers)

        self._sess: ClientSession = session or ClientSession(headers=headers)
        self.register()

    def register(self, app: Optional[Application] = None) -> None:
        """
        Registra el cliente en la aplicación de referencia.

        :param app: aplicación de referencia.
        :return: None
        """

        if app is None:
            app = self._app

        app.cli[self.name] = self
        app.ctr[self.name] = self.counters

    def unregister(self, app: Optional[Application] = None) -> None:
        """
        Elimina el registro del cliente en la aplicación de referencia.

        :param app: aplicación de referencia.
        :return: None
        """

        if app is None:
            app = self._app

        if self.name in app.cli:
            del app.cli[self.name]

        if self.name in app.ctr:
            del app.ctr[self.name]

    @property
    def name(self) -> str:
        """
        Retorno el nombre del cliente.

        :return: str
        """

        return self._name

    @property
    def app(self) -> Application:
        """
        Retorna la instancia asociada de la aplicación en el cliente.

        :return: Application
        """
        return self._app

    @property
    def sess(self) -> ClientSession:
        """
        Retorna la sesión establecida en el cliente.

        :return: ClientSession
        """

        return self._sess

    @property
    def counters(self) -> CounterManager:
        """
        Retorna los contadores definidos en el cliente.

        :return: CounterManager
        """

        return self._counters

    @property
    def closed(self) -> bool:
        """
        Retorna `TRUE` en caso de que la cliente haya cerrado la sesión,
        en caso contrario retornará `FALSE`.

        :return: bool
        """
        return self.sess.closed

    # auth

    @abstractmethod
    async def login(self, force: bool = False, **kwargs) -> Optional[str]:
        """
        Inicio de sesión.

        :param force: forzar el inicio de sesión.
        :param kwargs: argumentos key-value opcionales.
        :return: Optional[str]
        """

        raise NotImplementedError()

    @abstractmethod
    def logout(self) -> None:
        """
        Cierre de sesión.

        :return: None
        """

        raise NotImplementedError()

    @abstractmethod
    def is_logged(self) -> bool:
        """
        Retorna `TRUE` en caso de que la sesión esté iniciada, en caso
        contrario retornará `FALSE`.

        :return: bool
        """

        raise NotImplementedError()

    # helpers

    @cache
    def check_url(self, url: StrOrURL) -> URL:
        """
        Normaliza la URL.

        :param url: valor a normalizar.
        :return: URL
        """

        if isinstance(url, str):
            u: URL = URL(url)

            if not url.startswith('http'):
                return self._endpoint.join(u)

            return u

        return url

    # request

    def request(self, method: str, url: StrOrURL, **kwargs) -> RequestContext:
        return RequestContext(self, method, url, **kwargs)

    def head(self, url: StrOrURL, **kwargs) -> RequestContext:
        return RequestContext(self, hdrs.METH_HEAD, url, **kwargs)

    def get(self, url: StrOrURL, **kwargs) -> RequestContext:
        return RequestContext(self, hdrs.METH_GET, url, **kwargs)

    def post(self, url: StrOrURL, **kwargs) -> RequestContext:
        return RequestContext(self, hdrs.METH_POST, url, **kwargs)

    def put(self, url: StrOrURL, **kwargs) -> RequestContext:
        return RequestContext(self, hdrs.METH_PUT, url, **kwargs)

    def patch(self, url: StrOrURL, **kwargs) -> RequestContext:
        return RequestContext(self, hdrs.METH_PATCH, url, **kwargs)

    def delete(self, url: StrOrURL, **kwargs) -> RequestContext:
        return RequestContext(self, hdrs.METH_DELETE, url, **kwargs)

    def options(self, url: StrOrURL, **kwargs) -> RequestContext:
        return RequestContext(self, hdrs.METH_OPTIONS, url, **kwargs)

    def trace(self, url: StrOrURL, **kwargs) -> RequestContext:
        return RequestContext(self, hdrs.METH_TRACE, url, **kwargs)

    def connect(self, url: StrOrURL, **kwargs) -> RequestContext:
        return RequestContext(self, hdrs.METH_CONNECT, url, **kwargs)

    # magic

    async def __aenter__(self) -> 'ApiClientABC':
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if not self.sess.closed:
            await self.sess.close()
