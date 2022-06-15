#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-06

import re
from enum import Enum
from functools import partial
from typing import Any, Callable

from core.errors import MustBeStrError, InvalidFormatError

__all__ = ['client_id_rx', 'check_client_id', 'verify_client_id',
           'cxu_alias_rx', 'check_cxu_alias', 'verify_cxu_alias',
           'origin_id_rx', 'check_origin_id', 'verify_origin_id',
           'AutoName']


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


def _is_str(value: Any) -> bool:
    if not isinstance(value, str):
        raise MustBeStrError()
    return True


def _check(regex: re, value: Any) -> bool:
    if _is_str(value) and regex.match(value) is None:
        raise InvalidFormatError()
    return True


def _verify(func: Callable, value: Any) -> bool:
    try:
        return func(value)
    except Exception:
        return False


# C(x)U Alias => (
#   Identificador alfanumérico (a-z, 0-9), opcional la inclusión
#   de puntos (.) y/o guiones medios (-), con un largo mínimo de seis (6)
#   y un máximo de veinte (20) caracteres.
# )
# Example: alias-cvu-ejemplo
# Example: alias-cvu.ejemplo
cxu_alias_rx = re.compile(r'^[a-z0-9.-]{6,20}$', re.I)
check_cxu_alias = partial(_check, cxu_alias_rx)
verify_cxu_alias = partial(_verify, check_cxu_alias)

# Client ID => (
#   Identificador numérico (0-9) con un largo mínimo de uno (1) y un máximo de
#   doce (12) caracteres.
# )
# Example: 123
# Example: 000123
client_id_rx = re.compile(r'^\d{1,12}$')
check_client_id = partial(_check, client_id_rx)
verify_client_id = partial(_verify, check_client_id)

# Origin ID => (
#   Identificador numérico (0-9) con un largo mínimo de uno (1) y un máximo de
#   quince (15) caracteres.
# )
# Example: 123
# Example: 000123
origin_id_rx = re.compile(r'^\d{1,15}$')
check_origin_id = partial(_check, origin_id_rx)
verify_origin_id = partial(_verify, origin_id_rx)
