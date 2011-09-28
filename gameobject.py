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

        self.oldX = xpos
        self.oldY = ypos

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

        self.x += self.hspeed * (frametime / 1000.0)
        self.y += self.vspeed * (frametime / 1000.0)
        
        if self.rect:
            self.rect.topleft = (self.x - self.xRectOffset, self.y - self.yRectOffset)

    def collide(self):
        self.oldX = self.x
        self.oldY = self.y

    def draw(self):
        if self.sprite:
            self.root.Surface.blit(self.sprite, (self.x + self.xImageOffset - self.root.Xview, self.y + self.yImageOffset - self.root.Yview))

    def destroy(self):
        self.root.GameObjectList.remove(self)

            
class MapObject(GameObject):
    def __init__(self, root):
        GameObject.__init__(self, root, 0, 0)

        self.sprite = pygame.image.load("Maps/MapTesting.png")
        self.sprite.convert_alpha()
        self.sprite.convert()
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width()*6, self.sprite.get_height()*6))

        self.rect = pygame.Rect(0, 0, self.sprite.get_width(), self.sprite.get_height())
        self.root.Surface.blit(self.sprite, (0, 0))
        self.mask = pygame.mask.from_surface(self.sprite)
        
        self.root.map = self

    def draw(self):
        self.root.Surface.blit(self.sprite, (-self.root.Xview, -self.root.Yview))


class PlayerControl(GameObject):
    def __init__(self, root):
        GameObject.__init__(self, root, 0, 0)

    def beginStep(self, frametime):
        up = 0
        left = 0
        right = 0
        LMB = 0
        RMB = 0

        key = pygame.key.get_pressed()
        if key[K_w]: up = 1
        if key[K_a]: left = 1
        elif key[K_d]: right = 1

        LMB, middleMouseButton, RMB = pygame.mouse.get_pressed()

        # Send keybyte
        self.root.Myself.up = up
        self.root.Myself.left = left
        self.root.Myself.right = right
        self.root.Myself.LMB = LMB
        self.root.Myself.RMB = RMB
