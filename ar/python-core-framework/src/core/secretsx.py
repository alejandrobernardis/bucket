#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-06-03

# TODO(berna): implementar un modelo de filtrado para excluir claves.

import os
import base64
import stat
from functools import cache
from io import StringIO
from typing import Any, Union, Optional, AbstractSet, NewType, Generator

from cryptography.fernet import Fernet, MultiFernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from dotenv import dotenv_values

from core import constants as ct
from core.dotted.collection import DottedDict
from core.encoding import want_bytes_list, want_bytes
from core.pathx import Path, want_path

__all__ = ['Secrets', 'SecretsWriter', 'make_secrets']


SecretKeys = NewType(
    'SecretKeys',
    Union[bytes, tuple[bytes, ...], tuple[tuple[bytes, bytes], ...]]
)

DEFAULT_SALT: bytes = \
    os.getenv('SECRETS_SALT', b'w$l73t#c0r3!PyTh0n.Pi4zz0Ll@=')


def _get_passphrase(secret: SecretKeys, salt: bytes = DEFAULT_SALT) -> tuple:
    a, b, x, y = None, None, [], []
    if isinstance(secret, ct.LIST_TYPE):
        for item in secret:
            if isinstance(item, ct.LIST_TYPE):
                a, b = item if len(item) == 2 else salt, item[0]
            else:
                a, b = salt, item
            x.append(a), y.append(b)
    else:
        x.append(salt), y.append(secret)
    return want_bytes_list(x), want_bytes_list(y)


@cache
def _generate_key(salt: bytes, value: bytes) -> bytes:
    key = PBKDF2HMAC(hashes.SHA256(), 32, salt, 100000, default_backend())
    return base64.urlsafe_b64encode(key.derive(value))


def _get_key(salt: Any, value: Any) -> Union[bytes, tuple]:
    if all([isinstance(salt, Generator), isinstance(salt, Generator)]):
        return tuple([_generate_key(x, y) for x, y in zip(salt, value)])
    if all([isinstance(salt, bytes), isinstance(salt, bytes)]):
        return _generate_key(salt, value)
    return base64.urlsafe_b64encode(value)


def _get_fernet(secret: SecretKeys) -> Union[Fernet, MultiFernet]:
    key = _get_key(*_get_passphrase(secret))
    if isinstance(key, tuple):
        return MultiFernet([Fernet(x) for x in key])
    return Fernet(key)


