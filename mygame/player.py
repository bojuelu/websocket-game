import logging
import traceback


class Player(object):
    def __init__(self, websocket, player_id, name, hp, pos_str, rot_str, sca_str):
        self.websocket = websocket
        self.player_id = player_id

        self.name = 'unknow'
        self.hp = 0.0

        self.position_x = 0.0
        self.position_y = 0.0
        self.position_z = 0.0

        self.rotation_x = 0.0
        self.rotation_y = 0.0
        self.rotation_z = 0.0

        self.scale_x = 1.0
        self.scale_y = 1.0
        self.scale_z = 1.0

        self.init_player(websocket.socket_id, name, hp, pos_str, rot_str, sca_str)

    def init_player(self, player_id, name, hp, pos_str, rot_str, sca_str):
        try:
            self.player_id = player_id

            self.name = str(name)
            self.hp = float(hp)

            pos_str_split = str(pos_str).split(',')
            self.position_x = float(pos_str_split[0])
            self.position_y = float(pos_str_split[1])
            self.position_z = float(pos_str_split[2])

            rot_str_split = str(rot_str).split(',')
            self.rotation_x = float(rot_str_split[0])
            self.rotation_y = float(rot_str_split[1])
            self.rotation_z = float(rot_str_split[2])

            sca_str_split = str(sca_str).split(',')
            self.scale_x = float(sca_str_split[0])
            self.scale_y = float(sca_str_split[1])
            self.scale_z = float(sca_str_split[2])
        except:
            logging.error(traceback.format_exc())
        pass
    pass
