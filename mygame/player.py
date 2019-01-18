class Player(object):
    def __init__(self, websocket, game):
        self.websocket = websocket
        self.game = game

        self.player_id = websocket.socket_id

        self.name = 'unknow'
        self.hp = 10
        pass

    def setup_basic_info(self, name, hp):
        self.name = name
        self.hp = hp
        pass
    pass
