from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import networking
import engine.player
import constants

class Player(object):
    def __init__(self, networker, game, name, address):
        # generate id
        potentialids = set(range(len(networker.players) + 1))
        takenids = {player.id for player in networker.players.items()}
        self.id = (potentialids - takenids).pop()

        # communication data
        self.address = address
        self.events = []
        self.sequence = 1
        self.acksequence = 0
        self.time_since_update = 0.0

        # register in networker
        networker.players[address] = self

        # and at last add to engine
        engine.player.Player(game, game.current_state, self.id)

    def update(self, networker, game, frametime):
        # Clear the acked stuff from the history
        index = 0
        while index < len(self.events):
            seq, event = self.events[index]
            if seq > self.acksequence:
                # This (and all the following events) weren't acked yet. We're done.
                break
            else:
                self.events.pop(index)
                index -= 1
            index += 1

        self.time_since_update += frametime

        if self.time_since_update > constants.NETWORK_UPDATE_RATE:
            self.time_since_update %= constants.NETWORK_UPDATE_RATE
            self.send_packet(networker, game)

    def send_packet(self, networker, game):
        packet = networking.packet.Packet("server")
        packet.sequence = self.sequence
        packet.acksequence = self.acksequence
        packet.events = [event[1] for event in self.events]

        # Put state data before event data, for better compression
        data = networker.generate_snapshot_update(game)
        data += packet.pack()

        numbytes = networker.socket.sendto(data, self.address)
        if len(data) != numbytes:
            # TODO sane error handling
            print("SERIOUS ERROR, NUMBER OF BYTES SENT != PACKET SIZE")

        self.sequence = (self.sequence + 1) % 65535
