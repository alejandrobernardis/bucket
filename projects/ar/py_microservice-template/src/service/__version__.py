#!/usr/bin/env python

__all__ = ['__version__', ]

SEGMENT = 'dev0'
"""Segmento de la versión"""

VERSION = (1, 0, 0, SEGMENT)
"""Versión en formato de tuple"""

__version__ = '.'.join(map(str, VERSION))
"""Versión en formato de string"""
