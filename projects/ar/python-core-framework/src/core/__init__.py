#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-20

from secrets import SystemRandom

from core.__version__ import __version__

ins = isinstance
"""Alias de `isinstance`"""

random: SystemRandom = SystemRandom()
"""Instancia global de SystemRandom"""


try:
    import orjson as json

except ImportError:
    try:
        import ujson as json

    except ImportError:
        try:
            import simplejson as json

        except ImportError:
            import json


__all__ = ['json', 'random', 'ins', '__version__']

