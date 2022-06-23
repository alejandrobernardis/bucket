#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-13

import logging

from core.ar import cbu, cuit, dni
from core.schemas import client_id_rx, check_client_id, cxu_alias_rx, \
    check_cxu_alias, origin_id_rx, check_origin_id

__all__ = ['CXU', 'CVU', 'CBU', 'CUIT', 'CXUAlias', 'CVUAlias', 'CBUAlias',
           'ClientID', 'OriginID', 'DNI', 'LogLevel']


class _Str(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        raise NotImplementedError()

    @classmethod
    def validate(cls, v):
        raise NotImplementedError()

    def __repr__(self):
        return f'{self.__class__.__name__}({super().__repr__()})'


class CXU(_Str):

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(pattern=cbu.cbu_rx.pattern,
                            example='2850590940090418135201')

    @classmethod
    def validate(cls, v):
        return cls(cbu.check(v))


CBU = CXU
CVU = CXU


class CXUAlias(_Str):

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(pattern=cxu_alias_rx.pattern,
                            example=['cbu-alias-example',
                                     'cbu.alias.example',
                                     'cbu.alias-example'])

    @classmethod
    def validate(cls, v):
        return check_cxu_alias(v) and cls(v)


CBUAlias = CXUAlias
CVUAlias = CXUAlias


class DNI(_Str):

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(pattern=dni.dni_rx.pattern,
                            example=['7.321.654', '7321654'])

    @classmethod
    def validate(cls, v):
        return cls(dni.check(v))


class CUIT(_Str):

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(pattern=cuit.cuit_rx.pattern,
                            example=['20-05536168-2', '20055361682'])

    @classmethod
    def validate(cls, v):
        return cls(cuit.check(v))


class ClientID(_Str):

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(pattern=client_id_rx.pattern,
                            example=['1234567', '123456789012'])

    @classmethod
    def validate(cls, v):
        return check_client_id(v) and cls(v)


class OriginID(_Str):

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(pattern=origin_id_rx.pattern,
                            example=['1234567', '123456789012345'])

    @classmethod
    def validate(cls, v):
        return check_origin_id(v) and cls(v)


class LogLevel(_Str):
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(pattern=r'^[a-zA-Z]$',
                            example=['DEBUG', 'INFO', 'WARNING'])

    @classmethod
    def validate(cls, v):
        return logging.getLevelName(v) and cls(v)
