#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-03

import os
import time
from functools import cache

from core import random
from core.encoding import base36
from core.patterns import Manager

__all__ = ['CUID', 'CUIDManager']

BASE: int = 36
BLOCK_SIZE: int = 4
DISCRETE_VALUES: int = BASE ** BLOCK_SIZE
LETTER: str = 'a'
ZERO: str = '0'


@cache
def _pad(value: str, length: int = 9, char: str = ZERO) -> str:
    return value.rjust(length, char)[-length:]


@cache
def _make_fingerprint(pid: int, hostname: str) -> str:
    length: int = 2
    p: str = _pad(base36(pid), length)
    h: str = _pad(base36(sum(hostname.encode()) + len(hostname) + BASE), length)
    return f'{p}{h}'


def _fingerprint() -> str:
    return _make_fingerprint(os.getpid(), os.uname().nodename)


def _random_block() -> str:
    return _pad(base36(random.getrandbits(24)), BLOCK_SIZE)


def _milliseconds() -> str:
    return base36(int(time.time() * 1000))


class CUID:
    def __init__(self, fingerprint: str = None) -> None:
        self._fingerprint: str = _fingerprint() if fingerprint is None \
            else _pad(base36(sum(fingerprint.encode())), 4)
        self._counter: int = 0

    @property
    def fingerprint(self) -> str:
        return self._fingerprint

    def increment(self) -> str:
        self._counter += 1
        if self._counter >= DISCRETE_VALUES:
            self._counter = 0
        return _pad(base36(self._counter - 1), BLOCK_SIZE)

    def make(self) -> str:
        return ''.join({
            LETTER,
            _milliseconds(),
            self.increment(),
            self.fingerprint,
            _random_block(),
            _random_block()
        })

    def slug(self) -> str:
        return ''.join([
            _milliseconds()[-2:],
            self.increment(),
            self.fingerprint[0],
            self.fingerprint[-1],
            _random_block()[-2:]
        ])


class CUIDManager(Manager):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, kwargs)

    def register(self, key: str, generator: CUID) -> CUID:
        self._register(key, generator)
        return generator

    def unregister(self, key: str) -> bool:
        return self._unregister(key)
