#!/usr/bin/env python

from typing import Optional

from core import config
from pydantic import BaseModel


class SentryModel(BaseModel):

    # cuenta
    account: str

    # proyecto
    project: str

    # token
    token: str

    # conexión
    cnxstr: str


class ContainerModel(BaseModel):

    # Container Host
    host: str = '0.0.0.0'

    # Container Port
    port: int = 8000


class ConfigModel(config.ConfigModel):
    """Modelo base de configuración."""

    # Container
    container: ContainerModel = ContainerModel()

    # Sentry
    sentry: Optional[SentryModel]
