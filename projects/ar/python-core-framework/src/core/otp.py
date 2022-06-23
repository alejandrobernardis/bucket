#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-06-06

import base64
import datetime
import hmac
import struct
import time
from abc import ABC, abstractmethod
from functools import partial, cache
from typing import Any, AnyStr, Union, Tuple, Dict, Optional
from urllib.parse import quote, urlencode

from core import random
from core.encoding import want_bytes, want_text

# cache
_digest_cache: Dict = {}

# types
Token = Union[AnyStr, int, None]
TimeStamp = Union[int, float, time.struct_time, datetime.datetime]

# consts
DIGEST: str = 'sha1'
DIGEST_ALLOWED: Tuple = ('sha1', 'sha256', 'sha512')
DIGITS: int = 6
TOKEN_MIN: int = 0
TOKEN_MAX: int = 10 ** DIGITS
GRANULARITY: int = 30
PERIOD_TIMEOUT: int = 180
INIT: int = 1
TRIALS: int = 3
B32ALPHABET: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'


def _get_digest(digest: str) -> Any:
    if digest not in _digest_cache:
        _digest_cache[digest] = getattr(__import__('hashlib'), digest.lower())
    return _digest_cache[digest]


@cache
def _want_int(value: Any) -> int:
    if not isinstance(value, int):
        return int(float(want_text(value)))
    elif isinstance(value, float):
        return int(value)
    return value


def _randomizer(alphabet: str, min_length: int, length: int = 0) -> bytes:
    length = min(256, max(min_length, length))
    return want_bytes(''.join(random.choice(alphabet) for _ in range(length)))


secret_randomizer = partial(_randomizer, B32ALPHABET, 16)


@cache
def secret_sanitizer(secret: AnyStr) -> bytes:
    secret: bytes = want_bytes(secret)
    padding: int = len(secret) % 8
    if padding != 0:
        secret += b'=' * (8 - padding)
    return base64.b32decode(secret, casefold=True)


@cache
def secret_wrapper(secret: AnyStr, width: int = 4, sep: bytes = b' ') -> bytes:
    secret: bytes = want_bytes(secret)
    result: list = []
    while secret:
        result.append(secret[:width])
        secret = secret[width:]
    return sep.join(result)


@cache
def passphrase_encoder(value: AnyStr) -> bytes:
    secret: bytes = base64.b32encode(want_bytes(value))
    return want_bytes(want_text(secret).rstrip('='))


@cache
def token_normalizer(token: Token, digits: int = DIGITS) -> bytes:
    return want_bytes('{{:0{}d}}'.format(digits).format(_want_int(token)))


@cache
def is_token(token: Token) -> bool:
    return TOKEN_MIN < _want_int(token) < TOKEN_MAX


def value_at_time(
    start_time: TimeStamp = None,
    time_step: int = GRANULARITY
) -> int:
    if start_time is None:
        start_time = time.time()
    elif isinstance(start_time, datetime.datetime):
        start_time = start_time.timestamp()
    elif isinstance(start_time, time.struct_time):
        start_time = time.mktime(start_time)
    return int(start_time / time_step)


def compute(secret: AnyStr, times: int, digest: str = DIGEST) -> int:
    d: Any = _get_digest(digest)
    s: bytes = secret_sanitizer(secret)
    h: bytes = hmac.new(s, struct.pack('>Q', times), d).digest()
    offset: int = struct.unpack('B', h[-1:])[0] & 0xF
    truncated: int = struct.unpack('>I', h[offset:offset + 4])[0]
    truncated &= 0x7FFFFFFF
    truncated %= TOKEN_MAX
    return truncated


def compare(
        token: Token,
        secret: AnyStr,
        times: int,
        digest: str = DIGEST
) -> bool:
    return _want_int(token) == compute(secret, times, digest)


def totp(
        secret: AnyStr,
        start_time: TimeStamp = None,
        time_step: int = GRANULARITY,
        digest: str = DIGEST
) -> Tuple[int, int]:
    times: int = value_at_time(start_time, time_step)
    return times, compute(secret, times, digest)


def totp_compare(
        token: Token,
        secret: AnyStr,
        start_time: TimeStamp = None,
        time_step: int = GRANULARITY,
        digest: str = DIGEST
) -> bool:
    cmp: int = totp(secret, start_time, time_step, digest)[1]
    return _want_int(token) == cmp


def totp_verify(
        token: Token,
        secret: AnyStr,
        start_time: TimeStamp = None,
        time_step: int = GRANULARITY,
        timeout: int = PERIOD_TIMEOUT,
        digest: str = DIGEST
) -> bool:
    token = _want_int(token)
    times: int = value_at_time(start_time, time_step)
    units: float = (timeout / GRANULARITY)
    for offset in range(- int((units - 1) / 2), int(units / 2) + 1):
        if token == compute(secret, times + offset, digest):
            return True
    return False


def cotp(
        secret: AnyStr,
        counter: int = None,
        digest: str = DIGEST
) -> Tuple[int, int]:
    counter = max(INIT, counter or INIT)
    return counter, compute(secret, counter, digest)


def cotp_compare(
        token: Token,
        secret: AnyStr,
        counter: int = None,
        digest: str = DIGEST
) -> bool:
    return _want_int(token) == cotp(secret, counter, digest)[1]


def cotp_verify(
        token: Token,
        secret: AnyStr,
        counter: int = None,
        trials: int = TRIALS,
        digest: str = DIGEST
) -> bool:
    counter = max(INIT, counter or INIT)
    for offset in range(max(INIT, counter - trials), counter + trials):
        if cotp_compare(token, secret, offset, digest):
            return True
    return False


