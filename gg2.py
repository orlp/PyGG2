#!/usr/bin/env python

from __future__ import division, print_function

import math, pygame
from pygame.locals import *

import map
import character
import gamestate

# the central class
class GG2:
    def __init__(self):
        self.window = pygame.display.get_surface()

        # constants
        self.view_width = self.window.get_width()
        self.view_height = self.window.get_height()

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
        player.x = 2400
        player.y = 50
        
        # the object the camera should follow
        # deleting that object is undefined, use with care :D
        self.focus_object_id = player.id
        
        self.previous_state = self.current_state.copy()
        self.interpolated_state = self.previous_state.copy()

    def sendinput(self):
        # Set Character input to this, later on we'll also send stuff here to the server.
        self.focus_object_id.up = self.up
        self.focus_object_id.down = self.down
        self.focus_object_id.left = self.left
        self.focus_object_id.right = self.right
        self.focus_object_id.leftmouse = self.leftmouse
        self.focus_object_id.middlemouse = self.middlemouse
        self.focus_object_id.rightmouse = self.rightmouse
        
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
        self.yview = int(int(focus_object.y) - self.view_height / 2)
        
        # clear screen if needed
        if focus_object.x <= self.view_width / 2 or focus_object.x + self.view_width >= self.map.image.get_width() or focus_object.y <= self.view_height / 2 or self.yview + self.view_height >= self.map.image.get_height():
            self.window.fill(self.backgroundcolor)
            
        # draw background
        self.map.draw(self)
        
        # draw entities
        for entity in self.interpolated_state.entities.values(): entity.drawer.draw(self, self.interpolated_state, frametime)
        
        # blit overlay last
        for surface, offset in self.overlayblits:
            self.window.blit(surface, offset)
        self.overlayblits = []
    
    def is_onscreen(self, objpos, objsize):
        return objpos[0] + objsize[0] - self.xview >= 0 and objpos[0] - objsize[0] - self.xview < self.view_width and objpos[1] + objsize[1] - self.yview >= 0 and objpos[1] - objsize[1] - self.yview < self.view_height
    
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
