#!/usr/bin/env python

import sys

from core.config import load_env_files
from core.dotted.collection import DottedDict

from service.__version__ import __version__
from service.cmd import run
from service.config import ConfigModel


def main() -> None:
    """
    usage:
      cli [--help] [--version] COMMAND [ARGS...]
    
    Arguments:
      -h --help     Show command `help` and exit.
      -v --version  Show command `version` and exit.
    
    Commands:
      config     Retorna lo `configuración` del servicio (only debug mode on).
      counters   Retorna los `contadores` del servicio.
      health     Retorna el `estado` del servicio.
      ping       Retorna `Pong` si el servicio se encuentra disponible.
      uptime     Retorna el `tiempo de actividad` del servicio.
    
    --
    See `cli <command> --help` for more information on a specific command.
    """

    cfg = DottedDict(ConfigModel.parse_obj(load_env_files()).dict())
    
    sys.exit(run(main, cfg, version=__version__, options_first=True))


if __name__ == '__main__':
    main()
