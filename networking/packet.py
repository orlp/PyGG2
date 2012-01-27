#!/usr/bin/env python

from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import struct
import event

class Packet(object):
    def __init__(self, sender):
        self.sequence = None
        self.acksequence = None
        self.events = []
        self.sender = sender

    def pack(self):
        packetstr = ""

        packetstr += struct.pack(">HH", sequence, acksequence)

        for event in self.events:
            packetstr += struct.pack(">B", event.eventid)
            packetstr += event.pack()

        return packetstr

    def unpack(self, packetstr):
        self.events = []

        self.sequence, self.acksequence = struct.unpack_from(">HH", packetstr)
        packetstr = packetstr[struct.calcsize(">HH"):]

        while packetstr:
            eventid = struct.unpack_from(">B", packetstr)
            packetstr = packetstr[struct.calcsize(">B"):]

            if self.sender == "client":
                event = object.__new__(event.clientevents[eventid])
            else:
                event = object.__new__(event.serverevents[eventid])

            eventsize = event.unpack(packetstr)
            packetstr = packetstr[eventsize:]

            self.events.append(event)
