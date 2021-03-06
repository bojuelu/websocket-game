import asyncio
import threading
import logging

import tornado.web
import tornado.websocket
import tornado.ioloop

from utility.misc import WebsocketGlobalArgs
from mygame.cmd_router import CmdRouter
from mygame.game import Game


class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        super(WebSocketHandler, self).__init__(application, request, **kwargs)
        self.socket_id = WebsocketGlobalArgs.SOCKET_ID
        WebsocketGlobalArgs.SOCKET_ID += 1

        for func in WebsocketGlobalArgs.event_websocket_init:
            func(self)

    def open(self):
        # self.set_nodelay(True)
        WebsocketGlobalArgs.websockets[self.socket_id] = self

        for func in WebsocketGlobalArgs.event_websocket_open:
            func(self)

    def on_message(self, message):
        for func in WebsocketGlobalArgs.event_websocket_onmessage:
            func(self, message)

    def on_close(self):
        WebsocketGlobalArgs.websockets.pop(self.socket_id)

        for func in WebsocketGlobalArgs.event_websocket_onclose:
            func(self)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/websocket', WebSocketHandler)
        ]

        settings = {
            'template_path': 'templates'
        }
        tornado.web.Application.__init__(self, handlers, **settings)

    def run(self, port=8080):
        self.listen(port)
        tornado.ioloop.IOLoop.instance().start()


def start_server(app):
    asyncio.set_event_loop(asyncio.new_event_loop())
    app.run()


def start_game(game):
    asyncio.set_event_loop(asyncio.new_event_loop())
    game.run()
    pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET)

    # create websocket application
    ws_app = Application()
    ws_thread = threading.Thread(target=start_server, args=(ws_app, ))
    ws_thread.daemon = True
    ws_thread.start()
    logging.debug('websocket app start')

    # create cmd router
    cmd_router = CmdRouter()
    cmd_router.listen_websocket_events()

    # create game entry
    mygame = Game(cmd_router)
    mygame.listen_websocket_events()
    mygame_thread = threading.Thread(target=start_game, args=(mygame, ))
    mygame_thread.daemon = True
    mygame_thread.start()

    ws_thread.join()
    mygame_thread.join()
