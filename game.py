#!/usr/bin/env python

from __future__ import division, print_function

import math, pygame
from pygame.locals import *

import map
import character
import gamestate

# the central class
class Game:
    def __init__(self, window):
        self.window = window
    
        # constants
        self.view_width = self.window.width
        self.view_height = self.window.height
        
        # client rendering data
        self.xview = 0.0
        self.yview = 0.0
        self.overlayblits = [] # this list contains blits pending for the overlay
        
        # client input
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.leftmouse = False
        self.middlemouse = False
        self.rightmouse = False
        self.mouse_x = 0
        self.mouse_y = 0
        
        # map data
        self.map = map.Map(self, "twodforttwo_remix")
        self.backgroundcolor = pygame.Color(0, 0, 0)
        
        # game states
        self.current_state = gamestate.Gamestate()
        
        # TODO EDIT
        # start up by adding entities
        player = character.Scout(self, self.current_state)
        player.x = 2300
        player.y = 20
        
        # the object the camera should follow
        # deleting that object is undefined, use with care :D
        self.focus_object_id = player.id
        
        self.previous_state = self.current_state.copy()
        self.interpolated_state = self.previous_state.copy()
        
    def update(self, frametime):
        self.previous_state = self.current_state.copy()
        self.interpolated_state = self.previous_state.copy()
        self.current_state.update(self, frametime)

    def render(self, alpha, frametime):
        # calculate our interpolated state
        self.interpolated_state.interpolate(self.previous_state, self.current_state, alpha)
        
        # update view
        focus_object = self.interpolated_state.entities[self.focus_object_id]
        self.xview = int(int(focus_object.x) - self.view_width / 2)
        self.yview = int(self.view_height - int(focus_object.y) - self.view_height / 2)
        
        # clear screen if needed
        if focus_object.x <= self.view_width / 2 or focus_object.x + self.view_width >= self.map.image.width or focus_object.y <= self.view_height / 2 or self.yview + self.view_height >= self.map.image.height:
            self.window.clear()
            
        # draw background
        self.map.draw(self)
        
        # # draw entities
        # for entity in self.interpolated_state.entities.values(): entity.drawer.draw(self, self.interpolated_state, frametime)
        
        # # blit overlay last
        # for surface, offset in self.overlayblits:
            # surface.blit(*offset)
        # self.overlayblits = []
    
    def is_onscreen(self, objpos, objsize):
        return objpos[0] + objsize[0] - self.xview >= 0 and objpos[0] - objsize[0] - self.xview < self.view_width and objpos[1] + objsize[1] - self.yview >= 0 and objpos[1] - objsize[1] - self.yview < self.view_height