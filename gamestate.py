from __future__ import division

import pygame
from pygame.locals import *

import math

# the main physics class
# contains the complete game state
class Gamestate:
    def __init__(self):
        self.objects = []
        self.time = 0.0
    
    def update(self, frametime):
        self.time += step
        
        for obj in self.objects: obj.beginstep(self, frametime)
        for player in self.players: player.beginstep(self, frametime)
        
        for obj in self.objects: obj.step(self, frametime)
        for player in self.players: player.step(self, frametime)
        
        for obj in self.objects: obj.endstep(self, frametime)
        for player in self.players: player.endstep(self, frametime)
        
        self.objects = [obj for obj in self.objects if not obj.destroyinstance]
        self.players = [player for player in self.objects if not player.destroyinstance]
    
    def interpolate(self, next_state, alpha):
        integrated_state = Gamestate()
        integrated_state.time = next_state.time * alpha + self.time * (1 - alpha)
        
        return integrated_state
        
    def copy(self):
        new = Gamestate()
        
        new.time = self.time
        new.objects = [obj.copy() for obj in self.objects]
        
        return new
    
    def serialize_state(self):
        bytestate = str()
        return bytestate
    
    def deserialize_state(self, bytestate):
        pass