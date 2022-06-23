#!/usr/bin/env python

import asyncio
import json
from functools import cache
from typing import Union

from aiohttp.client import ClientSession, InvalidURL
from aiohttp.web import HTTPException
from core.encoding import defaults
from core.printer import Printer
from yarl import URL

__all__ = ['get_url', 'show_header', 'show_response']

pt = Printer()


@cache
def get_url(path: Union[str, URL, list, tuple], url: str, port: int) -> str:
    # TODO(berna): dale soporta para determinar el protocolo (http, https)
    return (URL(f'http://{url}:{port}') / path).human_repr()


def show_header(rsp) -> None:
    pt.blank()
    for k, v in rsp.headers.items():
        pt.write(f'{k}: {v}')
    pt.rule()


async def _show_response(url: str, method: str = 'GET', **kwargs) -> None:
    hdr = kwargs.pop('header', False)
    cfg = kwargs.pop('global_config', {})
    hcl = kwargs.pop('http_client', {})
    url = get_url(url, cfg.container.host, cfg.container.port)
    try:
        async with ClientSession(**hcl) as sss:
            async with sss.request(method, url) as rsp:
                if hdr is True:
                    show_header(rsp)
                ret = await rsp.json()
                pt.write(json.dumps(
                    ret,
                    indent=2,
                    sort_keys=True,
                    default=defaults
                ))
    except InvalidURL:
        pt.error(f'Invalid URL: {url}')
    except HTTPException as e:
        pt.error(f'Client Error: {e}')
    except Exception as e:
        pt.error(f'Uncontrolled Error: {e}')


def show_response(url: str, method: str = 'GET', **kwargs) -> None:
    asyncio.run(_show_response(url, method, **kwargs))
