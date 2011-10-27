from __future__ import division

import pygame, math
from pygame.locals import *

import random

import gameobject
import function
import shot

# abstract class, don't directly instantiate
class Weapon(gameobject.Gameobject):
    def __init__(self, game, state, owner):
        gameobject.Gameobject.__init__(self, game, state)

        self.owner = owner
        self.refirealarm = 0.0
        self.direction = 0.0
        self.ammo = self.maxammo
        
        self.posupdate(game, state)

    def step(self, game, state, frametime):
        # get angle of cursor relative to the horizontal axis, increasing counter-clockwise
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.direction = function.point_direction(int(self.x), int(self.y), mouse_x + game.xview, mouse_y + game.yview)
        
        if self.refirealarm <= 0:
            self.refirealarm = 0.0
        else:
            self.refirealarm -= frametime

        if game.leftmouse and self.refirealarm == 0:
            self.fire_primary(game, state)

        if game.rightmouse and self.refirealarm == 0:
            self.fire_secondary(game, state)

    def posupdate(self, game, state):
        self.x = state.entities[self.owner].x
        self.y = state.entities[self.owner].y

    # override this
    def fire_primary(self): pass
    def fire_secondary(self): pass

    def draw(self, game, state, surface):
        image = self.weaponsprite
        if self.refiretime - self.refirealarm < 0.1:
            image = self.firingsprite
        
        if state.entities[self.owner].flip:
            image = pygame.transform.flip(image, 0, 1)
        
        # get starting offset
        owner = state.entities[self.owner]
        xoff, yoff = owner.x, owner.y
        xoff += owner.weaponoffset[0]
        yoff += owner.weaponoffset[1]
        
        # rotate
        image, offset = function.rotate_surface_point(image, self.direction, self.weapon_rotate_point)
        
        # compensate for rotation
        xoff -= offset[0]
        yoff -= offset[1]
        
        game.draw_in_view(image, (xoff, yoff))
    
    def interpolate(self, next_object, alpha):
        gameobject.Gameobject.interpolate(self, next_object, alpha)
        self.direction = self.direction * (1 - alpha) + next_object.direction * alpha

class Scattergun(Weapon):
    weaponsprite = function.load_image("sprites/weapons/scatterguns/0.png")
    firingsprite = function.load_image("sprites/weapons/scatterguns/2.png")
    
    weapon_rotate_point = (4, 8) # where is the handle of the gun, where to rotate around
    maxammo = 6
    refiretime = 0.5
    reloadtime = 1
    
    def fire_primary(self, game, state):
        for i in range(6):
            shot.Shot(game, state, self.id)
        
        self.refirealarm = self.refiretime

"""
class Shotgun(Weapon):
    def __init__(self, root, owner, x, y):
        Weapon.__init__(self, root, owner, x, y)

        self.weaponsprite = load_image("sprites/weapons/shotguns/0.png")
        self.firingsprite = load_image("sprites/weapons/shotguns/2.png")
        self.rect = pygame.Rect((8, -2), tuple(self.weaponsprite.get_rect()[2:])) # TODO correct offsets

        self.maxammo = 8
        self.ammo = self.maxammo

        self.refiretime = 0.5
        self.reloadtime = 2/3

    def fire_primary(self):
        for i in range(4):
            shot = Shot(self.root, self.x, self.y)
            shot.owner = self.owner
            shot.direction = self.direction + random.randint(0, 11)-7

            shot.speed = 300 + (20 - random.randint(0, 40))# TODO: Put the correct speed

            raddirection = math.radians(shot.direction)
            shot.hspeed = math.cos(raddirection) * shot.speed + self.owner.hspeed/2
            shot.vspeed = math.sin(raddirection) * -shot.speed

            shot.speed = math.hypot(shot.hspeed, shot.vspeed) # nightcracker - Why are we recalculating bullet speed?
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

        shot.speed = math.hypot(shot.hspeed, shot.vspeed) # nightcracker - Why are we recalculating bullet speed?
        self.refirealarm = self.refiretime
"""