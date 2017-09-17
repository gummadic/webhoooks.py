import argparse
import asyncio
import os
import sys

from aiohttp.web import run_app

from .app import Application
from .loaders import YamlLoader


async def start_app(loop, options):
    config = os.path.abspath(options.config)
    loader = YamlLoader(config)
    app = Application(loop=loop)

    return app


def main():
    parser = argparse.ArgumentParser(description='Start a webhook service.')
    parser.add_argument('config', help='Configuration file')
    parser.add_argument('-p', '--port', type=int, default=3000, help='the port to listen on')
    parser.add_argument('-i', '--interface', default="127.0.0.1", help='the interface to listen on')

    options = parser.parse_args()
    config_path = os.path.abspath(options.config)

    if not os.path.exists(config_path):
        sys.stderr.write(f'Config path {options.config} does not exists\n')
        exit(1)

    loop = asyncio.get_event_loop()

    try:
        app = loop.run_until_complete(start_app(loop, options))
        run_app(app, host=options.interface, port=options.port)
    finally:
        if not loop.is_closed():
            loop.stop()
            loop.run_forever()
            loop.close()
