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
        return struct.pack(">32p32p", self.name, self.password)

    def unpack(self, packetstr):
        self.name, self.password = struct.unpack_from(">32p32p", packetstr)
        return struct.calcsize(">32p32p")

@serverevent
class ServerEventHello(object):
    eventid = constants.EVENT_HELLO

    def __init__(self, servername, playerid, maxplayers, mapname, version):
        self.servername = servername
        self.playerid = playerid
        self.maxplayers = maxplayers
        self.mapname = mapname
        self.version = version

    def pack(self):
        packetstr = struct.pack(">32pBB64pH", self.servername, self.playerid, self.maxplayers, self.mapname, self.version)

        return packetstr

    def unpack(self, packetstr):
        self.servername, self.playerid, self.maxplayers, self.mapname, self.version = struct.unpack_from(">32pBB64pH", packetstr)

        return struct.calcsize(">32pBB64pH")

@clientevent
class ClientEventJump(object):
    eventid = constants.EVENT_JUMP

    def __init__(self, time):
        self.time = time

    def pack(self):
        packetstr = struct.pack(">I", time)

        return packetstr

    def unpack(self, packetstr):
        self.time = struct.unpack(">I", packetstr)[0]

        return struct.calcsize(">I")

@serverevent
class ServerEventChangeclass(object):
    eventid = constants.EVENT_PLAYER_CHANGECLASS

    def __init__(self, playerid, newclass):
        self.playerid = playerid
        self.newclass = newclass

    def pack(self):
        packetstr = struct.pack(">HB", self.playerid, self.newclass)

        return packetstr

    def unpack(self, packetstr):
        self.playerid, self.newclass = struct.unpack_from(">HB", packetstr)

        return struct.calcsize(">HB")

@clientevent
class ClientEventChangeclass(object):
    eventid = constants.EVENT_PLAYER_CHANGECLASS

    def __init__(self, newclass):
        self.newclass = newclass

    def pack(self):
        packetstr = struct.pack(">B", self.newclass)

        return packetstr

    def unpack(self, packetstr):
        self.newclass = struct.unpack_from(">B", packetstr)[0]

        return struct.calcsize(">B")

@serverevent
class ServerEventSpawn(object):
    eventid = constants.EVENT_PLAYER_SPAWN

    def __init__(self, playerid, x, y):
        self.playerid = playerid
        self.x = x
        self.y = y

    def pack(self):
        packetstr = struct.pack(">BII", self.playerid, self.x, self.y)

        return packetstr

    def unpack(self, packetstr):
        self.playerid, self.x, self.y = struct.unpack_from(">BII", packetstr)

        return struct.calcsize(">BII")

@serverevent
class ServerEventDie(object):
    eventid = constants.EVENT_PLAYER_DIE

    def __init__(self, playerid):
        self.playerid = playerid

    def pack(self):
        packetstr = struct.pack(">B", self.playerid)

        return packetstr

    def unpack(self, packetstr):
        self.playerid = struct.unpack_from(">B", packetstr)[0]

        return struct.calcsize(">B")

@clientevent
class ClientEventInputstate(object):
    eventid = constants.INPUTSTATE

    def __init__(self, bytestr):
        self.bytestr = bytestr

    def pack(self):
        packetstr = struct.pack(">H", len(self.bytestr)) # TODO: Implement a better system that doesn't require this length, because it shouldn't be needed.
        packetstr += self.bytestr

        return packetstr

    def unpack(self, packetstr):
        length = struct.unpack_from(">H", packetstr)[0]
        packetstr = packetstr[2:]
        self.bytestr = packetstr[:length]

        return struct.calcsize(">H")+length

@serverevent
class ServerEventSnapshotUpdate(object):
    eventid = constants.SNAPSHOT_UPDATE

    def __init__(self, bytestr):
        self.bytestr = bytestr

    def pack(self):
        packetstr = struct.pack(">H", len(self.bytestr)) # TODO: Implement a better system that doesn't require this length, because it shouldn't be needed.
        packetstr += self.bytestr

        return packetstr

    def unpack(self, packetstr):
        length = struct.unpack_from(">H", packetstr)[0]
        packetstr = packetstr[2:]
        self.bytestr = packetstr[:length]

        return struct.calcsize(">H")+length

@serverevent
class ServerEventFullUpdate(object):
    eventid = constants.FULL_UPDATE

    def __init__(self, bytestr):
        self.bytestr = bytestr

    def pack(self):
        packetstr = struct.pack(">H", len(self.bytestr)) # TODO: Implement a better system that doesn't require this length, because it shouldn't be needed.
        packetstr += self.bytestr

        return packetstr

    def unpack(self, packetstr):
        length = struct.unpack_from(">H", packetstr)[0]
        packetstr = packetstr[2:]
        self.bytestr = packetstr[:length]
        packetstr = packetstr[length:]

        return struct.calcsize(">H")+length

@clientevent
class ClientEventDisconnect(object):
    eventid = constants.EVENT_PLAYER_DISCONNECT

    def pack(self):
        return ""

    def unpack(self, packetstr):
        return 0

@serverevent
class ServerEventDisconnect(object):
    eventid = constants.EVENT_PLAYER_DISCONNECT

    def __init__(self, playerid):
        self.playerid = playerid

    def pack(self):
        packetstr = struct.pack(">B", self.playerid)

        return packetstr

    def unpack(self, packetstr):
        self.playerid = struct.unpack_from(">B", packetstr)[0]

        return struct.calcsize(">B")
