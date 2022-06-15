#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-03

import builtins
from functools import partial
from typing import Union, Iterator, Sequence, Any

from core import constants as ct

__all__ = ['flatten', 'dict_picker', 'list_picker', 'nested_get', 'printr',
           'primitives']


def flatten(value: Union[list, tuple, set]) -> Iterator:
    for x in value:
        if isinstance(x, ct.LIST_TYPE):
            for y in flatten(x):
                yield y
        else:
            yield x


def dict_picker(keys: Sequence[str], value: dict) -> dict:
    return {k: v for k, v in value.items() if k in keys}


def list_picker(keys: Sequence[int], value: Any) -> list:
    return [value[x] for x in range(len(value)) if x in keys]


def nested_get(key: Any, values: Any, lazy: bool = False) -> Any:
    if isinstance(key, ct.LIST_TYPE):
        return (nested_get(x, values, lazy) for x in key) if lazy is True \
            else [nested_get(x, values, lazy) for x in key]
    return values[key]


printr = partial(print, end='\r', flush=True)
primitives = frozenset(filter(lambda x: not x.startswith('_'), dir(builtins)))
