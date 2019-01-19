
class WebsocketGlobalArgs(object):
    SOCKET_ID = 0

    websockets = {}  # socket_id: WebsocketHandler

    event_websocket_init = []  # function(WebsocketHandler)
    event_websocket_open = []  # function(WebsocketHandler)
    event_websocket_onmessage = []  # function(WebsocketHandler, message)
    event_websocket_onclose = []  # function(WebsocketHandler)
