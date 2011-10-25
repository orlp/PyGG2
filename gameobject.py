from __future__ import division

import pygame
from pygame.locals import *
from functions import sign, point_direction
import math

class Gameobject(pygame.sprite.Sprite):
    def __init__(self, root, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)
        
        # every game object has a root, this root will point to the GG2 object containing the object
        self.root = root
        
        # x and y are the position of the actual object
        self.x = float(xpos)
        self.y = float(ypos)

        # hspeed and vspeed are the speeds of the object in respective directions
        self.hspeed = 0.0
        self.vspeed = 0.0
        
        # every game object has to have an image and rect attribute
        # the image attribute should contain either None (undrawable) or a pygame.Surface object
        # the rect consists of (offsetx, offsety, width, height) - offsetx and offsety are used for drawing
        # the image will be drawn on (x + offsetx, y + offsety)
        # the width and height are the width and height of the actual object, and thus should be used for things like collision detection
        self.image = None
        self.rect = pygame.Rect(0, 0, 0, 0)

        # to destroy a gameobject, simply set it's destroyinstance attribute to True and it will be destroyed in the next cleanup round - fire and forget
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
            
            # calculate drawing position
            draw_x = int(self.x + self.rect.left - self.root.xview + additional_offset_x)
            draw_y = int(self.y + self.rect.top - self.root.yview + additional_offset_y)
            
            # even if we see a tiny little bit of the object, blit it - otherwise don't even blit
            if draw_x + width >= 0 and draw_x - width < self.root.view_width and draw_y + height >= 0 and draw_y - height < self.root.view_height:
                self.root.surface.blit(self.image, (draw_x, draw_y))
    
    def destroy(self):
        pass
