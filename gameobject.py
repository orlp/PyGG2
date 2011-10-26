from __future__ import division

import pygame
from pygame.locals import *
from functions import sign, point_direction
import math

class Gameobject():
    def __init__(self, xpos = 0.0, ypos = 0.0, hspeed = 0.0, vspeed = 0.0):
        # x and y are the position of the actual object
        self.x = float(xpos)
        self.y = float(ypos)

        # hspeed and vspeed are the speeds of the object in respective directions
        self.hspeed = float(hspeed)
        self.vspeed = float(vspeed)

        # if this is true the object will be destroyed next round
        self.destroyinstance = False

    def beginstep(self, state, frametime):
        pass

    def step(self, state, frametime):
        pass

    def endstep(self, state, frametime):
        self.x += self.hspeed * frametime
        self.y += self.vspeed * frametime
        
        self.x = max(self.x, 0)
        self.y = max(self.y, 0)

    def draw(self, state, offset_x = 0, offset_y = 0):
        if self.image:
            width, height = self.image.get_rect().size
            
            # calculate drawing position
            draw_x = int(self.x + self.rect.left - self.root.xview + additional_offset_x)
            draw_y = int(self.y + self.rect.top - self.root.yview + additional_offset_y)
            
            # even if we see a tiny little bit of the object, blit it - otherwise don't even blit
            if draw_x + width >= 0 and draw_x - width < self.root.view_width and draw_y + height >= 0 and draw_y - height < self.root.view_height:
                self.root.surface.blit(self.image, (draw_x, draw_y))
    
    def destroy(self):
        self.destroyinstance = True
