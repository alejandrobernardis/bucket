#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-03-31

from typing import Any, ValuesView, AbstractSet

from core.dotted.collection import DottedDict

__all__ = ['Manager', ]


class Manager:
    def __init__(self, name: str, initial: dict = None) -> None:
        self._name: str = name
        self._objects: DottedDict = DottedDict()
        if isinstance(initial, dict):
            for key, value in initial.items():
                self._objects[key] = value

    @property
    def name(self) -> str:
        return self._name

    def _register(self, key: str, value: Any = None) -> None:
        if any([not key, not key.strip()]):
            raise ValueError('Can\'t register object with a blank name.')
        elif key in self._objects:
            if isinstance(self._objects[key], DottedDict):
                raise KeyError(f'Can\'t register object with name "{key}" '
                               f'because a namespace with the same name was '
                               f'previously registered.')
            raise KeyError(f'Can\'t register object with name "{key}" because '
                           f'an object with the same name was previously '
                           f'registered.')
        self._objects[key] = value

    def _unregister(self, key: str) -> bool:
        if key in self._objects:
            del self._objects[key]
            return True
        return False

    def keys(self) -> AbstractSet:
        return self._objects.keys()

    def values(self) -> ValuesView:
        return self._objects.values()

    def items(self) -> AbstractSet:
        return self._objects.items()

    def get(self, key: str) -> Any:
        return self._objects[key]

    __getitem__ = get

    __getattr__ = get

    def has(self, key: str) -> bool:
        return key in self._objects

    __contains__ = has

    def count(self) -> int:
        return len(self._objects)

    def clear(self) -> None:
        self._objects and self._objects.clear()
