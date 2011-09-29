from __future__ import division

import pygame
from pygame.locals import *
from gameobject import GameObject
from collision import objectCheckCollision
from functions import load_image, point_direction

class Shot(GameObject):
    def __init__(self, root, x, y):
        GameObject.__init__(self, root, x, y)

        self.lifeAlarm = 0
        self.direction = 0

        self.sprite, self.rect = load_image("Sprites/Projectiles/Shot.png")

    def step(self, frametime):
        self.vspeed += 5 * frametime

    def collide(self, frametime):
        GameObject.collide(self, frametime)

        if objectCheckCollision(self):
            self.destroyInstance = True

    def draw(self):
        self.direction = point_direction(self.x - self.hspeed, self.y - self.vspeed, self.x, self.y)

        tempSprite = self.sprite.copy()
        tempSprite = pygame.transform.rotate(self.sprite, self.direction)
        self.root.Surface.blit(tempSprite, (self.x + self.xImageOffset - self.root.Xview, self.rect.top + self.yImageOffset - self.root.Yview))
