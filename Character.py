import pygame
from pygame.locals import *
from load_image import load_image
from collision import characterHitObstacle, objectCheckCollision
from gameobject import GameObject
from functions import sign, place_free, lengthdir

class Character(GameObject):

    def __init__(self, root):

        GameObject.__init__(self, root, 400, 400)
        self.up, self.left, self.right, self.LMB, self.RMB = 0, 0, 0, 0, 0


    def step(self):

        if self.up:
            self.vspeed -= 2

        if self.left:
            self.hspeed -= 1
        elif self.right:
            self.hspeed += 1


        self.vspeed += 0.2

        if self.vspeed > 5:
            self.vspeed = 5
        elif self.vspeed < -5:
            self.vspeed = -5

        if self.hspeed > 5:
            self.hspeed = 5
        elif self.hspeed < -5:
            self.hspeed = -5


    def collide(self):

        check = objectCheckCollision(self)

        if check:
            characterHitObstacle(self)

        GameObject.collide(self)









class Scout(Character):

    def __init__(self, root):

        Character.__init__(self, root)

        self.sprite, self.rect = load_image('Sprites/Characters/Scout/Red/ScoutRedS_fr1.png')

        # The Scout hitbox: left = -6; right = 6; top = -10; bottom = 23
        self.rect = pygame.Rect(self.x-6, self.y-10, 12, 33)

        self.xImageOffset = -30
        self.yImageOffset = -30

        self.xRectOffset = self.x-self.rect.centerx
        self.yRectOffset = self.y-self.rect.centery
