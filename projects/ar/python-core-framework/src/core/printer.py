#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-12-27

import sys
from functools import partialmethod, cache
from io import TextIOWrapper
from typing import Callable, Any, Union

from core import json

__all__ = ['Printer', 'WritableObject', 'StdOut', 'StdErr', 'is_writable']


def is_writable(output) -> None:
    if not all([hasattr(output, 'write'), hasattr(output, 'flush')]):
        raise TypeError(f'The object "{output}" does not have the  '
                        f'"write" and/or "flush" methods defined.')


class WritableObject:
    def __init__(self, output: TextIOWrapper, parser: Callable = None) -> None:
        is_writable(output)
        self.__output = output
        self.__parser = parser

    def parse(self, *args, **kwargs) -> Any:
        if self.__parser is None:
            raise NotImplementedError('Parse function is undefined')
        return self.__parser(*args, **kwargs)

    def write(self, *args, **kwargs) -> None:
        value = self.parse(*args, **kwargs)
        if value is not None:
            self.__output.write(value)

    def flush(self) -> None:
        self.__output.flush()


class StdOut(WritableObject):
    def __init__(self, parser: Callable = None) -> None:
        super().__init__(sys.__stdout__, parser)
        self._ = sys.stdout
        sys.stdout = self


class StdErr(WritableObject):
    def __init__(self, parser: Callable = None) -> None:
        super().__init__(sys.__stderr__, parser)
        self._ = sys.stderr
        sys.stderr = self


class Printer:
    def __init__(
            self,
            output: Union[TextIOWrapper, WritableObject] = sys.stdout
    ) -> None:
        is_writable(output)
        self.__output: TextIOWrapper = output

    @cache
    def _builder(
            self,
            *message,
            tmpl: str = None,
            sep: str = ' ',
            end: str = None,
            endx: int = None,
            prex: str = '',
            subx: str = '',
            tab: int = 0,
            **kwargs
    ) -> str:
        msg = tmpl.format(*message) if tmpl is not None \
            else sep.join([str(x) for x in message])
        for x in ('lower', 'upper', 'title', 'capitalize', 'swapcase'):
            if kwargs.get(x, False) is True:
                msg = getattr(msg, x)()
                break
        msg = f'{prex}{msg}{subx}'
        if end is None:
            end = '\n'
        if endx is None:
            endx = 1
        if end and endx and not msg.endswith(end):
            msg = f'{msg}{end * max(1, endx)}'
        return f'{" " * tab}{msg}'

    def write(self, *message, **kwargs) -> None:
        value = self._builder(*message, **kwargs)
        value and self.__output.write(value)

    def flush(self, *message, **kwargs) -> None:
        if message:
            self.write(*message, **kwargs)
        self.__output.flush()

    def done(self) -> None:
        self.flush('Done')

    def blank(self) -> None:
        self.flush('')

    def rule(self, size=1, char='-') -> None:
        self.flush(char * max(1, size or 1))

    def header(self, *message, **kwargs) -> None:
        self.blank()
        self.write(*message, **kwargs)
        self.rule(2)

    def footer(self, *message, **kwargs) -> None:
        self.blank()
        self.rule(2)
        self.write(*message, **kwargs)
        self.blank()

    def json(self, value: dict, indent: int = 2) -> None:
        @cache
        def _parser(v: dict, i: int):
            return json.dumps(v, indent=i, default=str) \
                if isinstance(v, dict) else '-'
        self.__output.write(_parser(value, indent) + '\n')
        self.flush()

    error = partialmethod(write, prefix='(E) ')
    question = partialmethod(write, subffix='?')
    bullet = partialmethod(write, prefix='> ')

    def __call__(self, *args, **kwargs) -> None:
        self.flush(*args, **kwargs)
