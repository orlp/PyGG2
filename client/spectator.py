from __future__ import division, print_function

import engine.gamestate
import constants

class Spectator(object):
    def __init__(self, player):
        self.x = 1700
        self.y = 900
        self.player = player
