from __future__ import division

import pygame
from pygame.locals import *
from functions import sign, point_direction
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
        self.rect = pygame.Rect(0, 0, 0, 0)

        self.destroyinstance = False
        self.root.gameobjects.append(self)

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

    def draw(self, additional_offset_x = 0, additional_offset_y = 0):
        if self.image:
            width, height = self.image.get_rect().size
            
            draw_x = int(self.x + self.rect.left - self.root.xview + additional_offset_x)
            draw_y = int(self.y + self.rect.top - self.root.yview + additional_offset_y)
            
            if draw_x + width >= 0 and draw_x - width < self.root.view_width and draw_y + height >= 0 and draw_y - height < self.root.view_height:
                self.root.surface.blit(self.image, (draw_x, draw_y))
    
    def destroy(self):
        pass
