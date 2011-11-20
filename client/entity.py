from __future__ import division, print_function

# this is the base class for drawer objects
class EntityRenderer(object):
    def __init__(self, renderer, state, entity_id):
        self.entity_id = entity_id
    
    def get_entity(self, state):
        return state.entities[self.entity_id]
    
    def render(self, renderer, state, frametime): pass