#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-05

import re

from core.errors import MustBeStrError, InvalidFormatError

__all__ = ['check', 'verify', 'dni_rx']

dni_rx = re.compile(r'^\d{1,3}\.?\d{1,3}\.?\d{1,3}$')


def check(value: str) -> str:
    """
    Verifica la composición e integridad del DNI, de no existir error retorna
    el DNI, en caso contrario arrojará una Excepción.

    :param value: valor a verificar.
    :return: str
    """
    value = value.replace('.', '')
    if not isinstance(value, str):
        raise MustBeStrError()
    elif not dni_rx.match(value):
        raise InvalidFormatError()
    return value


def verify(value: str) -> bool:
    """
    Verifica la composición e integridad del DNI, de no existir error retorna
    `TRUE`, en caso contrario retornará `FALSE`.

    :param value: valor a verificar.
    :return: bool
    """
    try:
        check(value)
        return True
    except Exception:
        return False
