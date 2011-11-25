from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import networking

class Player(object):
    def __init__(self, networker, name, address):
        potentialids = set(range(len(networker.players) + 1))
        takenids = {player.id for player in networker.players.items()}
        
        self.address = address
        self.id = (potentialids - takenids).pop()
        
        self.events = []
        self.sequence = 0
        self.acksequence = 0
        
        networker.players[address] = self
        networker.update_counters[self.id] = 0.0
    
    def sendupdate(self, networker):
        packet = networking.packet.Packet("server")
        packet.sequence = self.sequence
        packet.acksequence = self.acksequence
        packet.events = self.events
            
        data = packet.pack()
            
        numbytes = self.socket.sendto(data, self.address)
        if len(data) != numbytes:
            # TODO sane error handling
            print("SERIOUS ERROR, NUMBER OF BYTES SENT != PACKET SIZE")
            
        self.sequence = (self.sequence + 1) % 65535