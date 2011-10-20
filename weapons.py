from __future__ import division

import pygame, math, random
from pygame.locals import *
from gameobject import Gameobject
from functions import sign, place_free, point_direction, load_image
from shot import Shot

class Weapon(Gameobject):
    def __init__(self, root, owner, x, y):
        Gameobject.__init__(self, root, x, y)

        self.owner = owner
        
        # weaponsprite contains the original sprite while image is the rotated image
        # firingsprite is the sprite to be shown while firing

        self.ammo = 0
        self.maxammo = 0
        self.refirealarm = 0

        self.direction = 0

    def step(self, frametime):
        if self.refirealarm <= 0:
            self.refirealarm = 0
        else:
            self.refirealarm -= frametime

        if self.root.leftmouse and self.refirealarm == 0:
            self.fire_primary()

        if self.root.rightmouse and self.refirealarm == 0:
            self.fire_secondary()

    def endstep(self, frametime):
        pass

    def posupdate(self):
        self.x = self.owner.x
        self.y = self.owner.y

    def fire_primary(self):
        pass

    def fire_secondary(self):
        pass

    def draw(self):        
        if self.refiretime - self.refirealarm < 0.1:
            self.image = self.firingsprite
        else:
            self.image = self.weaponsprite

        if self.owner.flip:
            self.image = pygame.transform.flip(self.image, 0, 1)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.direction = point_direction(self.x, self.y, mouse_x + self.root.xview, mouse_y + self.root.yview)
        
        # store width before rotating
        oldw, oldh = self.image.get_rect().size
        self.image = pygame.transform.rotate(self.image, self.direction)
        
        # get offset from rotating
        offx, offy = self.image.get_rect().width - oldw, self.image.get_rect().height - oldh
        
        # store original offset
        origx, origy = self.rect.topleft
        
        #print(self.direction)
        self.rect.top -= self.image.get_rect().width * math.sin(math.radians(self.direction))
        
        Gameobject.draw(self)
        xview, yview = int(self.root.xview), int(self.root.yview)
        self.root.surface.set_at((int(self.x) - xview, int(self.y)  - yview), (255, 0, 255))
        
        # restore original offset
        self.rect.topleft = (origx, origy)
        
        Gameobject.draw(self)

class Scattergun(Weapon):
    def __init__(self, root, owner, x, y):
        Weapon.__init__(self, root, owner, x, y)

        self.weaponsprite = load_image("sprites/weapons/scatterguns/0.png")
        self.firingsprite = load_image("sprites/weapons/scatterguns/2.png")
        self.rect = pygame.Rect((0, 0), tuple(self.weaponsprite.get_rect()[2:]))

        self.maxammo = 6
        self.ammo = self.maxammo

        self.refiretime = 0.5
        self.reloadtime = 1

    def fire_primary(self):
        for i in range(6):
            shot = Shot(self.root, self.x, self.y)
            shot.owner = self.owner
            shot.direction = self.direction + (7 - random.randint(0, 15))

            shot.speed = 300 + (20 - random.randint(0, 40))# TODO: Put the correct speed

            raddirection = math.radians(shot.direction)
            shot.hspeed = math.cos(raddirection) * shot.speed + self.owner.hspeed/2
            shot.vspeed = math.sin(raddirection) * -shot.speed

            shot.speed = math.hypot(shot.hspeed, shot.vspeed)
            self.refirealarm = self.refiretime


class Shotgun(Weapon):
    def __init__(self, root, owner, x, y):
        Weapon.__init__(self, root, owner, x, y)

        self.weaponsprite = load_image("sprites/weapons/shotguns/0.png")
        self.firingsprite = load_image("sprites/weapons/shotguns/2.png")
        self.rect = pygame.Rect((8, -2), tuple(self.weaponsprite.get_rect()[2:])) # TODO correct offsets

        self.maxammo = 8
        self.ammo = self.maxammo

        self.refiretime = 0.5
        self.reloadtime = 0.66# 2/3

    def fire_primary(self):
        for i in range(4):
            shot = Shot(self.root, self.x, self.y)
            shot.owner = self.owner
            shot.direction = self.direction + random.randint(0, 11)-7

            shot.speed = 300 + (20 - random.randint(0, 40))# TODO: Put the correct speed

            raddirection = math.radians(shot.direction)
            shot.hspeed = math.cos(raddirection) * shot.speed + self.owner.hspeed/2
            shot.vspeed = math.sin(raddirection) * -shot.speed

            shot.speed = math.hypot(shot.hspeed, shot.vspeed)
            self.refirealarm = self.refiretime


class Revolver(Weapon):
    def __init__(self, root, owner, x, y):
        Weapon.__init__(self, root, owner, x, y)

        self.weaponsprite = load_image("sprites/weapons/revolvers/0.png")
        self.firingsprite = load_image("sprites/weapons/revolvers/2.png")
        self.rect = pygame.Rect((8, -2), tuple(self.weaponsprite.get_rect()[2:])) # TODO correct offsets

        self.maxammo = 6
        self.ammo = self.maxammo

        self.refiretime = 0.6
        self.reloadTime = 0.5

    def fire_primary(self):
        shot = Shot(self.root, self.x, self.y)
        shot.owner = self.owner
        shot.direction = self.direction + random.randint(0, 1)-2

        shot.speed = 300 + (20 - random.randint(0, 40)) # TODO: Put the correct speed

        shot.damage = 28

        raddirection = math.radians(shot.direction)
        shot.hspeed = math.cos(raddirection) * shot.speed
        shot.vspeed = math.sin(raddirection) * -shot.speed

        shot.speed = math.hypot(shot.hspeed, shot.vspeed)
        self.refirealarm = self.refiretime
