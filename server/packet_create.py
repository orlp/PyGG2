#!/usr/bin/env python

from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import precision_timer
import engine.game
import constants

def create_packet(game, state):

    tempbuffer = str()

    for player in players:
        
