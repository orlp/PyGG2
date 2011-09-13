import pygame
from pygame.locals import *
from load_image import load_image
from gameobject import GameObject
from functions import sign, lengthdir, place_free, point_direction


class Weapon(GameObject):


    def __init__(self, root, x, y):

        GameObject.__init__(self, root, x, y)

        self.owner = -1

        self.firingSprite = -1

        self.ammo = 0
        self.maxAmmo = 0
        self.justShot = False
        self.readyToShoot = True
        self.refireAlarm = 0

        self.direction = 0


    def step(self):

        if self.refireAlarm <= 0:

            self.refireAlarm = 0
            self.readyToShoot = True


    def endStep(self):

        self.rect.topleft = (self.x-self.xRectOffset, self.y-self.yRectOffset)


    def posUpdate(self):

        self.x = self.owner.x
        self.y = self.owner.y


    def draw(self):

        if self.sprite == -1:
            return False

        if self.justShot:
            tempSprite = self.firingSprite.copy()
        else:
            tempSprite = self.sprite.copy()

#        self.sprite = pygame.transform.rotate(self.sprite, self.direction)
        GameObject.draw(self)
        self.sprite = tempSprite




class ScatterGun(Weapon):


    def __init__(self, root, x, y):

        Weapon.__init__(self, root, x, y)

        self.sprite, self.rect = load_image("Sprites/Weapons/Scattergun/ScatterGunS.png")
        self.firingSprite, unusedRect = load_image("Sprites/Weapons/Scattergun/ScatterGunS-firing.png")

        self.maxAmmo = 6
        self.ammo = self.maxAmmo

        self.refireTime = 20
        self.reloadTime = 15

        self.xImageOffset = -6
        self.yImageOffset = -6
