#!/usr/bin/env python

from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import struct
import event_serialize

class Packet(object):
    def __init__(self, sender):
        self.sequence = None
        self.acksequence = None
        self.events = []
        self.sender = sender

    def pack(self):
        packetstr = ""

        packetstr += struct.pack(">HH", sequence, acksequence)

        for packet_event in self.events:
            packetstr += struct.pack(">B", packet_event.eventid)
            packetstr += packet_event.pack()

        return packetstr

    def unpack(self, packetstr):
        self.events = []
        statedata = []

        self.sequence, self.acksequence = struct.unpack_from(">HH", packetstr)
        packetstr = packetstr[struct.calcsize(">HH"):]

        while packetstr:
            eventid = struct.unpack_from(">B", packetstr)
            packetstr = packetstr[struct.calcsize(">B"):]

            if self.sender == "client":
                packet_event = object.__new__(event_serialize.clientevents[eventid])
            else:
                packet_event = object.__new__(event_serialize.serverevents[eventid])

            eventsize = packet_event.unpack(packetstr)
            packetstr = packetstr[eventsize:]

            # Separate states and events
            if eventid in (constants.INPUTSTATE, constants.SNAPSHOT_UPDATE, constants.FULL_UPDATE):
                statedata.append(packet_event)
            else:
                self.events.append(packet_event)

            # Append the state updates to the end of the normal event list.
            self.events += statedata
