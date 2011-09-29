from __future__ import division

import pygame
from pygame.locals import *
from gameobject import GameObject
from collision import objectCheckCollision
from functions import point_direction, load_image

class Shot(GameObject):
    def __init__(self, root, x, y):
        GameObject.__init__(self, root, x, y)
        
        self.lifeAlarm = 0
        self.direction = 0

        self.sprite = load_image("Sprites/Projectiles/ShotS/0.png")
        self.rect = self.sprite.get_rect()

    def step(self, frametime):
        self.vspeed += 50 * frametime
        
        self.direction = point_direction(self.x - self.hspeed, self.y - self.vspeed, self.x, self.y)

    def collide(self, frametime):
        GameObject.collide(self, frametime)

        if objectCheckCollision(self):
            self.destroyInstance = True

    def draw(self):
        tmpsprite = pygame.transform.rotate(self.sprite, self.direction)
        self.rect = tmpsprite.get_rect()
        self.root.Surface.blit(tmpsprite, (self.x + self.xImageOffset - self.root.Xview, self.y + self.yImageOffset - self.root.Yview))
