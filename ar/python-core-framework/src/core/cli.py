#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-20

from inspect import getdoc

from docopt import docopt

__all__ = ['doc_options', 'doc_string']


def doc_string(obj, tmpl='{}') -> str:
    """
    Retorna la documentación definida para un objeto.

    :param obj: objeto de referencia
    :param tmpl: string con el formato de retorno, en caso de valer `None`
                 retorna el string crudo del objeto.
    :return: str
    """

    if not isinstance(obj, str):
        obj = getdoc(obj)

    if tmpl is not None:
        return tmpl.format(obj)

    return obj


def doc_options(obj, *args, **kwargs) -> tuple[dict, str]:
    """
    Crea una instancia de `docopt` y retorna una tupla con la instancia creada
    y el string de documentación.

    :param obj: objeto de referencia
    :param args: argumentos opcionales
    :param kwargs: argumentos key-value opcionales
    :return: tuple[dict, str]
    """

    obj = doc_string(obj)

    return docopt(obj, *args, **kwargs), obj
