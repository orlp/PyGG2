from __future__ import division

import socket, struct, uuid

import constants

class Lobby(object):
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.timer = 30

    def update(self, server, frametime):
        if self.timer <= 0:
            packet = self.build_packet(server)
            self.socket.sendto(packet, (constants.LOBBY_HOST, constants.LOBBY_PORT))
            self.timer = 30
        else:
            self.timer -= frametime

    def build_packet(self, server):
        packet = ""

        # Message type for the lobby
        messagetype = uuid.UUID()
        packet += messagetype.get_bytes(constants.LOBBY_MESSAGE_TYPE_UUID)
        # Server ID
        ID = uuid.uuid4()
        packet += ID.get_bytes()
        # GG2 Lobby ID
        ID = uuid.UUID(constants.GG2_LOBBY_UUID)
        packet += ID.get_bytes()

        # Protocol Indicator, in our case 1 for UDP
        packet += struct.pack(">B", 1)
        # Port number
        packet += struct.pack(">H", server.port)

        # Max number of players, current number of players and current number of AI players
        packet += struct.pack(">HHH", server.game.maxplayers, len(server.game.current.players), 0)# There are no AI players in mainstream.
        # Password protected?
        packet += struct.pack(">H", 0)

        # Number of key-value pairs
        packet += struct.pack(">H", 7)

        # The server name
        packet += struct.pack(">B4sH"+str(len(server.name))+"s", 4, "name", len(server.name), server.name)
        # The current map
        packet += struct.pack(">B3sH"+str(len(server.game.map.mapname))+"s", "map", server.game.map.mapname)

        # The game/mod compatibility protocol
        packet += struct.pack(">B11sH", 11, "protocol_id", 16)
        packet += uuid.UUID(constants.PYGG2_COMPATIBILITY_PROTOCOL)
        # The server game/mod name, short name and version
        packet += struct.pack(">B4sH5sB10sH5sB8sH"+str(len(constants.GAME_VERSION_STRING))+"s", "game", "PyGG2", "game_short", "PyGG2", "game_ver", constants.GAME_VERSION_STRING)
        # The website/page of this game/mod
        packet += struct.pack(">B8sH"+str(len(constants.GAME_URL)), "game_url", constants.GAME_URL)

        return packet
