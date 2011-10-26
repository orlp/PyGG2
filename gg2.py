from __future__ import division

import pygame
from pygame.locals import *

import map
import character
import math
import gamestate

class GG2:
    """
    Central class
    """
    
    def __init__(self):        
        # All drawing should be done on the surface object
        self.window = pygame.display.set_mode((800, 600), HWSURFACE | DOUBLEBUF) # use HWSURFACE in the case it helps, and DOUBLEBUF to prevent screen tearing
        self.surface = self.window
        
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
        
        # game objects
        self.previous_state = gamestate.Gamestate()
        self.current_state = gamestate.Gamestate()
        self.myself = character.Scout(self)
        
    def update(self, frametime):
        self.previous_state = self.current_state.copy()
        self.current_state.update(frametime)

    def render(self):
        # update view
        self.xview = int(self.myself.x) - self.view_width / 2
        self.yview = int(self.myself.y) - self.view_height / 2
    
        # draw background
        self.surface.fill(self.backgroundcolor)
        self.gamemap.draw()
        
        # draw objects
        for obj in self.gameobjects: obj.draw()
        
        pygame.display.update()