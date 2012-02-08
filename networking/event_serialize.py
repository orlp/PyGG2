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

class Event_Mainframe(object):
    def __init__(self, sequence):
        self.sequence = sequence

    def pack(self):
        return struct.pack(">H", self.sequence)

    def unpack(self, packetstr):
        self.sequence = struct.unpack_from(">H", self.sequence)
        return 1

@serverevent
class Server_Event_Player_Join(Event_Mainframe):
    eventid = constants.EVENT_PLAYER_JOIN

    def __init__(self, sequence, id, name):
        Event_Mainframe.__init__(self, sequence)
        self.id = id
        self.name = name

    def pack(self):
        return Event_Mainframe.pack(self) + struct.pack(">H32p", self.id, self.name)

    def unpack(self, packetstr):
        mainframe_length = Event_Mainframe.unpack(self, packetstr)
        packetstr = packetstr[length:]
        self.id, self.name = struct.unpack_from(">H32p", packetstr)

        return mainframe_length + struct.calcsize(">H32p")

@clientevent
class Client_Event_Hello(Event_Mainframe):
    eventid = constants.EVENT_HELLO

    def __init__(self, sequence, name, password):
        Event_Mainframe.__init__(self, sequence)
        self.name = name
        self.password = password

    def pack(self):
        return Event_Mainframe.pack(self) + struct.pack(">32p32p", self.name, self.password)

    def unpack(self, packetstr):
        mainframe_length = Event_Mainframe.unpack(self, packetstr)
        packetstr = packetstr[length:]
        self.name, self.password = struct.unpack_from(">32p32p", packetstr)
        return mainframe_length + struct.calcsize(">32p32p")

@serverevent
class Server_Event_Hello(Event_Mainframe):
    eventid = constants.EVENT_HELLO

    def __init__(self, sequence, servername, maxplayers, mapname, version):
        Event_Mainframe.__init__(self, sequence)
        self.servername = servername
        self.maxplayers = maxplayers
        self.mapname = mapname
        self.version = version

    def pack(self):
        packetstr = Event_Mainframe.pack(self) + struct.pack(">32pB64pH", self.servername, self.maxplayers, self.mapname, self.version)

        return packetstr

    def unpack(self, packetstr):
        mainframe_length = Event_Mainframe.unpack(self, packetstr)
        packetstr = packetstr[length:]
        self.servername, self.maxplayers, self.mapname, self.version = struct.unpack_from(">32pB64pH", packetstr)

        return mainframe_length + struct.calcsize(">32pB64pH")

@clientevent
class Client_Event_Jump(Event_Mainframe):
    eventid = constants.EVENT_JUMP

    def __init__(self, sequence, time):
        Event_Mainframe.__init__(self, sequence)
        self.time = time

    def pack(self):
        packetstr = Event_Mainframe.pack(self) + struct.pack(">I", time)

        return packetstr

    def unpack(self, packetstr):
        mainframe_length = Event_Mainframe.unpack(self, packetstr)
        packetstr = packetstr[length:]
        self.time = struct.unpack(">I", packetstr)[0]

        return mainframe_length + struct.calcsize(">I")

@serverevent
class Server_Event_Changeclass(Event_Mainframe):
    eventid = constants.EVENT_PLAYER_CHANGECLASS

    def __init__(self, sequence, playerid, newclass):
        Event_Mainframe.__init__(self, sequence)
        self.playerid = playerid
        self.newclass = newclass

    def pack(self):
        packetstr = Event_Mainframe.pack(self) + struct.pack(">HB", self.playerid, self.newclass)

        return packetstr

    def unpack(self, packetstr):
        mainframe_length = Event_Mainframe.unpack(self, packetstr)
        packetstr = packetstr[length:]
        self.playerid, self.newclass = struct.unpack_from(">HB", packetstr)

        return mainframe_length + struct.calc_size(">HB", packetstr)

@clientevent
class Client_Event_Changeclass(Event_Mainframe):
    eventid = constants.EVENT_PLAYER_CHANGECLASS

    def __init__(self, sequence, newclass):
        Event_Mainframe.__init__(self, sequence)
        self.newclass = newclass

    def pack(self):
        packetstr = Event_Mainframe.pack(self) + struct.pack(">B", self.newclass)

        return packetstr

    def unpack(self, packetstr):
        mainframe_length = Event_Mainframe.unpack(self, packetstr)
        packetstr = packetstr[length:]
        self.newclass = struct.unpack_from(">B", packetstr)[0]

        return mainframe_length + struct.calcsize(">B")

