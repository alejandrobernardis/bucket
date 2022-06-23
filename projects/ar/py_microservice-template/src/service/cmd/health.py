#!/usr/bin/env python

from core.command import command

from service.cmd.base import show_response

__all__ = ['ping', 'health', 'uptime', 'counters']


@command()
def ping(**kwargs) -> None:
    """
    Retorna `Pong` si el servicio se encuentra disponible.

    usage:
      uptime [--help] [-i|--header]

    Arguments:
      -i --header    Show request header.
    """

    show_response('ping', **kwargs)


@command()
def health(**kwargs) -> None:
    """
    Retorna el `estado` del servicio.

    usage:
      health [--help] [-i|--header]

    Arguments:
      -i --header    Show request header.
    """

    show_response('health', **kwargs)


@command()
def uptime(**kwargs) -> None:
    """
    Retorna el `tiempo de actividad` del servicio.

    usage:
      uptime [--help] [-i|--header]

    Arguments:
      -i --header    Show request header.
    """

    show_response('uptime', **kwargs)


@command()
def counters(**kwargs) -> None:
    """
    Retorna los `contadores` del servicio.

    usage:
      uptime [--help] [-i|--header]

    Arguments:
      -i --header    Show request header.
    """

    show_response('counters', **kwargs)


@command()
def config(**kwargs) -> None:
    """
    Retorna la `configuración` del servicio.

    usage:
      config [--help] [-i|--header]
    """

    show_response('config', **kwargs)
