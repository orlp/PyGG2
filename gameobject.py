from __future__ import division

import pygame
from pygame.locals import *
from functions import sign, point_direction
import math

import gamestate

# simple object implementing movement
class Gameobject(gamestate.Entity):
    def __init__(self, state, xpos = 0.0, ypos = 0.0, hspeed = 0.0, vspeed = 0.0):
        # x and y are the position of the actual object
        self.x = float(xpos)
        self.y = float(ypos)

        # hspeed and vspeed are the speeds of the object in respective directions
        self.hspeed = float(hspeed)
        self.vspeed = float(vspeed)

    def endstep(self, state, frametime):
        self.x += self.hspeed * frametime
        self.y += self.vspeed * frametime
        
        self.x = max(self.x, 0)
        self.y = max(self.y, 0)
