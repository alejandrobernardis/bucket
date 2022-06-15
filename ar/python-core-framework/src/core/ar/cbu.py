#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-05

import re
from typing import Union

from core.encoding import want_text
from core.errors import InvalidFormatError, InvalidLengthError, \
    InvalidChecksumError, MustBeStrError

__all__ = ['checksum', 'check', 'verify', 'cbu_rx']

cbu_rx = re.compile(r'^\d{22}$')


def checksum(value: str) -> str:
    """
    Comprueba la integridad del CBU y lo retorna.

    :param value: valor a verificar.
    :return: str
    """
    w = (3, 1, 7, 9)
    c = sum(int(y) * w[x % 4] for x, y in enumerate(reversed(value)))
    return str((10 - c) % 10)


def check(value: Union[str, int]) -> str:
    """
    Verifica la composición e integridad del CBU, de no existir error retorna
    el CBU, en caso contrario arrojará una Excepción.

    :param value: valor a verificar.
    :return: str
    """
    value = want_text(value)
    if not isinstance(value, str):
        raise MustBeStrError()
    if not value.isdigit():
        raise InvalidFormatError()
    if len(value) != 22:
        raise InvalidLengthError()
    if checksum(value[:7]) != value[7] or checksum(value[8:-1]) != value[-1]:
        raise InvalidChecksumError()
    return value


def verify(value: str) -> bool:
    """
    Verifica la composición e integridad del CBU, de no existir error retorna
    `TRUE`, en caso contrario retornará `FALSE`.

    :param value: valor a verificar.
    :return: bool
    """
    try:
        check(value)
        return True
    except Exception:
        return False
