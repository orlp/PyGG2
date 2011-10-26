from __future__ import division

import pygame
from pygame.locals import *

import math

# helper class for the gamestate
# every entity should inherit from this
class Entity:
    def __init__(self, state):
        self.id = state.entity_count
        state.entities[id] = self
        state.entity_count += 1
    
    def destroy(self, state):
        del state.entities[self.id]
    
    def beginstep(self, state, frametime): pass
    def step(self, state, frametime): pass
    def endstep(self, state, frametime): pass
    def draw(self, state, surface): pass

# the main physics class
# contains the complete game state
class Gamestate:
    def __init__(self):
        self.entities = {}
        self.next_entity_id = 0
        self.time = 0.0
    
    def update(self, game, frametime):
        self.time += step
        
        for entity in entities: entity.beginstep(self, game, frametime)
        for entity in entities: entity.step(self, game, frametime)
        for entity in entities: entity.endstep(self, game, frametime)
    
    def interpolate(self, next_state, alpha):
        interpolated_state = Gamestate()
        interpolated_state.next_entity_id = next_state.next_entity_id
        interpolated_state.time = next_state.time * alpha + self.time * (1 - alpha)
        
        return interpolated_state
        
    def copy(self):
        new = Gamestate()
        
        new.entities = {id:entity.copy() for id, entity in self.entities.items()}
        new.next_entity_id = self.next_entity_id
        new.time = self.time
        
        return new
    
    def serialize_state(self):
        bytestate = str()
        return bytestate
    
    def deserialize_state(self, bytestate):
        pass