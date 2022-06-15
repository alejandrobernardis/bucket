#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-12-27

from typing import Any, Optional, Callable

from core.cli import doc_options
from core.dotted.collection import DottedDict
from core.encoding import want_text
from core.printer import Printer

EXIT_ERROR: int = 1
ABORT_ERROR: int = 2
COMMAND_ERROR: int = 7


def want_name(value: Any) -> str:
    if hasattr(value, '__name__'):
        value = value.__name__
    return want_text(value)


class Command:
    _printer: Optional[Printer] = None
    _commands: Optional[DottedDict] = None

    @classmethod
    def register(cls, cmd: 'Command') -> None:
        if Command._commands is None:
            Command._commands = DottedDict()
        cls._commands[cmd.name] = cmd

    @classmethod
    def run(cls, opts: dict, **kwargs) -> int:
        try:
            if Command._printer is None:
                Command._printer = Printer()
            if Command._commands is None:
                raise Exit('No commands available')
            name: str = opts['COMMAND']
            if name not in Command._commands:
                raise NoSuchCommand(name)
            cfg = kwargs.pop('global_config')
            cmd = Command._commands[name]
            cmd_args: list = opts['ARGS']
            kwargs.setdefault('options_first', True)
            cmd_opts, _ = doc_options(cmd, cmd_args, **kwargs)
            cmd_opts.setdefault('attrs', cmd.attributes)
            cmd_opts['global_config'] = cfg
            cmd(**{k.lower().replace('-', ''): v for k, v in cmd_opts.items()})
            return 0
        except CommandError as e:
            return e.command.prune()
        except (NoSuchCommand, Exit, EOFError) as e:
            Command._printer.error(e)
            return EXIT_ERROR
        except (KeyboardInterrupt, Abort):
            Command._printer.write('Abort')
            return ABORT_ERROR

    def __init__(self, name, callback, **kwargs) -> None:
        self._name: str = want_name(name or callback)
        self._callback: Callable = callback
        self._attributes: dict = kwargs
        self.__doc__ = callback.__doc__
        Command.register(self)

    @property
    def name(self) -> str:
        return self._name

    @property
    def callback(self) -> Callable:
        return self._callback

    @property
    def attributes(self) -> dict:
        return self._attributes

    def prune(self) -> int:
        return COMMAND_ERROR

    def __call__(self, *args, **kwargs) -> Any:
        return self._callback(*args, **kwargs)


def run(obj: Any, config=None, **kwargs) -> int:
    opts, _ = doc_options(obj, **kwargs)
    return Command.run(opts, global_config=config, **kwargs)


def run_opts(opts: dict, **kwargs) -> int:
    return Command.run(opts, **kwargs)


def command(name=None, **attrs) -> Callable:
    def decorator(f):
        return Command(name, f, **attrs)
    return decorator


class CommandError(Exception):
    def __init__(self, message: str,  target: Command) -> None:
        super().__init__(message)
        self.command: Command = target


class NoSuchCommand(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(f'Command `{name}` not found.')


class Exit(SystemExit):
    pass


class Abort(RuntimeError):
    pass
