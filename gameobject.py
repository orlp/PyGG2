from __future__ import division

import pygame
from pygame.locals import *
from functions import sign, place_free, point_direction
import math

class Gameobject(pygame.sprite.Sprite):
    def __init__(self, root, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)

        self.root = root

        self.x = xpos
        self.y = ypos

        self.hspeed = 0
        self.vspeed = 0

        self.image = None
        self.rect = (0, 0, 0, 0)

        self.root.gameobjects.append(self)
        self.destroyinstance = False

    def beginstep(self, frametime):
        pass

    def step(self, frametime):
        pass

    def endstep(self, frametime):
        self.x += self.hspeed * frametime
        self.y += self.vspeed * frametime
        
        self.x = max(self.x, 0)
        self.y = max(self.y, 0)

    def destroy(self, frametime):
        pass

    def draw(self):
        if self.image:
            x, y = int(self.x), int(self.y)
            xoff, yoff = self.rect[0:2]
            xview, yview = int(self.root.xview), int(self.root.yview)
            
            # range checking - TODO consider sprite heigth/width
            if x >= xview and x < xview + self.root.wview and y >= yview and y < yview + self.root.hview:
                self.root.surface.blit(self.image, (x - xoff - xview, y - yoff - yview))
    
    def destroy(self):
        pass
