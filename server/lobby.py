from __future__ import division

import socket, struct, uuid

import constants
import random

class Lobby(object):

    # FIXME: Remove, this is only a troll (AJF's idea)
    max_players = 128
    num_players = random.randint(32, 128)

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.timer = 0

    def update(self, server, frametime):
        if self.timer <= 0:
            packet = self.build_reg_packet(server)
            self.socket.sendto(packet, (constants.LOBBY_HOST, constants.LOBBY_PORT))
            self.timer = 30
        else:
            self.timer -= frametime


    def build_reg_packet(self, server):
        packet = ""

        if random.randint(1, 3) == 1:
            if self.num_players < 16:
                self.num_players = 16
            elif self.num_players > self.max_players:
                self.num_players = self.max_players
            else:
                self.num_players += random.randint(-1, 1)

        # Message type for the lobby
        messagetype = uuid.UUID(constants.LOBBY_MESSAGE_TYPE_REG)
        packet += messagetype.get_bytes()
        # Server ID
        packet += server.ID.get_bytes()
        # GG2 Lobby ID
        ID = uuid.UUID(constants.GG2_LOBBY_UUID)
        packet += ID.get_bytes()

        # Protocol Indicator, in our case 1 for UDP
        packet += struct.pack(">B", 1)
        # Port number
        packet += struct.pack(">H", server.port)

        # Max number of players, current number of players and current number of AI players
        #packet += struct.pack(">HHH", server.game.maxplayers, len(server.game.current_state.players), 0)# There are no AI players in mainstream.
        packet += struct.pack(">HHH", self.max_players, self.num_players, 0)# AJF's troll
        # Password protected?
        packet += struct.pack(">H", 0)

        # Number of key-value pairs
        packet += struct.pack(">H", 7)

        # The server name
        packet += struct.pack(">B4sH"+str(len(server.name))+"s", 4, "name", len(server.name), server.name)
        # The current map
        packet += struct.pack(">B3sH"+str(len(server.game.map.mapname))+"s", 3, "map", len(server.game.map.mapname), server.game.map.mapname)

        # The game/mod compatibility protocol
        packet += struct.pack(">B11sH", 11, "protocol_id", 16)
        packet += uuid.UUID(constants.PYGG2_COMPATIBILITY_PROTOCOL).get_bytes()
        # The server game/mod name, short name and version
        packet += struct.pack(">B4sH5sB10sH5sB8sH"+str(len(constants.GAME_VERSION_STRING))+"s", 4, "game", 5, "PyGG2", 10, "game_short", 5, "PyGG2", 8, "game_ver", len(constants.GAME_VERSION_STRING), constants.GAME_VERSION_STRING)
        # The website/page of this game/mod
        packet += struct.pack(">B8sH"+str(len(constants.GAME_URL))+"s", 8, "game_url", len(constants.GAME_URL), constants.GAME_URL)

        return packet


    def destroy(self, server):
        packet = ""
        # Message type for the lobby
        messagetype = uuid.UUID(constants.LOBBY_MESSAGE_TYPE_UNREG)
        packet += messagetype.get_bytes()
        # Server ID
        packet += server.ID.get_bytes()
        self.socket.sendto(packet, (constants.LOBBY_HOST, constants.LOBBY_PORT))
