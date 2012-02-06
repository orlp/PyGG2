from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import socket
import constants
import networking.packet
import networking.event_serialize
import event_handler

class Networker(object):
    def __init__(self, server_address, client):
        self.server_address = server_address

        self.events = []
        self.sequence = 0
        self.acksequence = 0

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("", 0))
        self.socket.setblocking(False)

        self.has_connected = False
        self.connection_timeout_timer = constants.CLIENT_TIMEOUT

        # Connect to the server, or at least send the hello
        packet = networking.packet.Packet("client")
        packet.sequence = 0
        packet.acksequence = 0

        event = networking.event_serialize.Client_Event_Hello(client.player_name, client.server_password)
        packet.events.append(event)
        data = packet.pack()

        numbytes = self.socket.sendto(data, self.server_address)
        if len(data) != numbytes:
            # TODO sane error handling
            print("SERIOUS ERROR, NUMBER OF BYTES SENT != PACKET SIZE AT HELLO")


    def recieve(self, game, client):
        # If we haven't received confirmation that we're connected yet, see if we should try again:
        if not self.has_connected:
            self.connection_timeout_timer -= 1

            if self.connection_timeout_timer <= 0:
                self.connection_timeout_timer = constants.CLIENT_TIMEOUT
                # Send a reminder, in case the first packet was lost
                packet = networking.packet.Packet("client")
                packet.sequence = 0
                packet.acksequence = 0

                event = networking.event_serialize.Client_Event_Hello(client.player_name, client.server_password)
                packet.events.append(event)
                data = packet.pack()

                numbytes = self.socket.sendto(data, self.server_address)
                if len(data) != numbytes:
                    # TODO sane error handling
                    print("SERIOUS ERROR, NUMBER OF BYTES SENT != PACKET SIZE AT HELLO")


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
