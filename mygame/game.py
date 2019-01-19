from utility.misc import WebsocketGlobalArgs
from utility.timer import Timer
import logging
import traceback

from mygame.cmd_router import Cmd
from mygame.player import Player


class Game(object):
    def __init__(self, cmd_router):
        self.cmd_router = cmd_router

        self.broadcast_interval = 3
        self.broadcast_timer = Timer()

        self.player_dict = {}

        self.cmd_router.register_cmd_handler(Cmd.player_join, self.recv_player_join)
        pass

    def listen_websocket_events(self):
        WebsocketGlobalArgs.event_websocket_open.append(self.__on_websocket_open)
        WebsocketGlobalArgs.event_websocket_onclose.append(self.__on_websocket_close)
        pass

    def recv_player_join(self, websocket, data):
        data = str(data)
        data_split = data.split('|')
        player_name = data_split[0]
        player_hp = data_split[1]
        player_position = data_split[2]
        player_rotation = data_split[3]
        player_scale = data_split[4]
        self.create_player(
            websocket, player_name, player_hp, player_position, player_rotation, player_scale)

    def create_player(
            self, websocket, player_name, player_hp, pos_str, rot_str, sca_str
    ):
        new_player = Player(
            websocket, player_name, player_hp, pos_str, rot_str, sca_str)
        self.player_dict[new_player.player_id] = new_player
        self.send_player_join_done(
            new_player.player_id, new_player.name, new_player.hp, pos_str, rot_str, sca_str)

    def send_player_join_done(
            self, player_id, player_name, player_hp, pos_str, rot_str, sca_str
    ):
        msg = '{}:{}|{}|{}|{}|{}|{}'.format(
            Cmd.player_join_done, player_id, player_name, player_hp, pos_str, rot_str, sca_str)
        self.cmd_router.broadcast_message(msg)

    def on_socket_open(self, websocket):
        socket_id = websocket.socket_id
        msg = '{}:{}'.format(Cmd.socket_open, socket_id)
        self.cmd_router.send_message(socket_id, msg)

    def on_socket_close(self, websocket):
        player_id = websocket.socket_id
        msg = '{}:{}'.format(Cmd.player_leave_done, player_id)
        self.cmd_router.broadcast_message(msg)

    def run(self):
        # msgs = [
        #     '沒有所謂運氣這回事。 一切無非是考驗、懲罰或補償。',
        #     '神聖羅馬帝國既不神聖，亦非羅馬，更非帝國。',
        #     '不经巨大的困难，不会有伟大的事业。（ 11月14日名言）',
        #     '親愛的讀者，請您相信我這句話吧：萬萬不可以輕易相信。',
        #     '假如上帝並不存在，那就必須把祂造出來。'
        # ]
        # import random
        #
        # while True:
        #     if self.broadcast_timer.is_above(self.broadcast_interval, True):
        #         choice_msg = random.choice(msgs)
        #         broadcast_msg = 'Game broadcast: {}'.format(choice_msg)
        #         logging.debug(broadcast_msg)
        #
        #         self.cmd_router.broadcast_message(broadcast_msg)
            pass

    def __on_websocket_open(self, websocket):
        self.on_socket_open(websocket)

    def __on_websocket_close(self, websocket):
        self.on_socket_close(websocket)

    pass
