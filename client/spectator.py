from __future__ import division, print_function

import engine.gamestate
import constants

class Spectator(object):
    def __init__(self, player):
        self.x = 0
        self.y = 0
        self.following_id = player
