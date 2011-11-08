#!/usr/bin/env python

from __future__ import division, print_function

# this is the base class for drawer objects
class EntityDrawer(object):
    def __init__(self, game, state, entity_id):
        self.entity_id = entity_id
    
    def get_entity(self, state):
        return state.entities[self.entity_id]
    
    def draw(self, game, state, frametime): pass

# every entity should inherit from this
class Entity(object):
    Drawer = EntityDrawer
    
    def __init__(self, game, state):
        # create entity and register it
        self.id = state.next_entity_id        
        state.entities[self.id] = self
        state.next_entity_id += 1
        
        # assign drawer for this object
        if self.Drawer: self.drawer = self.Drawer(game, state, self.id)
        else: self.drawer = None
    
    def copy(self):
        cpobj = object.__new__(type(self))
        cpobj.__dict__.update(self.__dict__)
        return cpobj
    
    def destroy(self, state):
        del state.entities[self.id]
    
    # default member functions - notice the lack of
    # .interpolate(), .serialize(), .deserialize():
    # they are obligated and shouldn't just be added by inheritance
    def beginstep(self, game, state, frametime): pass
    def step(self, game, state, frametime): pass
    def endstep(self, game, state, frametime): pass

# simple object implementing movement
class MovingObject(Entity):
    def __init__(self, game, state):
        Entity.__init__(self, game, state)
        
        # x and y are the position of the actual object
        self.x = 0.0
        self.y = 0.0

        # hspeed and vspeed are the speeds of the object in respective directions
        self.hspeed = 0.0
        self.vspeed = 0.0
        
    def endstep(self, game, state, frametime):
        # first move
        self.x += self.hspeed * frametime
        self.y += self.vspeed * frametime

    def interpolate(self, prev_obj, next_obj, alpha):
        self.x = prev_obj.x * (1 - alpha) + next_obj.x * alpha
        self.y = prev_obj.y * (1 - alpha) + next_obj.y * alpha
        