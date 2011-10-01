from __future__ import division

import pygame, math, random
from pygame.locals import *
from gameobject import GameObject
from functions import sign, place_free, point_direction, load_image
from shot import Shot

class Weapon(GameObject):
    def __init__(self, root, x, y):
        GameObject.__init__(self, root, x, y)

        self.owner = None
        self.firingSprite = None

        self.ammo = 0
        self.maxAmmo = 0
        self.justShot = False
        self.readyToShoot = True
        self.refireAlarm = 0

        self.direction = 0

    def step(self, frametime):
        if self.refireAlarm <= 0:
            self.refireAlarm = 0
            self.readyToShoot = True
        else:
            self.refireAlarm -= frametime

        if self.root.LMB and self.refireAlarm == 0:
            self.FirePrimary()

        if self.root.RMB and self.refireAlarm == 0:
            self.FireSecondary()

    def endStep(self, frametime):
        pass

    def posUpdate(self):
        self.x = self.owner.x
        self.y = self.owner.y
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.direction = point_direction(self.x, self.y, mouse_x + self.root.Xview, mouse_y + self.root.Yview)

    def FirePrimary(self):
        pass

    def FireSecondary(self):
        pass

    def draw(self):
        if not self.sprite: return

        oldsprite, oldrect = self.sprite, self.rect
        
        if self.justShot:
            self.sprite = self.firingSprite

        if self.owner.flip:
            self.sprite = pygame.transform.flip(self.sprite, 0, 1)

        self.sprite = pygame.transform.rotate(self.sprite, self.direction)
        self.rect = self.sprite.get_rect()
        
        GameObject.draw(self)
        
        self.sprite, self.rect = oldsprite, oldrect


class ScatterGun(Weapon):
    def __init__(self, root, x, y):
        Weapon.__init__(self, root, x, y)

        self.sprite = load_image("sprites/weapons/scatterguns/0.png")
        self.rect = (8, -2) + tuple(self.sprite.get_rect()[2:])
        self.firingSprite = load_image("sprites/weapons/scatterguns/2.png")

        self.maxAmmo = 6
        self.ammo = self.maxAmmo

        self.refireTime = 0.5
        self.reloadTime = 1

    def FirePrimary(self):
        for i in range(6):
            shot = Shot(self.root, self.x, self.y)
            shot.owner = self.owner
            shot.direction = self.direction + (7 - random.randint(0, 15))

            shot.speed = 100 + (20 - random.randint(0, 40))

            radDirection = math.radians(shot.direction)
            shot.hspeed = math.cos(radDirection) * shot.speed + self.owner.hspeed/2
            shot.vspeed = math.sin(radDirection) * -shot.speed

            shot.speed = math.hypot(shot.hspeed, shot.vspeed)
            self.refireAlarm = self.refireTime
            