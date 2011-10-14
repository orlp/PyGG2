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
    
    # This is to replace the gmk "all" and also to update everything.
    GameObjectList = []
    
    Xview = 0
    Yview = 0
    
    def __init__(self):        
        # All drawing should be done on the Surface object
        self.Window = pygame.display.set_mode((800, 600), HWSURFACE | DOUBLEBUF)
        self.Surface = self.Window
        
        self.Wview = self.Window.get_width()
        self.Hview = self.Window.get_height()
        
        self.gameMap = map.Map(self)
        self.collisionMap = map.CollisionMap(self)
        self.Myself = character.Scout(self)
        
        self.clock = pygame.time.Clock()
        
        # text drawing is quite expensive, save it
        self.fps = 0
        self.fpstext = pygame.font.SysFont("None", 30).render("0 FPS", 0, (130, 130, 130))
        
    def update(self, frametime):        
        for obj in self.GameObjectList: obj.beginStep(frametime)
        for obj in self.GameObjectList: obj.step(frametime)
        for obj in self.GameObjectList: obj.endStep(frametime)

        self.GameObjectList = [obj for obj in self.GameObjectList if not obj.destroyInstance]

    def render(self):
        # get info
        self.Xview = self.Myself.x - self.Wview/2
        self.Yview = self.Myself.y - self.Hview/2
    
        # draw background
        self.Surface.fill((245, 245, 235))
        self.gameMap.draw()

        for obj in self.GameObjectList: obj.draw()
        
        # text drawing is quite expensive, save it
        newfps = int(self.clock.get_fps())
        if newfps != self.fps:
            self.fps = newfps
            self.fpstext = pygame.font.SysFont("None", 30).render("%d FPS" % self.fps, 0, (130, 130, 130))
        
        self.Surface.blit(self.fpstext, (10, 10))
        
        pygame.display.update()
