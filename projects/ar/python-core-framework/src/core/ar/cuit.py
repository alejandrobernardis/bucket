#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-05

import re

from core.errors import InvalidFormatError, InvalidLengthError, \
    InvalidChecksumError, MustBeStrError

__all__ = ['checksum', 'check', 'verify', 'cuit_rx']

cuit_rx = re.compile(r'^\d{2}-?\d{8}-?\d$')


def checksum(value: str):
    """
    Comprueba la integridad del CUIT y lo retorna.

    :param value: valor a verificar.
    :return: str
    """
    w = (5, 4, 3, 2, 7, 6)
    c = sum(int(y) * w[x % 6] for x, y in enumerate(value)) % 11
    return '012345678990'[11 - c]


def check(value: str) -> str:
    """
    Verifica la composición e integridad del CUIT, de no existir error retorna
    el CUIT, en caso contrario arrojará una Excepción.

    :param value: valor a verificar.
    :return: str
    """
    value = value.replace('-', '')
    if not isinstance(value, str):
        raise MustBeStrError()
    if not value.isdigit():
        raise InvalidFormatError()
    if len(value) != 11:
        raise InvalidLengthError()
    if checksum(value[:-1]) != value[-1]:
        raise InvalidChecksumError()
    return value


def verify(value: str) -> bool:
    """
    Verifica la composición e integridad del CUIT, de no existir error retorna
    `TRUE`, en caso contrario retornará `FALSE`.

    :param value: valor a verificar.
    :return: bool
    """
    try:
        return bool(check(value))
    except Exception:
        return False
