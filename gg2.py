from __future__ import division

import math, pygame
from pygame.locals import *

import map
import character
import gamestate

class GG2:
    """
    Central class
    """
    
    def __init__(self):        
        # All drawing should be done on the surface object
        self.window = pygame.display.set_mode((800, 600), HWSURFACE | DOUBLEBUF) # use HWSURFACE in the case it helps, and DOUBLEBUF to prevent screen tearing
        
        # constants
        self.view_width = self.window.get_width()
        self.view_height = self.window.get_height()
        
        # client rendering data
        self.xview = 0.0
        self.yview = 0.0
        
        # map data
        self.gamemap = map.Map(self, "twodforttwo_remix")
        self.collisionmap = map.Collisionmap(self, "twodforttwo_remix")
        self.backgroundcolor = pygame.Color(0, 0, 0)
        
        # game states
        self.current_state = gamestate.Gamestate()
        
        # TODO EDIT
        # start up by adding entities
        player = character.Scout(self, self.current_state)
        
        # the object the camera should follow
        # deleting it is undefined, use with care :D
        self.focus_object_id = player.id
        
        self.previous_state = self.current_state.copy()
        
    def update(self, frametime):
        self.previous_state = self.current_state.copy()
        self.current_state.update(self, frametime)

    def render(self, alpha):
        # get our interpolated state
        interpolated_state = self.previous_state.interpolate(self.current_state, alpha)
        
        # update view
        focus_object = interpolated_state[self.focus_object_id]
        self.xview = int(focus_object.x) - self.view_width / 2
        self.yview = int(focus_object.y) - self.view_height / 2
    
        # draw background
        self.window.fill(self.backgroundcolor)
        self.gamemap.draw()
        
        # draw entities
        for entity in interpolated_state.entities: entity.draw(self, interpolated_state, self.window)
        
        # and display it to the user
        pygame.display.update()
    
    # this function is called to draw on the game's window
    def draw_in_view(game, surface, offset_x = 0, offset_y = 0):
        width, height = surface.get_size()
        
        # calculate drawing position
        draw_x = int(offset_x - game.xview)
        draw_y = int(offset_y - game.yview)
        
        # even if we see a tiny little bit of the object, blit it - otherwise don't even blit
        if draw_x + width >= 0 and draw_x - width < game.view_width and draw_y + height >= 0 and draw_y - height < game.view_height:
            game.window.blit(surface, (draw_x, draw_y))