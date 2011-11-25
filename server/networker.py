from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import socket
import constants
import networking.packet
import event_handler

class Networker(object):
    def __init__(self, port):
        self.send_accumulator = 0.0
        self.port = port
        
        self.sequence = 0
        
        self.players = {}
        self.update_counters = {}
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("", self.port))
        self.socket.setblocking(False)
        
    def send(self, server, game, frametime):        
        for address, player in self.players.items():
            self.update_counters[player.id] += frametime
            
            if self.update_counters[player.id] > constants.NETWORK_UPDATE_RATE:
                self.update_counters[player.id] %= constants.NETWORK_UPDATE_RATE
                
                player.sendupdate()
    
    def recieve(self, server, game):
        packet = networking.packet.Packet("client")
        
        # recieve all packets
        while True:
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
            
            # only handle this packet if we know the player or the first event is a hello
            if sender in self.players:
                for event in packet.events:
                    event_handler.eventhandlers[type(event)](self, game, self.players[sender])
            # or if someone wants to shake hands
            elif packet.events[0].eventid == constants.EVENT_HELLO:
                