class Secrets:

    def __init__(
            self,
            domain: str,
            secret_key: SecretKeys,
            storage_path: Union[Path, str]
    ):
        """
        Administración de las claves de acceso.

        :param domain: dominio habilitado
        :param secret_key: clave secreta
        :param storage_path: ubicación raíz de los archivos
        """

        self._domain: str = domain
        self._secrets: DottedDict = DottedDict()
        self._secrets_sanitized: DottedDict = DottedDict()
        self._fernet: Union[Fernet, MultiFernet] = _get_fernet(secret_key)
        self._storage_path: Path = want_path(storage_path)
        self._path: Path = self._storage_path.joinpath(domain)

    @cache
    def _get_path(self, service: str) -> Path:
        secret = f'{service}.key' if not service.endswith('.key') else ''
        return self._path.joinpath(secret)

    @cache
    def _get_key(self, service: str) -> bytes:
        secret = self._get_path(service).read_bytes().strip()
        return self._set_key(service, secret)

    def _set_key(self, service: str, secret: bytes) -> bytes:
        if isinstance(self._fernet, MultiFernet):
            secret = self._fernet.rotate(secret)
        self._secrets[service] = self._fernet.decrypt(secret)
        return self._secrets[service]

    def load(self) -> bool:
        """
        Carga en memoria todas los servicios disponibles.

        :return: bool
        """

        for secret in self._path.glob('*.key'):
            self._get_key(secret.stem)

        return self.count() > 0

    def get(self, service: str, default: bytes = None) -> bytes:
        """
        Retorna el valor de un servicio, en caso de no estar cargado en memoria,
        intentará cargarlo.

        :param service: nombre del servicio
        :param default: valor por default
        :return: bytes
        """

        if service not in self._secrets:
            self._get_key(service)

        return self._secrets.get(service, default)

    __getitem__ = get
    __getattr__ = get

    def _sanitizer(self, value: [bytes, DottedDict]) -> DottedDict:
        if isinstance(value, DottedDict):
            return DottedDict((k, self._sanitizer(v)) for k, v in value.items())
        values: DottedDict = DottedDict()
        for k, v in dotenv_values(stream=StringIO(value.decode())).items():
            values[k.lower().split('_', 1)[1]] = v
        return values

    def sanitize(self, service: str, default: Any = None) -> Any:
        """
        Sanitiza el contenido del servicio convirtiendo en un diccionario
        y retorna su contenido.

        :param service: nombre del servicio
        :param default: valor por default
        :return: Any
        """

        if service not in self._secrets_sanitized:
            try:
                default = self._sanitizer(self.get(service))
            except Exception:
                pass
            self._secrets_sanitized[service] = default

        return self._secrets_sanitized[service]

    def sanitize_all(self) -> bool:
        """
        Sanitiza todos los servicios convirtiendo el contenido del servicio
        en un diccionario.

        :return: bool
        """

        for service in self._secrets.keys():
            self.sanitize(service)

        return len(self._secrets_sanitized) > 0

    def keys(self) -> AbstractSet:
        """
        Retorna una lista con los servicios cargados en memoria.

        :return: set
        """

        return self._secrets.keys()

    def has(self, service: str) -> bool:
        """
        Verifica si un servicio se encuentra cargado en memoria y retorna `TRUE`
        en caso de éxito, de lo contrario retornará `FALSE`.

        :param service: nombre del servicio
        :return: bool
        """

        return service in self._secrets

    __contains__ = has

    def count(self) -> int:
        """
        Verifica la cantidad de servicios cargados en memoria y retorna
        el valor.

        :return: int
        """

        return len(self._secrets)

    def prune(self) -> None:
        """
        Borra los servicios cargados en memoria.

        :return: None
        """

        self._secrets = {}


class SecretsWriter(Secrets):

    def _write_key(self, service: str, secret: bytes) -> bool:
        f = self._get_path(service)
        if not f.exists():
            f.touch()
        f.chmod(stat.S_IRUSR | stat.S_IWUSR)
        w: int = f.write_bytes(secret)
        self._secrets[service] = secret
        return w and w > 0

    def put(self, service: str, secret: bytes) -> Optional[bytes]:
        """
        Almacena o actualiza un servicio.

        :param service: nombre del servicio
        :param secret: valores asociados al servicio
        :return: Optional[bytes]
        """

        token = self._fernet.encrypt(want_bytes(secret))

        if self._write_key(service, token):
            return self._get_key(service)

        return None

    def save(self, secrets_list: tuple[tuple[str, bytes], ...]) -> bool:
        """
        Almacena o actualiza una lista de servicios.

        :param secrets_list: lista de servicios
        :return: bool
        """

        return all([self.put(x, y) for x, y in secrets_list])


def make_secrets(
        secret_key: SecretKeys,
        storage_path: Union[Path, str]
) -> bool:
    """
    Crear a partir de una o varias claves y la ruta los archivos cifrados
    con el contenido asociado a cada servicio.

    :param secret_key: claves de cifrado
    :param storage_path: ubicación de los archivos de servicio
    :return:
    """
    count: int = 0

    for domain in want_path(storage_path).glob('*'):
        if not domain.is_dir():
            continue

        s: SecretsWriter = SecretsWriter(domain.name, secret_key, storage_path)

        for secret in domain.glob('*.plain'):
            s.put(secret.stem, secret.read_bytes())

        count += s.count()

    return count > 0
