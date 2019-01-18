from utility.misc import Misc
from utility.timer import Timer
import logging
import traceback

from mygame.player import Player


class Game(object):
    def __init__(self):
        self.websockets = Misc.websockets

        self.event_websocket_init = Misc.event_websocket_init
        self.event_websocket_open = Misc.event_websocket_open
        self.event_websocket_onmessage = Misc.event_websocket_onmessage
        self.event_websocket_onclose = Misc.event_websocket_onclose

        self.event_websocket_init.append(self.on_websocket_init)
        self.event_websocket_open.append(self.on_websocket_open)
        self.event_websocket_onmessage.append(self.on_websocket_message)
        self.event_websocket_onclose.append(self.on_websocket_close)

        self.broadcast_interval = 3
        self.broadcast_timer = Timer()

        self.cmd_dict = {}
        self.player_dict = {}
        pass

    def init_cmd_dict(self):
        pass

    ##############################
    # 指令格式(str):
    # cmd:value
    ##############################
    def route_client_message(self, websocket, message):
        if type(message) is bytes:
            message = message.decode('utf-8')

        # test
        for player_id in self.player_dict:
            self.player_dict[player_id].websocket.write_message(message)

        try:
            message = str(message)
            message_splited = message.split(':')
            cmd = message_splited[0]
            val = message_splited[1]

            if cmd in self.cmd_dict:
                func = self.cmd_dict[cmd]
                func(websocket, val)
            else:
                logging.error('not support this cmd. {}'.format(cmd))
        except:
            logging.error(traceback.format_exc())
        pass

    def on_websocket_init(self, websocket):
        logging.debug('初始化完成时调用  socket_id {} init()'.format(websocket.socket_id))

        new_player = Player(websocket, self)
        self.player_dict[new_player.player_id] = new_player

    def on_websocket_open(self, websocket):
        logging.debug('连接成功时调用 socket_id {} open()'.format(websocket.socket_id))
        pass

    def on_websocket_message(self, websocket, message):
        logging.debug('接受client发来的消息时调用 socket_id {} on_message()'.format(websocket.socket_id, message))

        self.route_client_message(websocket, message)
        pass

    def on_websocket_close(self, websocket):
        logging.debug('连接关闭时调用 socket_id {} onclose()'.format(websocket.socket_id))

        socket_id = websocket.socket_id
        player_id = socket_id
        self.player_dict.pop(player_id)

    def run(self):
        msgs = [
            '沒有所謂運氣這回事。 一切無非是考驗、懲罰或補償。',
            '神聖羅馬帝國既不神聖，亦非羅馬，更非帝國。',
            '不经巨大的困难，不会有伟大的事业。（ 11月14日名言）',
            '親愛的讀者，請您相信我這句話吧：萬萬不可以輕易相信。',
            '假如上帝並不存在，那就必須把祂造出來。'
        ]
        import random

        while True:
            if self.broadcast_timer.is_above(self.broadcast_interval, True):
                choice_msg = random.choice(msgs)
                broadcast_msg = 'Game broadcast: {}'.format(choice_msg)
                logging.debug(broadcast_msg)

                for socket_id in self.websockets:
                    self.websockets[socket_id].write_message(broadcast_msg)
                pass
            pass

    pass
