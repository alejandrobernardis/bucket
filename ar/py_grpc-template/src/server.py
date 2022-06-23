import asyncio
import logging
import os

import grpc.aio
import sentry_sdk
from dotenv import dotenv_values
from grpc_reflection.v1alpha import reflection
# from sentry_sdk.integrations.aiohttp import AioHttpIntegration

# noinspection PyUnresolvedReferences
# https://www.jetbrains.com/help/pycharm/disabling-and-enabling-inspections.html#comments-ref
import fix  # <<< NO BORRAR, REPARA SYS.PATH
import common_pb2
import common_pb2_grpc
import health_pb2
import health_pb2_grpc
from service.common import CommonApi
from service.health import HealthApi

_cleanup_coroutines = []


async def server() -> None:

    srv = grpc.aio.server()

    common_pb2_grpc.add_CommonServiceServicer_to_server(CommonApi(), srv)
    health_pb2_grpc.add_HealthServiceServicer_to_server(HealthApi(), srv)

    services = [
        common_pb2.DESCRIPTOR.services_by_name['CommonService'].full_name,
        health_pb2.DESCRIPTOR.services_by_name['HealthService'].full_name,
        reflection.SERVICE_NAME,
    ]

    reflection.enable_server_reflection(services, srv)

    lst = f'{cfg.get("CFG_GRPC_HOST", "[::]")}' \
          f':{cfg.get("CFG_GRPC_PORT", 50051)}'

    srv.add_insecure_port(lst)
    await srv.start()

    logging.debug('Start -> %s', lst)

    async def graceful_shutdown():
        await srv.stop(5)

    _cleanup_coroutines.append(graceful_shutdown())
    await srv.wait_for_termination()


if __name__ == '__main__':

    cfg = {**dotenv_values(os.environ.get('ENV_FILE', '/app/.env'))}

    if not cfg:
        cfg.update(dotenv_values('../../.env'))

    logging.basicConfig(level=int(cfg.get('CFG_LOG_LEVEL', logging.DEBUG)))
    logging.debug(cfg)

    sentry_sdk.init(
      dsn=cfg.CFG_SENTRY_CNXSTR,
      # integrations=[AioHttpIntegration()]
    )

    loop = asyncio.get_event_loop()

    try:
        try:
            loop.run_until_complete(server())
        except KeyboardInterrupt:
            pass

    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()