class OTP(ABC):

    def __init__(
        self,
        secret: bytes,
        label: Optional[str] = None,
        digest: str = DIGEST,

    ) -> None:
        self._secret: bytes = secret
        self._label: str = label or 'wallet-otp'
        self._digest: str = digest
        self._token: Token = None

    @property
    def secret(self) -> bytes:
        return self._secret

    @property
    def label(self) -> str:
        return self._label

    @property
    def digest(self) -> str:
        return self._digest

    @property
    def token(self) -> Token:
        return self._token

    @abstractmethod
    def compute(self, counter: int = INIT) -> Token:
        pass

    @abstractmethod
    def compare(self, token: Token, *args, **kwargs) -> bool:
        pass

    @abstractmethod
    def verify(self, token: Token, *args, **kwargs) -> bool:
        pass

    def __str__(self) -> str:
        return f'<{self.__class__.__name__} label="{self.label}" ' \
               f'digest="{self.digest}">'

    def __repr__(self) -> str:
        return want_text(self._secret)


class HOTP(OTP):

    def __init__(
            self,
            secret: bytes,
            counter: int = INIT,
            label: Optional[str] = None,
            digest: str = DIGEST

    ) -> None:
        super().__init__(secret, label, digest)
        self._counter: int = counter
        self.current()

    @property
    def counter(self) -> int:
        return self._counter

    def compute(self, counter: int = INIT) -> int:
        self._counter, self._token = cotp(self.secret, counter, self.digest)
        return self.token

    def compare(self, token: Token, **kwargs) -> bool:
        return cotp_compare(token, self.secret, self.counter, self.digest)

    def verify(self, token: Token, trials: int = TRIALS, **kwargs) -> bool:
        return cotp_verify(
            token,
            self.secret,
            self.counter,
            trials,
            self.digest
        )

    def next(self) -> int:
        return self.compute(self.counter + 1)

    def current(self) -> int:
        return self.compute(self.counter)

    def prev(self) -> int:
        return self.compute(self.counter - 1)

    def __str__(self) -> str:
        s: str = super().__str__()[:-1]
        return f'{s} counter="{self.counter}">'


class TOTP(OTP):

    def __init__(
            self,
            secret: AnyStr,
            start_time: TimeStamp = None,
            time_step: int = GRANULARITY,
            label: Optional[str] = None,
            digest: str = DIGEST

    ) -> None:
        super().__init__(secret, label, digest)
        self._start_time: TimeStamp = start_time
        self._time_step: int = time_step
        self.compute()

    @property
    def start_time(self) -> TimeStamp:
        return self._start_time

    @property
    def time_step(self) -> int:
        return self._time_step

    def compute(self, start_time: TimeStamp = None) -> int:
        if start_time is not None:
            self._start_time = start_time
        _, self._token = totp(
            self.secret,
            self.start_time,
            self.time_step,
            self.digest
        )
        return self.token

    def compare(self, token: Token, **kwargs) -> bool:
        return totp_compare(
            token,
            self.secret,
            self.start_time,
            self.time_step,
            self.digest
        )

    def verify(
            self,
            token: Token,
            timeout: int = PERIOD_TIMEOUT,
            **kwargs
    ) -> bool:
        return totp_verify(
            token,
            self.secret,
            self.start_time,
            self.time_step,
            timeout,
            self.digest
        )

    def now(self) -> int:
        return self.compute(time.time())

    def __str__(self) -> str:
        s: str = super().__str__()[:-1]
        return f'{s} start-time="{self.start_time}" ' \
               f'time-step="{self.time_step}">'


def ga_uri_maker(
        label: str,
        issuer: str,
        secret: AnyStr,
        digest: str = DIGEST,
        digits: int = DIGITS,
        counter: Optional[int] = None,
        period: Optional[int] = None

) -> str:
    label = f'{issuer}: ({label})'

    arguments: Dict = {
        'secret': secret,
        'issuer': issuer,
        'algorithm': digest.upper(),
        'digits': digits
    }

    if counter is not None and period is None:
        mode = 'hotp'
        arguments['counter'] = 0 if counter <= 0 else counter
    else:
        mode = 'totp'
        arguments['period'] = 30 if period is None else period

    return f'otpauth://{mode}/{quote(label)}?{urlencode(arguments)}'\
        .replace('+', '%20')


def ga_qr_maker(uri: str, width: int = 300, height: int = 300) -> str:
    return f'https://chart.googleapis.com/chart?cht=qr&chs={width}x{height}' \
           f'&chld=M|0&chl={uri}'


class GooogleMixin:

    def __init__(self, issuer: str):
        self._issuer: str = issuer

    @property
    def issuer(self) -> str:
        return self._issuer

    def provisioning_uri(self) -> str:
        raise NotImplementedError()

    def provisioning_qa(self, width: int = 300, height: int = 300) -> str:
        return ga_qr_maker(self.provisioning_uri(), width, height)


class GHOTP(HOTP, GooogleMixin):

    def __init__(
            self,
            label: str,
            issuer: str,
            secret: bytes,
            counter: int = INIT

    ) -> None:
        super().__init__(secret, counter, label, DIGEST)
        GooogleMixin.__init__(self, issuer)

    def provisioning_uri(self) -> str:
        return ga_uri_maker(
            self.label,
            self.issuer,
            self.secret,
            counter=self.counter
        )


class GTOTP(TOTP, GooogleMixin):

    def __init__(
            self,
            label: str,
            issuer: str,
            secret: AnyStr,
            start_time: TimeStamp = None,
            time_step: int = GRANULARITY

    ) -> None:
        super().__init__(secret, start_time, time_step, label, DIGEST)
        GooogleMixin.__init__(self, issuer)

    def provisioning_uri(self) -> str:
        return ga_uri_maker(
            self.label,
            self.issuer,
            self.secret,
            period=self.time_step
        )
