
class Misc(object):
    SOCKET_ID = 0

    websockets = {}

    event_websocket_init = []  # function(self)
    event_websocket_open = []  # function(self)
    event_websocket_onmessage = []  # function(self, message)
    event_websocket_onclose = []  # function(self)
