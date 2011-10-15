from __future__ import division

import pygame
from pygame.locals import *

import map
import character
import math

class GG2:
    """
    Central class
    """
    
    def __init__(self):        
        # All drawing should be done on the surface object
        self.window = pygame.display.set_mode((800, 600), HWSURFACE | DOUBLEBUF)
        self.surface = self.window
        
        self.wview = self.window.get_width()
        self.hview = self.window.get_height()
        self.xview = 0
        self.yview = 0
        
        self.gameobjects = []
        self.gamemap = map.Map(self)
        self.collisionmap = map.Collisionmap(self)
        self.myself = character.Scout(self)
        
        self.clock = pygame.time.Clock()
        
        # text drawing is quite expensive, save it
        self.fps = 0
        self.fpstext = pygame.font.SysFont("None", 30).render("0 FPS", 0, (130, 130, 130))
        
    def update(self, frametime):        
        for obj in self.gameobjects: obj.beginstep(frametime)
        for obj in self.gameobjects: obj.step(frametime)
        for obj in self.gameobjects: obj.endstep(frametime)

        for obj in self.gameobjects:
            if obj.destroyinstance: obj.destroy()
        self.gameobjects = [obj for obj in self.gameobjects if not obj.destroyinstance]

    def render(self):
        # get info
        self.xview = self.myself.x - self.wview/2
        self.yview = self.myself.y - self.hview/2
    
        # draw background
        self.surface.fill((0, 0, 0))
        self.gamemap.draw()

        for obj in self.gameobjects: obj.draw()
        
        # text drawing is quite expensive, save it
        newfps = int(self.clock.get_fps())
        if newfps != self.fps:
            self.fps = newfps
            self.fpstext = pygame.font.SysFont("None", 30).render("%d FPS" % self.fps, 0, (130, 130, 130))
        
        self.surface.blit(self.fpstext, (10, 10))
        
        pygame.display.update()
