from __future__ import division, print_function
# add our main folder as include dir
import sys
sys.path.append("../")

import socket
import struct
import constants
import function
import networking.packet
import networking.event_serialize
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
        for address, player_obj in self.players.items():
            # Give them the new events
            for event in self.sendbuffer:
                player_obj.events.append((player_obj.sequence, event))

            # Let each of the players decide whether to send something
            player_obj.update(self, game, frametime)

        # Clear the slate afterwards
        self.sendbuffer = []


    def generate_snapshot_update(self, game):
        packetstr = ""
        state = game.current_state

        packetstr += struct.pack(">I", state.time)

        for playerid, player_obj in state.players.items():
            packetstr += player_obj.serialize_input()
            try:
                character = state.entities[player_obj.character_id]
                packetstr += character.serialize(state)
            except KeyError:
                # Character is dead
                pass

        event = networking.event_serialize.ServerEventSnapshotUpdate(packetstr)

        return event


    def generate_full_update(self, game):
        packetstr = ""
        state = game.current_state

        packetstr += struct.pack(">I", state.time)
        packetstr += struct.pack(">B", len(state.players))

        for player_id, player_obj in state.players.items():
            try:
                current_class = state.entities[player_obj.character_id].__class__
                current_class = function.convert_class(current_class)
                character_exists = True
            except KeyError:
                # The character does not exist yet.
                # Send nextclass instead
                current_class = function.convert_class(player_obj.nextclass)
                character_exists = False

            packetstr += struct.pack(">32pBB", player_obj.name, current_class, character_exists)

        event = networking.event_serialize.ServerEventFullUpdate(packetstr)
        return event


    def service_new_player(self, server, game, newplayer):
        hello_event = networking.event_serialize.ServerEventHello(server.name, newplayer.id,  server.game.maxplayers, server.game.map.mapname, constants.GAME_VERSION_NUMBER)
        newplayer.events.append((newplayer.sequence, hello_event))

        update = self.generate_full_update(game)
        newplayer.events.append((newplayer.sequence, update))

    def recieve(self, server, game):
        # recieve all packets
        while True:
            packet = networking.packet.Packet("client")

            try:
                data, sender = self.socket.recvfrom(constants.MAX_PACKET_SIZE)
            except socket.error:
                # recvfrom throws socket.error if there was no packet to read
                break

            # FIXME: Uncomment these as soon as networking debugging is done. I commented this out because it messed with Traceback.
            #try:
            packet.unpack(data)
            #except:
            #    # parse error, don't throw exception but print it
            #    print("Parse error: %s" % sys.exc_info()[1])
            #    continue # drop packet

            # only handle this packet if we know the player
            if sender in self.players:
                for seq, event in packet.events:
                    if seq <= self.players[sender].server_acksequence:
                        # Event has already been processed before, discard
                        continue
                    try:
                        event_handler.eventhandlers[event.eventid](self, game, self.players[sender], event)
                    except KeyError:
                        # Invalid event; ignore
                        print("WARNING: Client sent invalid event:", type(event), event.eventid)

            # or if someone wants to shake hands
            elif (packet.events[0])[1].eventid == constants.EVENT_HELLO:
                event = (packet.events[0])[1]
                if event.password == server.password:
                    newplayer = player.Player(self, game, event.name, sender)
                    newplayer.name = event.name

                    for player_obj in self.players.values():
                        if player_obj == newplayer:
                            self.service_new_player(server, game, newplayer)
                        else:
                            join_event = networking.event_serialize.ServerEventPlayerJoin(newplayer.id, newplayer.name)
                            player_obj.events.append((player_obj.sequence, join_event))
            # otherwise drop the packet
            else:
                continue

            try:
                # ack the packet
                self.players[sender].server_acksequence = packet.sequence
                self.players[sender].client_acksequence = packet.acksequence
            except KeyError:
                # The player has just disconnected, so no-one cares about acksequence
                pass
