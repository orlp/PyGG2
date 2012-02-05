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
        self.sendbuffer = []

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("", self.port))
        self.socket.setblocking(False)


    def update(self, server, game, frametime):
        # update everyone
        for address, player in self.players.items():
            # Let each of the players decide whether to send something
            player.update(self, game, frametime)


    def generate_statedata(self, game):
        packetstr = ""
        state = game.current_state

        for playerid, player in state.players.items():
            packetstr += player.serialize_input()
            character = state.entities[player.character_id]
            packetstr += character.serialize(state)

        return packetstr


    def service_new_player(self, server, game, player):
        pass


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
                    event_handler.eventhandlers[type(event)](self, game, self.players[sender], event)

                # Stick the new events to everyone
                for event in self.sendbuffer:
                    player.events.append((player.acksequence, event))
                self.sendbuffer = []# Clear the slate afterwards

            # or if someone wants to shake hands
            elif packet.events[0].eventid == constants.EVENT_HELLO:
                if packet.password == server.password:
                    newplayer = player.Player(self, game, packet.name, sender)
                    player.name = packet.name

                    for player in self.players.items():
                        if player == newplayer:
                            self.service_new_player(self, server, game, player)
                        else:
                            join_event = event_serialize.Server_Event_Player_Join(player.id, player.name)
                            player.events.append((player.acksequence, join_event))
            # otherwise drop the packet
            else:
                continue

            # ack the packet
            self.players[sender].acksequence = packet.sequence
