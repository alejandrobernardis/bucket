#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-10

import os
import re
from copy import deepcopy
from functools import partial
from typing import Optional, Union, Callable

from dotenv import load_dotenv, dotenv_values
from pydantic import BaseModel

from core.pathx import Path, want_path

__all__ = ['load_env_file', 'load_env_values', 'load_env_parser',
           'load_env_files', 'mask_password', 'ConfigModel']

rx_pwd = re.compile(r'(pass[word]|pwd|secret)', re.I)


def mask_password(value: dict, mask: str = '******') -> dict:
    """
    Enmascara dentro de un diccionario todas las ocurrencias con relación
    a contraseñas.

    :param value: diccionario de referencia.
    :param mask: formato de la máscara.
    :return: dict
    """

    value = deepcopy(value)

    for k, v in value.items():
        if isinstance(v, dict):
            value[k] = mask_password(v, mask)
        elif rx_pwd.search(k):
            value[k] = mask

    return value


def _load_env(
        f: Callable,
        filename: Union[str, Path],
        **kwargs
) -> [dict, set, set]:
    """NOTA: de momento soporta únicamente archivos."""
    old_vars: set = set(os.environ.copy().keys())
    new_vars: Union[dict, bool] = f(filename, **kwargs)
    if not new_vars:
        raise SystemExit(f'The {filename} file could not be loaded')
    if isinstance(new_vars, bool):
        new_vars = os.environ.copy()
    data: dict = dict({k: v for k, v in new_vars.items() if k.isupper()})
    return data, old_vars, set(data.keys()) - old_vars


def load_env_parser(values: Optional[dict]) -> dict:
    """
    Retorna un diccionario agrupando las variables de entorno por su prefijo.

    >>> # EnvVar
    >>> DB_USERNAME="wallet"
    >>> DB_LOCAL_HOST="localhost"
    >>>
    >>> # Python dict
    >>> {'db': {'username': 'wallet', 'local_host': 'localhost'}}

    :param values: valores de referencia.
    :return: dict
    """

    data = dict()

    for k, v in values.items():
        k = k.lower()
        prefix = k.split('_', 1)

        if len(prefix) > 1:
            if prefix[0] not in data:
                data[prefix[0]] = dict()
            data[prefix[0]][prefix[1]] = v
        else:
            data[k] = v

    return data


def load_env_parser_2l(values: Optional[dict]) -> dict:
    """
    Retorna un diccionario agrupando las variables de entorno por su prefijo.

    >>> # EnvVar
    >>> DB_CNX1_USERNAME="wallet"
    >>> DB_CNX1_LOCAL_HOST="localhost"
    >>>
    >>> # Python dict
    >>> {'db': {'cnx1': {'username': 'wallet', 'local_host': 'localhost'}}}

    :param values: valores de referencia.
    :return: dict
    """

    data = load_env_parser(values)

    for k, v in data.items():
        data[k] = load_env_parser(v)

    return data


def load_env_files(
        source: Union[str, Path, list[Union[str, Path]]] = None,
        simple: bool = True,
        **kwargs
) -> dict:
    """
    Retorna un diccionario agrupando las variables de entorno por su prefijo.

    Buscará en el valor definido por `source`, en caso contrario utilizará
    una lista de ubicaciones por default.

    :param source: ruta de referencia.
    :param simple: determina si la agrupación es en uno (`true`)
                   o dos (`false`) niveles.
    :param kwargs: argumentos key-value opcionales.
    :return: dict
    """

    ret: dict = {}
    files = []

    if source is not None:
        if not isinstance(source, (list, tuple)):
            source: Path = want_path(source)
            if source.is_dir():
                files = source.glob('*.*')
            else:
                files.append(source)
        else:
            files = source
    else:
        name: str = os.getenv('ENV_FILE', '.env')

        if name != '.env':
            return load_env_files(name, **kwargs)

        user: Path = Path('~').expanduser()

        files.extend([
            Path(name),
            Path(f'../{name}'),
            Path(f'/app/{name}'),
            Path(f'/data/{name}'),
            Path(f'/etc/{name}'),
            Path(f'/{name}'),
            user.joinpath(name),
            user.joinpath('.config', name),
            user.joinpath('.local', name)
        ])

    for item in files:
        if not item.is_file():
            continue

        raw = load_env_values(item, **kwargs)[0]

        data = load_env_parser(raw) if simple is True \
            else load_env_parser_2l(raw)

        if data:
            ret.update(data)

    return ret


load_env_file = partial(_load_env, load_dotenv)
"""Carga las variables a partir de un archivo y luego las actualiza 
en el entorno."""

load_env_values = partial(_load_env, dotenv_values)
"""Carga las variables a partir de un archivo y retorna un diccionario 
con las mismas."""


# Config Model

class EngineModel(BaseModel):
    host: str
    port: int
    database: str
    username: Optional[str]
    password: str
    arguments: Optional[str]
    ca_cert: Optional[str]
    cert_key: Optional[str]
    cert_cert: Optional[str]
    timeout: Optional[int]
    try_policy: int
    try_sleep: float


class ServiceModel(BaseModel):
    host: str = '0.0.0.0'
    port: int = 8000
    cors: bool = True
    debug: bool = False
    reload: bool = False
    log_level: str = 'WARNING'
    log_format: str = '%a %t %r %s %b %{Referer}i'
    name: str = 'Frank Zappa'
    version: str = '1.0.0'
    try_policy: int = 3
    try_sleep: float = 10
    sess_time: float = 24 * 60 * 60
    verify: bool = True


class JobsModel(BaseModel):
    limit: int = 100
    pending_limit: int = 10000
    close_timeout: float = 0.1


class ConfigModel(BaseModel):
    """Modelo base de configuración."""

    # Configuración para `etcd` (opcional).
    etcd: Union[None, EngineModel, dict]

    # Configuración para `mariadb` (opcional).
    maria: Union[None, EngineModel, dict]

    # Configuración para `mongodb` (opcional).
    mongo: Union[None, EngineModel, dict]

    # Configuración para `redis` (opcional).
    redis: Union[None, EngineModel, dict]

    # Configuración para `jobs` (opcional).
    jobs: Union[None, JobsModel, dict]

    # Configuración del `service`.
    service: Optional[ServiceModel]
