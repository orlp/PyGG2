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

    def interpolate(self, prev_state, next_state, alpha):
        self.next_entity_id = next_state.next_entity_id
        self.time = prev_state.time + (next_state.time - prev_state.time) * alpha

        # remove unnecessary entities
        self.entities = {id:entity for id, entity in self.entities.items() if id in next_state.entities}

        for id, entity in next_state.entities.items():
            if not id in self.entities:
                self.entities[id] = next_state.entities[id].copy()

            if id in prev_state.entities:
                prev_entity = next_state.entities[id]
            else:
                prev_entity = entity

            self.entities[id].interpolate(prev_entity, entity, alpha)

    def copy(self):
        new = Gamestate()

        new.entities = {id:entity.copy() for id, entity in self.entities.items()}
        new.next_entity_id = self.next_entity_id
        new.time = self.time

        return new

    # TODO: make serialize functions
    def serialize(self):
        bytestate = str()
        return bytestate

    def deserialize(self, bytestate):
        pass
