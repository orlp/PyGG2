from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import socket
import constants
import networking.packet
import event_handler

class Networker(object):
    def __init__(self, port, server_address):
        self.server_address = server_address

        self.events = []
        self.sequence = 0
        self.acksequence = 0

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("", self.port))
        self.socket.setblocking(False)

    def recieve(self, game):
        while True:
            packet = networking.packet.Packet("server")

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

            # only accept the packet if the sender is the server
            if sender == self.server_address:
                for event in packet.events:
                    event_handler.eventhandlers[type(event)](self, game, event)
            # otherwise drop the packet
            else:
                continue

            # ack the packet
            self.acksequence = packet.sequence

            # Clear the acked stuff from the history
            index = 0
            while index < len(self.events):
                seq, event = self.events[index]
                if seq > self.acksequence:
                    # This (and all the following events) weren't acked yet. We're done.
                    break
                else:
                    del self.events[index]
                    index -= 1
                index += 1


    def generate_inputdata(self, client):
        packetstr = client.our_player.serialize_input()
        return packetstr


    def update(self, client):
        packet = networking.packet.Packet("client")
        packet.sequence = self.sequence
        packet.acksequence = self.acksequence
        packet.events = [event[1] for event in self.events]

        packetstr = ""
        packetstr += self.generate_inputdata(client)
        packetstr += packet.pack()

        self.sequence = (self.sequence + 1) % 65535
