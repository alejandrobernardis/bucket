#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-03

NONE_TYPE = type(None)
TEXT_TYPE: tuple = (str, bytes, NONE_TYPE)
LIST_TYPE: tuple = (list, tuple, set, frozenset)
DATA_TYPE: tuple = (dict,) + LIST_TYPE
NUMBER_TYPE: tuple = (int, float)

# misc
DOT: str = '.'
COLON: str = ','
HYPHEN: str = '-'
PLUS: str = '+'
SEMICOLON: str = ':'
SLASH: str = '/'
BACKSLASH: str = '\\'
STRICT: str = 'strict'
EMPTY = object()
EMPTY_STRING: str = ''
EMPTY_BYTES: bytes = b''
LOCALHOST: str = 'localhost'
LOCALHOST_LOCAL: str = 'localhost.local'
LOCALIP: str = '127.0.0.1'

# encoding
ASCII: str = 'ascii'
UTF8: str = 'utf-8'
CP1252: str = 'cp1252'
LATIN1: str = 'latin-1'
ENCODING: str = UTF8

# all in seconds
SECONDS_PER_MINUTE: int = 60
SECONDS_PER_HOUR: int = 60 * 60
SECONDS_PER_DAY: int = 60 * 60 * 24
SECONDS_PER_WEEK: int = SECONDS_PER_DAY * 7
SECONDS_PER_MONTH: int = SECONDS_PER_WEEK * 4
MINUTE: int = SECONDS_PER_MINUTE
HOUR: int = SECONDS_PER_HOUR
