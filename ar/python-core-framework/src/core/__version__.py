#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-20

__all__ = ['__version__', ]

SEGMENT = 'dev0'
"""Segmento de la versión"""

VERSION = (2021, 11, 5, SEGMENT)
"""Versión en formato de tuple"""

__version__ = '.'.join(map(str, VERSION))
"""Versión en formato de string"""
