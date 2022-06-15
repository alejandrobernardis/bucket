#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-03-31

from abc import ABC
from threading import Lock
from typing import Union

from core.patterns import Manager

__all__ = ['CounterABC', 'Counter', 'Gauge', 'CounterManager']


class CounterABC:

    def __init__(
            self,
            name: str,
            factor: float = 1,
            reset: float = 0
    ) -> None:
        """
        Objeto base.

        :param name: nombre del contador
        :param factor: factor de incremento
        :param reset: valor de reseteo
        """

        self.__name: str = name
        self._factor: float = factor
        self._reset: float = reset
        self._counter: float = reset

    @property
    def name(self) -> str:
        """
        Nombre del contador.

        :return: str
        """

        return self.__name

    @property
    def raw(self) -> float:
        """
        Valor actual de contador.

        :return: float
        """
        return self._counter

    def reset(self) -> None:
        """
        Reinicia el contador con el valor de referencia definido
        en el constructor.

        :return: None
        """
        self._counter = self._reset

    def __str__(self) -> str:
        return f'<{self.__class__.__name__} {self.name}="{self.raw}">'

    def __repr__(self) -> str:
        return f'{self.raw}'

    def __eq__(self, other: float) -> bool:
        return self.raw == other

    def __gt__(self, other: float) -> bool:
        return self.raw > other

    def __ge__(self, other: float) -> bool:
        return self.raw >= other

    def __lt__(self, other: float) -> bool:
        return self.raw < other

    def __le__(self, other: float) -> bool:
        return self.raw <= other

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class Counter(CounterABC, ABC):

    def add(self, value: float) -> float:
        """
        Agrega al contador el valor pasado como argumento y lo múltiplica por
        el factor definido.

        >>> value * self._factor

        :param value: valor de referencia.
        :return: float
        """

        self._counter += value * self._factor

        return self._counter

    def increment(self) -> float:
        """
        Incrementa el valor del contador.

        :return: float
        """

        return self.add(1)


class Gauge(Counter, ABC):

    def sub(self, value: float) -> float:
        """
        Quita del contador el valor pasado como argumento y lo múltiplica por
        el factor definido.

        >>> value * self._factor * -1

        :param value: valor de referencia.
        :return: float
        """

        return self.add(-value)

    def decrement(self) -> float:
        """
        Decrementa el valor del contador.

        :return: float
        """

        self._counter -= self._factor
        return self._counter

    def set(self, value: float) -> float:
        """
        Establece como absoluto el valor pasado como argumento, en este caso
        no se multiplica por el factor.

        :return: float
        """

        self._counter = value

        return self._counter


class CounterManager(Manager):
    def __init__(self, name: str, *args) -> None:
        values: dict = {getattr(x, 'name'): x for x in args} \
            if args else {}
        super().__init__(name, values)

    def register(self, counter: CounterABC) -> CounterABC:
        """
        Registra un nuevo contador.

        :param counter: contador de referencia.
        :return: CounterABC
        """

        self._register(counter.name, counter)

        return counter

    def unregister(self, key: Union[CounterABC, str]) -> bool:
        """
        Elimina del registro un contador específico.

        :param key: nombre o referencia del contador.
        :return: CounterABC
        """

        if isinstance(key, CounterABC):
            key = key.name

        return self._unregister(key)


class Stats:
    def __init__(self, name: str):
        """
        Contador sincronizado.

        :param name: Nombre del contador
        """

        self._name: str = name
        self._lock: Lock = Lock()
        self._value: float = 0

    def add(self, value: float) -> float:
        """
        Agrega el valor pasado como argumento al contador.

        :param value: valor de referencia.
        :return: float
        """

        return self.set(self._value + value)

    def sub(self, value: float) -> float:
        """
        Remueve el valor pasado como argumento al contador.

        :param value: valor de referencia.
        :return: float
        """

        return self.add(-value)

    def increment(self) -> float:
        """
        Incrementa el contador.

        :return: float
        """

        return self.add(1)

    def decrement(self) -> float:
        """
        Decrementa el contador.

        :return: float
        """

        return self.add(-1)

    def set(self, value: float) -> float:
        """
        Estable como valor absoluto el valor pasado como argumento.

        :param value: valor de referencia.
        :return: float
        """

        with self._lock:
            self._value = value

        return self._value

    @property
    def name(self) -> str:
        """
        Nombre del contador.

        :return: str
        """

        return self._name

    @property
    def value(self) -> float:
        """
        Valor del contador.

        :return: float
        """

        with self._lock:
            return self._value
