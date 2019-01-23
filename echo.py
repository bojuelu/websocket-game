import asyncio
import threading
import logging

import tornado.web
import tornado.websocket
import tornado.ioloop


class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        super(WebSocketHandler, self).__init__(application, request, **kwargs)
        pass

    def open(self):
        self.set_nodelay(True)
        logging.debug('open()')
        self.write_message("open")

    def on_message(self, message):
        logging.debug('on_message() {}'.format(message))
        self.write_message(message, True)

    def on_close(self):
        logging.debug('on_close()')


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


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET)

    # create websocket application
    ws_app = Application()
    ws_thread = threading.Thread(target=start_server, args=(ws_app, ))
    ws_thread.daemon = True
    ws_thread.start()
    logging.debug('websocket app start')

    ws_thread.join()
