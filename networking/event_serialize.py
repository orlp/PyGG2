from __future__ import division, print_function

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

@serverevent
class ServerEventPlayerJoin(object):
    eventid = constants.EVENT_PLAYER_JOIN

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def pack(self):
        return struct.pack(">H32p", self.id, self.name)

    def unpack(self, packetstr):
        self.id, self.name = struct.unpack_from(">H32p", packetstr)

        return struct.calcsize(">H32p")

@clientevent
class ClientEventHello(object):
    eventid = constants.EVENT_HELLO

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def pack(self):
        return struct.pack("32p32p", name, password)

    def unpack(self, packetstr):
        self.name, self.password = struct.unpack_from("32p32p", packetstr)

        return struct.calcsize("32p32p")

@serverevent
class ServerEventHello(object):
    eventid = constants.EVENT_HELLO

    def __init__(self, servername, maxplayers, mapname, version):
        self.servername = servername
        self.maxplayers = maxplayers
        self.mapname = mapname
        self.version = version

    def pack(self):
        packetstr = struct.pack("32pB64pH", self.servername, self.maxplayers, self.mapname, self.version)

        return packetstr

    def unpack(self, packetstr):
        self.servername, self.maxplayers, self.mapname, self.version = struct.unpack_from("32pB64pH", packetstr)

        return struct.calcsize("32pB64pH")

@clientevent
class ClientEventLeftMousebuttonDown(object):
    eventid = constants.EVENT_LEFTMOUSEBUTTON_DOWN

    def __init__(self, time):
        self.time = time

    def pack(self):
        packetstr = struct.pack("I", time)

        return packetstr

    def unpack(self, packetstr):
        self.time = struct.unpack("I", packetstr)

        return 0

@clientevent
class ClientEventRightMousebuttonDown(object):
    eventid = constants.EVENT_RIGHTMOUSEBUTTON_DOWN

    def __init__(self, time):
        self.time = time

    def pack(self):
        packetstr = struct.pack("I", time)

        return packetstr

    def unpack(self, packetstr):
        self.time = struct.unpack("I", packetstr)

        return 0

@clientevent
class ClientEventJump(object):
    eventid = constants.EVENT_JUMP

    def __init__(self, time):
        self.time = time

    def pack(self):
        packetstr = struct.pack("I", time)

        return packetstr

    def unpack(self, packetstr):
        self.time = struct.unpack("I", packetstr)

        return 0