@serverevent
class Server_Event_Spawn(Event_Mainframe):
    eventid = constants.EVENT_PLAYER_SPAWN

    def __init__(self, sequence, playerid, x, y):
        Event_Mainframe.__init__(self, sequence)
        self.playerid = playerid
        self.x = x
        self.y = y

    def pack(self):
        packetstr = Event_Mainframe.pack(self) + struct.pack(">BII", self.playerid, self.x, self.y)

        return packetstr

    def unpack(self, packetstr):
        mainframe_length = Event_Mainframe.unpack(self, packetstr)
        packetstr = packetstr[length:]
        self.playerid, self.x, self.y = struct.unpack_from(">BII", packetstr)

        return mainframe_length + struct.calcsize(">BII")

@serverevent
class Server_Event_Die(Event_Mainframe):
    eventid = constants.EVENT_PLAYER_DIE

    def __init__(self, sequence, playerid):
        Event_Mainframe.__init__(self, sequence)
        self.playerid = playerid

    def pack(self):
        packetstr = Event_Mainframe.pack(self) + struct.pack(">B", self.playerid)

        return packetstr

    def unpack(self, packetstr):
        mainframe_length = Event_Mainframe.unpack(self, packetstr)
        packetstr = packetstr[length:]
        self.playerid = struct.unpack_from(">B", packetstr)[0]

        return mainframe_length + struct.calcsize(">B")

@clientevent
class Client_Event_Inputstate(Event_Mainframe):
    eventid = constants.INPUTSTATE

    def __init__(self, sequence, bytestr):
        Event_Mainframe.__init__(self, sequence)
        self.bytestr = bytestr

    def pack(self):
        packetstr =  Event_Mainframe.pack(self) + struct.pack(">H", len(self.bytestr)) # TODO: Implement a better system that doesn't require this length, because it shouldn't be needed.
        packetstr += bytestr

        return packetstr

    def unpack(self, packetstr):
        mainframe_length = Event_Mainframe.unpack(self, packetstr)
        packetstr = packetstr[length:]
        length = struct.unpack_from(">H", packetstr)[0]
        bytestr = packetstr[:length]

        return mainframe_length + struct.calcsize(">H") + length

@serverevent
class Server_Event_Snapshot_Update(Event_Mainframe):
    eventid = constants.SNAPSHOT_UPDATE

    def __init__(self, sequence, bytestr):
        Event_Mainframe.__init__(self, sequence)
        self.bytestr = bytestr

    def pack(self):
        packetstr = Event_Mainframe.pack(self) + struct.pack(">H", len(self.bytestr)) # TODO: Implement a better system that doesn't require this length, because it shouldn't be needed.
        packetstr += self.bytestr

        return packetstr

    def unpack(self, packetstr):
        mainframe_length = Event_Mainframe.unpack(self, packetstr)
        packetstr = packetstr[length:]
        length = struct.unpack_from(">H", packetstr)[0]
        self.bytestr = packetstr[:length]

        return mainframe_length + struct.calcsize(">H") + length

@serverevent
class Server_Event_Full_Update(Event_Mainframe):
    eventid = constants.FULL_UPDATE

    def __init__(self, sequence, bytestr):
        Event_Mainframe.__init__(self, sequence)
        self.bytestr = bytestr

    def pack(self):
        packetstr = Event_Mainframe.pack(self) + struct.pack(">H", len(self.bytestr)) # TODO: Implement a better system that doesn't require this length, because it shouldn't be needed.
        packetstr += self.bytestr

        return packetstr

    def unpack(self, packetstr):
        mainframe_length = Event_Mainframe.unpack(self, packetstr)
        packetstr = packetstr[length:]
        length = struct.unpack_from(">H", packetstr)[0]
        packetstr = packetstr[2:]
        self.bytestr = packetstr[:length]
        packetstr = packetstr[length:]

        return mainframe_length + struct.calcsize(">H")+length
