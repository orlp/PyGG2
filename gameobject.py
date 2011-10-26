from __future__ import division

import math, pygame
from pygame.locals import *

import function
import gamestate

# simple object implementing movement
class Gameobject(gamestate.Entity):
    def __init__(self, game, state):
        self.Entity.__init__(self)
        
        # x and y are the position of the actual object
        self.x = 0.0
        self.y = 0.0

        # hspeed and vspeed are the speeds of the object in respective directions
        self.hspeed = 0.0
        self.vspeed = 0.0

    def endstep(self, game, state, frametime):
        self.x += self.hspeed * frametime
        self.y += self.vspeed * frametime
        
        self.x = max(self.x, 0)
        self.y = max(self.y, 0)
