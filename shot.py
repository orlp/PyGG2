from __future__ import division

import pygame
from pygame.locals import *
from gameobject import Gameobject
from functions import point_direction, load_image

shotsprite = load_image("sprites/projectiles/shots/0.png")

class Shot(Gameobject):

    def __init__(self, root, x, y):
        Gameobject.__init__(self, root, x, y)
        
        self.lifealarm = 1.5
        self.damage = 8
        self.direction = 0

        # shotsprite contains the original sprite while image is the rotated image
        self.image = pygame.transform.rotate(self.shotsprite, self.direction)
        self.rect = self.image.get_rect()
        
        self.mask = pygame.mask.from_surface(self.image)

    def step(self, frametime):
        self.vspeed += 50 * frametime
        
        # calculate direction and recalculate data
        self.direction = point_direction(self.x - self.hspeed, self.y - self.vspeed, self.x, self.y)
        
        self.image = pygame.transform.rotate(self.shotsprite, self.direction)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
    def endstep(self, frametime):
        Gameobject.endstep(self, frametime)

        self.lifealarm -= frametime

        if self.root.collisionmap.mask.overlap(self.mask, (int(self.x), int(self.y))) or self.lifealarm <= 0:
            self.destroyinstance = True
