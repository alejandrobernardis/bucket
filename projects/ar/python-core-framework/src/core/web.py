#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-03-31

from functools import cache
from typing import Optional

from aiohttp import web, typedefs
from yarl import URL

from core.config import load_env_files, ConfigModel
from core.counters import CounterManager, Counter
from core.dotted.collection import DottedDict

__all__ = ['Application', 'str_to_url']


class Application(web.Application):

    def __init__(self, cfg: Optional[DottedDict] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # configuración global
        self._cfg: DottedDict = cfg or DottedDict()

        # clientes globales
        self._cli: DottedDict = DottedDict()

        # contadores globales
        self._ctr: DottedDict = DottedDict()

        # contadores
        self._ctr['main'] = CounterManager(
            'main',
            Counter('req'),
            Counter('err')
        )

    @property
    def cfg(self) -> DottedDict:
        return self._cfg

    @property
    def cli(self) -> DottedDict:
        return self._cli

    @property
    def ctr(self) -> DottedDict:
        return self._ctr

    def discover_config(self, model=ConfigModel, **kwargs) -> None:
        self.cfg.update(model.parse_obj(load_env_files(**kwargs)).dict())


@cache
def str_to_url(value: typedefs.StrOrURL) -> URL:
    if isinstance(value, str):
        value = URL(value)
    return value
