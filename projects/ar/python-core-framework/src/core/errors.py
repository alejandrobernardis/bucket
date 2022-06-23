#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-07

__all__ = ['BaseError', 'InvalidFormatError', 'InvalidLengthError',
           'InvalidChecksumError', 'MustBeStrError', 'MustBeDictError',
           'DEFAULT_ERROR']

DEFAULT_ERROR: int = -1


class BaseError(Exception):

    def __str__(self):
        return f'[{self.raw_code}] {self.raw_message}'

    def __repr__(self):
        return '<{name} code="{code}" message="{message}">'\
            .format(**self.to_dict())

    @property
    def raw_code(self) -> int:
        return ''.join(self.args[:1]) or getattr(self, 'code', DEFAULT_ERROR)

    @property
    def raw_message(self) -> int:
        return getattr(self, 'message', '')

    def to_dict(self) -> dict:
        return {
            'name': self.__class__.__name__,
            'code': self.raw_code,
            'message': self.raw_message
        }


class InvalidFormatError(BaseError):

    message = 'Value has an invalid format'


class InvalidLengthError(BaseError):

    message = 'Value has an invalid length'


class InvalidChecksumError(BaseError):

    message = "Value's checksum or check digit is invalid"


class MustBeStrError(BaseError):

    message = 'Value must be a string'


class MustBeDictError(BaseError):

    message = 'Value must be a dictionary'
