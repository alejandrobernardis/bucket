#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-03

from functools import partial, cache
from io import StringIO, BytesIO
from typing import Callable, Iterator, Union, Any, Iterable, Optional


from core import constants as ct, json
from core.dotted.collection import DottedDict
from core.errors import MustBeDictError
from core.tools import flatten

__all__ = ['want_bytes', 'want_text', 'want_bytes_flatten', 'want_text_flatten',
           'want_bytes_list', 'want_text_list', 'base36', 'sanitizer',
           'defaults']

B36ALPHABET: str = '0123456789abcdefghijklmnopqrstuvwxyz'


def _want_list(
        f: Callable,
        values: Union[tuple, list, set, frozenset],
        **kwargs
) -> Iterator:
    if values is None:
        return None
    if kwargs.pop('flatten', False) is True:
        values = flatten(values)
    for value in values:
        yield f(value, **kwargs)


def want_bytes(
        value: Any,
        encoding: str = ct.UTF8,
        errors: str = ct.STRICT
) -> bytes:
    if isinstance(value, bytes):
        return value if encoding == ct.UTF8 \
            else value.decode(ct.UTF8, errors).encode(encoding, errors)
    if isinstance(value, memoryview):
        return bytes(value)
    if isinstance(value, StringIO):
        value = value.read()
    return str(value).encode(encoding, errors)


want_bytes_list = partial(_want_list, want_bytes)
want_bytes_flatten = partial(_want_list, want_bytes, flatten=True)


def want_text(
        value: Any,
        encoding: str = ct.UTF8,
        errors: str = ct.STRICT
) -> str:
    if issubclass(type(value), str):
        return value
    if isinstance(value, (bytes, BytesIO)):
        if isinstance(value, BytesIO):
            value = value.read()
        return str(value, encoding, errors)
    if isinstance(value, StringIO):
        return value.read()
    return str(value)


want_text_list = partial(_want_list, want_text)
want_text_flatten = partial(_want_list, want_text, flatten=True)


# dict

def raw_dict(value: Any) -> Union[dict]:
    if value is not None:
        if not isinstance(value, (dict, DottedDict)):
            raise MustBeDictError()
        if isinstance(value, DottedDict):
            return value.to_python()
    return value


# base 36

@cache
def base36(value: int, default: str = '0') -> str:
    if value < 0:
        return f'-{base36(-value)}'
    result: str = ''
    while not result or value > 0:
        value, index = divmod(value, 36)
        result = B36ALPHABET[index] + result
    return result or default


# sanitizer

def sanitizer(chunk: Any, f: Optional[Callable] = None, **kwargs) -> Any:
    if isinstance(chunk, Iterable) and not isinstance(chunk, ct.TEXT_TYPE):
        if isinstance(chunk, DottedDict):
            chunk = chunk.to_python()
        if isinstance(chunk, dict):
            return dict((k, sanitizer(v, f, **kwargs))
                        for k, v in chunk.items())
        return list(sanitizer(v, f, **kwargs) for v in chunk)
    if isinstance(chunk, (int, float, bool)):
        return chunk
    if kwargs.get('strftime', False) and hasattr(chunk, 'strftime'):
        return chunk.strftime(kwargs['strftime'])
    if kwargs.get('isoformat', False) and hasattr(chunk, 'isoformat'):
        return chunk.isoformat()
    if isinstance(chunk, str) and chunk.startswith('{\"'):
        return json.loads(chunk)
    return f(chunk) if callable(f) else chunk


def defaults(value: Any) -> Any:
    if hasattr(value, 'isoformat'):
        return value.isoformat()
    if isinstance(value, DottedDict):
        return value.to_python()
    return value
