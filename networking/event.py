from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import constants
import struct

clientevents = {}
serverevents = {}

# decorators to register classes as events
def clientevent(cls):
    clientevents[cls.eventid] = cls
    return cls

def serverevent(cls):
    serverevents[cls.eventid] = cls
    return cls

@clientevent
class ClientEventHello(object):
    eventid = constants.EVENT_HELLO

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def pack(self):
        return struct.pack("32p32p", name, password)

    def unpack(self, packetstr):
        name, password = struct.unpack_from("32p32p", packetstr)
        packetstr = packetstr[struct.calcsize("32p32p"):]

        return packetstr
