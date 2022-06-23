#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-04

import os
import pathlib
import sys

from os.path import sep, dirname
from typing import Any

from core.encoding import want_text_list, want_text

__all__ = ['Path', 'want_path', 'is_dangerous_path', 'normalizer',
           'normalize_case', 'module']


class Path(pathlib.Path):
    def __new__(cls, *args, **kwargs):
        if cls is Path:
            cls = pathlib.WindowsPath if os.name == 'nt' else pathlib.PosixPath
        if sys.version_info.minor < 10:
            self = cls._from_parts(args, init=False)
        else:
            self = cls._from_parts(args)
        if not self._flavour.is_supported:
            raise NotImplementedError("Cannot instantiate %r on your system"
                                      % (cls.__name__,))
        if sys.version_info.minor < 10:
            self._init()
        return self

    def as_str(self) -> str:
        return str(self)

    def as_lower(self) -> str:
        return self.as_str().lower()


def want_path(value: Any, absolute: bool = False, exists: bool = False) -> Path:
    if not isinstance(value, Path):
        value = Path(want_text(value))
    if absolute is True:
        value = value.absolute()
    if exists is True and not value.exists():
        raise ValueError(f'Path "{value}" not found.')
    return value


def is_dangerous_path(root: Any, final_path: Any) -> bool:
    root = normalize_case(root)
    final_path = normalize_case(final_path)
    return not final_path.startswith(root + sep) \
        and final_path != root \
        and dirname(root) != root


def normalizer(root: Any, *args) -> Path:
    root = want_path(root, True)
    final_path = root.joinpath(*want_text_list(args))
    if is_dangerous_path(root, final_path):
        raise ValueError('The joined path is located outside of the base path '
                         'component.')
    return final_path


def normalize_case(value: Any, exists: bool = False) -> str:
    return want_path(value, True, exists).as_lower()


def module(value: Any) -> Path:
    path = list(getattr(value, '__path__', []))
    if len(path) == 1:
        return path[0]
    else:
        path = getattr(value, '__file__', None)
        if path is not None:
            return want_path(path, True)
    raise ValueError(f'Cannot determine directory containing "{value}".')
