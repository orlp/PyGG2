from __future__ import division

import pygame
from pygame.locals import *
from gameobject import GameObject
from functions import point_direction, load_image

class Shot(GameObject):
    def __init__(self, root, x, y):
        GameObject.__init__(self, root, x, y)
        
        self.lifeAlarm = 1.5
        self.direction = 0
        self.damage = 8

        self.image = load_image("sprites/projectiles/shots/0.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.Mask((self.rect.width, self.rect.height))
        self.mask.fill()

    def step(self, frametime):
        self.vspeed += 50 * frametime
        
        self.direction = point_direction(self.x - self.hspeed, self.y - self.vspeed, self.x, self.y)

    def endStep(self, frametime):
        GameObject.endStep(self, frametime)

        self.lifeAlarm -= frametime

        if self.root.collisionMap.mask.overlap(self.mask, (int(self.x), int(self.y))) or self.lifeAlarm <= 0:
            self.destroyInstance = True

    def draw(self):
        origsprite, origrect = self.image, self.rect
    
        self.image = pygame.transform.rotate(self.image, self.direction)
        self.rect = self.image.get_rect()
        
        GameObject.draw(self)
        
        self.image, self.rect = origsprite, origrect
