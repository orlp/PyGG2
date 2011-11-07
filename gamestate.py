#!/usr/bin/env python

from __future__ import division, print_function

# the main physics class
# contains the complete game state
class Gamestate(object):
    def __init__(self):
        self.entities = {}
        self.next_entity_id = 0
        self.time = 0.0
    
    def update(self, game, frametime):
        self.time += frametime
        
        for entity in self.entities.values(): entity.beginstep(game, self, frametime)
        for entity in self.entities.values(): entity.step(game, self, frametime)
        for entity in self.entities.values(): entity.endstep(game, self, frametime)
    
    def interpolate(self, next_state, alpha):
        interpolated_state = Gamestate()
        
        interpolated_state.next_entity_id = next_state.next_entity_id
        interpolated_state.time = self.time * (1 - alpha) + next_state.time * alpha
        interpolated_state.entities = {id:entity.copy() for id, entity in self.entities.items() if id in next_state.entities}
        
        for id, entity in interpolated_state.entities.items():
            entity.interpolate(next_state.entities[id], alpha)
        
        return interpolated_state
        
    def copy(self):
        new = Gamestate()
        
        new.entities = {id:entity.copy() for id, entity in self.entities.items()}
        new.next_entity_id = self.next_entity_id
        new.time = self.time
        
        return new
    
    # TODO: make serialize functions
    def serialize_state(self):
        bytestate = str()
        return bytestate
    
    def deserialize_state(self, bytestate):
        pass