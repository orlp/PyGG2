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
        self.window = pygame.display.get_surface()
        
        # constants
        self.view_width = self.window.get_width()
        self.view_height = self.window.get_height()
        
        # client rendering data
        self.xview = 0.0
        self.yview = 0.0
        self.overlayblits = [] # this list contains blits pending for the overlay
        
        # map data
        self.gamemap = map.Map(self, "twodforttwo_remix")
        self.collisionmap = map.Collisionmap(self, "twodforttwo_remix")
        self.backgroundcolor = pygame.Color(0, 0, 0)
        
        # game states
        self.current_state = gamestate.Gamestate()
        
        # TODO EDIT
        # start up by adding entities
        player = character.Scout(self, self.current_state)
        player.x = 2400
        player.y = 50
        
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
        focus_object = interpolated_state.entities[self.focus_object_id]
        self.xview = int(int(focus_object.x) - self.view_width / 2)
        self.yview = int(int(focus_object.y) - self.view_height / 2)
    
        # draw background
        self.window.fill(self.backgroundcolor)
        self.gamemap.draw(self)
        
        # draw entities
        for entity in interpolated_state.entities.values(): entity.draw(self, interpolated_state, self.window)
        
        # blit overlay last
        for surface, offset in self.overlayblits:
            self.window.blit(surface, offset)
        self.overlayblits = []
        
        # and display it to the user
        pygame.display.update()
    
    # this function is called to draw on the game's window with game world coordinate
    def draw_world(self, surface, offset = (0, 0)):
        width, height = surface.get_size()
        
        # calculate drawing position
        draw_x = int(offset[0] - self.xview)
        draw_y = int(offset[1] - self.yview)
        
        # even if we see a tiny little bit of the object, blit it - otherwise don't even blit
        if draw_x + width >= 0 and draw_x - width < self.view_width and draw_y + height >= 0 and draw_y - height < self.view_height:
            self.window.blit(surface, (draw_x, draw_y))
    
    # this function is called to draw over the game world with screen coordinates
    def draw_overlay(self, surface, offset = (0, 0)):
        width, height = surface.get_size()
        
        if offset[0] + width >= 0 and offset[0] - width < self.view_width and offset[1] + height >= 0 and offset[1] - height < self.view_height:
            self.overlayblits.append((surface, offset))
    
    