from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import socket
import constants
import networking.packet
import event_handler
import player

class Networker(object):
    def __init__(self, port):
        self.port = port

        self.players = {}

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("", self.port))
        self.socket.setblocking(False)

    def update(self, server, game, frametime):
        # generate events

        # send packets if necessary
        for address, player in self.players.items():
            player.update(self, game, frametime)

    def recieve(self, server, game):
        # recieve all packets
        while True:
            packet = networking.packet.Packet("client")

            try:
                data, sender = self.socket.recvfrom(constants.MAX_PACKET_SIZE)
            except socket.error:
                # recvfrom throws socket.error if there was no packet to read
                break

            try:
                packet.unpack(data)
            except:
                # parse error, don't throw exception but print it
                print("Parse error: %s" % sys.exc_info()[1])
                continue # drop packet

            # only handle this packet if we know the player
            if sender in self.players:
                for event in packet.events:
                    event_handler.eventhandlers[type(event)](self, game, self.players[sender])
            # or if someone wants to shake hands
            elif packet.events[0].eventid == constants.EVENT_HELLO:
                if packet.password == server.password:
                    newplayer = player.Player(self, game, packet.name, sender)

                    for player in self.players.items():
                        if player == newplayer:
                            pass # TODO ADD SERVER_EVENT_HELLO
                        else:
                            pass # TODO ADD PLAYER_JOIN
            # otherwise drop the packet
            else:
                continue

            # ack the packet
            self.players[sender].acksequence = packet.sequence
