import json

from aiohttp import web
from aiohttp.web_ws import WebSocketResponse

from .renderer import HtmlDoc
from .tail import AsyncTail


async def websocket_handler(request):
    resp = WebSocketResponse()
    await resp.prepare(request)

    async with AsyncTail(filepath=request.app['filepath']) as atail:
        async for line in atail:
            resp.send_str(json.dumps({
                'action': 'sent',
                'text': line
            }))

    resp.send_str(json.dumps({
        'action': 'close',
    }))

    await resp.close()

    return resp


class Application(web.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.router.add_get('/', self.index)

    async def index(self, request):
        doc, tag, text = HtmlDoc().tagtext()

        with tag('html'):
            with tag('header'):
                doc.stag("meta", name="charset", width="utf-8")
                doc.stag("meta", name="viewport", width="device-width, initial-scale=1")

                with tag('style'):
                    doc.asis(
                        'html{-ms-text-size-adjust:100%;-webkit-text-size-adjust:100%}'
                        'body {font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",'
                        '"Roboto", "Droid Sans", "Helvetica Neue", Helvetica, Arial, sans-serif; '
                        'font-size: 12px; margin: 0}'
                        'h1, h2, h3 {font-size: 1.5rem; line-height: 1.5; margin: 0}'
                        '[hidden],.hidden]{display:none}')

            with tag('body'):
                with tag('h1'):
                    text('Hello world!')

        return web.Response(text=doc.render(), content_type='text/html')
