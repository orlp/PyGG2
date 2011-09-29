from __future__ import division

import pygame
from pygame.locals import *
from collision import characterHitObstacle, objectCheckCollision
from functions import sign, place_free, point_direction

class GameObject(pygame.sprite.Sprite):
    def __init__(self, root, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)

        self.root = root

        self.x = xpos
        self.y = ypos

        self.hspeed = 0
        self.vspeed = 0

        self.sprite = None
        self.rect = None

        self.xImageOffset = 0
        self.yImageOffset = 0

        self.xRectOffset = 0
        self.yRectOffset = 0

        self.root.GameObjectList.append(self)
        self.destroyInstance = False

    def beginStep(self, frametime):
        pass

    def step(self, frametime):
        pass

    def endStep(self, frametime):
        self.x = max(self.x, 0)
        self.y = max(self.y, 0)

        self.x += self.hspeed * frametime
        self.y += self.vspeed * frametime

    def draw(self):
        if self.sprite:
            self.root.Surface.blit(self.sprite, (self.x + self.xImageOffset - self.root.Xview, self.y + self.yImageOffset - self.root.Yview))

    def destroy(self):
        self.root.GameObjectList.remove(self)
