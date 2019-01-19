import logging
import traceback

from utility.misc import WebsocketGlobalArgs
from utility.timer import Timer


class Cmd(object):
    socket_open = "socket_open"
    player_join = "player_join"
    player_join_done = "player_join_done"
    player_leave = "player_leave"
    player_leave_done = "player_leave_done"
    player_transform = "player_transform"
    chat = "chat"
    create_bullet = "create_bullet"
    create_bullet_done = "create_bullet_done"
    bullet_transform = "bullet_transform"
    del_bullet = "del_bullet"
    del_bullet_done = "del_bullet_done"
    bullet_hit_player = "bullet_hit_player"
    pass


class CmdRouter(object):
    def __init__(self):
        self.websockets = None

        self.cmd_dict = {}
        pass

    def listen_websocket_events(self):
        self.websockets = WebsocketGlobalArgs.websockets

        WebsocketGlobalArgs.event_websocket_init.append(self.__on_websocket_init)
        WebsocketGlobalArgs.event_websocket_open.append(self.__on_websocket_open)
        WebsocketGlobalArgs.event_websocket_onmessage.append(self.__on_websocket_message)
        WebsocketGlobalArgs.event_websocket_onclose.append(self.__on_websocket_close)

    ###################################################################################################################
    # 註冊各個cmd處理的方法
    # cmd(str) = 就是cmd沒啥好解釋
    # func(function) = 處理的方法，也就是function，一定是兩個function input: websocket(WebsocketHandler物件), data(str)
    ###################################################################################################################
    def register_cmd_handler(self, cmd, func):
        self.cmd_dict[cmd] = func
        pass

    # ###################################################################################################################
    # # 註冊來自websocket的事件
    # # 處理事件的function, function input請見misc.py class WebsocketGlobalArgs
    # ###################################################################################################################
    # def register_websocket_events_handler(
    #         self, init_handler=None, open_handler=None, onmessage_handler=None, onclose_handler=None
    # ):
    #     if init_handler is not None:
    #         self.event_websocket_init.append(init_handler)
    #     if open_handler is not None:
    #         self.event_websocket_open.append(open_handler)
    #     if onmessage_handler is not None:
    #         self.event_websocket_onmessage.append(onmessage_handler)
    #     if onclose_handler is not None:
    #         self.event_websocket_onclose.append(onclose_handler)
    #     pass

    ############################################################
    # 收到websocket的信息時，把資料派送出去處理
    # 這邊的規範，任何信息都是這種格式 cmd:data
    # 由':'分隔出cmd, data
    ############################################################
    def route_client_message(self, websocket, message):
        if type(message) is bytes:
            message = message.decode('utf-8')

        try:
            message = str(message)
            message_split = message.split(':')
            cmd = message_split[0]
            data = message_split[1]

            if cmd in self.cmd_dict:
                func = self.cmd_dict[cmd]
                func(websocket, data)
            else:
                logging.error('not support this cmd. {}'.format(cmd))
        except:
            logging.error(traceback.format_exc())
        pass

    def send_message(self, socket_id, message):
        if socket_id in self.websockets:
            self.websockets[socket_id].write_message(message)
        else:
            logging.error('socket_id not exist. {}'.format(socket_id))

    def broadcast_message(self, message):
        for socket_id in self.websockets:
            self.websockets[socket_id].write_message(message)

    def __on_websocket_init(self, websocket):
        logging.debug('初始化完成时调用  socket_id {} init()'.format(websocket.socket_id))

    def __on_websocket_open(self, websocket):
        logging.debug('连接成功时调用 socket_id {} open()'.format(websocket.socket_id))

    def __on_websocket_message(self, websocket, message):
        logging.debug('接受client发来的消息时调用 socket_id {} on_message()'.format(websocket.socket_id, message))
        self.route_client_message(websocket, message)

    def __on_websocket_close(self, websocket):
        logging.debug('连接关闭时调用 socket_id {} onclose()'.format(websocket.socket_id))
