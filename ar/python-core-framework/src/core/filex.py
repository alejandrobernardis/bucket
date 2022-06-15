#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-06-05

from functools import partial
from typing import Any, Iterator

from core.pathx import Path, want_path

BUFFER_SIZE: int = 1024 * 1024
READ_MODE: str = 'rb'
APPEND_MODE: str = 'ab'
WRITE_MODE: str = 'wb'
CARRIAGE_RETURN: bytes = b'\n'


def _open(mode: str, file_path: Any, **kwargs):
    return want_path(file_path).open(mode, **kwargs)


_reader = partial(_open, READ_MODE)
_writer = partial(_open, WRITE_MODE)
_appender = partial(_open, APPEND_MODE)


def lines_chunk(file_object: Any, buffer_size: int = BUFFER_SIZE) -> Iterator:
    while 1:
        data = file_object.read(buffer_size)
        if not data:
            break
        yield data


def lines_counter(
        file_path: Any,
        buffer_size: int = BUFFER_SIZE,
        **kwargs
) -> int:
    with _reader(file_path, **kwargs) as data:
        return sum(x.count(CARRIAGE_RETURN)
                   for x in lines_chunk(data, buffer_size))


def lines_picker(file_path: Any, max_lines: int = 100, **kwargs) -> Iterator:
    index = 0
    with _reader(file_path, **kwargs) as data:
        while 1:
            line = data.readline()
            index += 1
            if not line or index > max_lines:
                break
            yield index, line


def lines_merger(
        file_path: Any,
        file_output: Any,
        write_mode: str = APPEND_MODE,
        ignore_first_line: bool = False,
        **kwargs
) -> int:
    index = 0
    first_line = False
    with _reader(file_path, **kwargs) as data, \
            _open(file_output, write_mode, **kwargs) as output:
        for line in data:
            if ignore_first_line is True and first_line is False:
                first_line = True
                continue
            output.write(line)
            index += 1
    return index


def chunks_merger(
        file_path: Any,
        file_output: Any,
        write_mode: str = APPEND_MODE,
        buffer_size: int = BUFFER_SIZE,
        ignore_first_line: bool = False,
        **kwargs
) -> int:
    index = 0
    first_line = False
    with _reader(file_path, **kwargs) as data, \
            _open(file_output, write_mode, **kwargs) as output:
        for chunk in lines_chunk(data, buffer_size):
            if ignore_first_line is True and first_line is False:
                chunk = chunk[chunk.find(CARRIAGE_RETURN) + 1:]
                first_line = True
            output.write(chunk)
            index += chunk.count(CARRIAGE_RETURN)
    return index


def touch(
        file_path: Any,
        data: bytes = None,
        mode: int = 0o666,
        exist_ok: bool = True
) -> Path:
    item: Path = want_path(file_path, True)
    item.touch(mode, exist_ok)
    if data:
        item.write_bytes(data)
    return item


def clear(file_path: Any, **kwargs) -> None:
    with _writer(file_path, **kwargs) as _:
        pass
