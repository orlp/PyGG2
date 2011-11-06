#!/usr/bin/env python

from __future__ import division, print_function

import pygame, math
from pygame.locals import *

import random

import entity
import function
import projectile

# abstract class, don't directly instantiate
class Weapon(entity.Entity):
    def __init__(self, game, state, owner):
        super(Weapon, self).__init__(game, state)

        self.owner = owner
        self.refirealarm = 0.0
        self.direction = 0.0
        self.ammo = self.maxammo

    def step(self, game, state, frametime):
        owner = state.get_entity(self.owner)
    
        # get angle of cursor relative to the horizontal axis, increasing counter-clockwise
        self.direction = function.point_direction(int(owner.x), int(owner.y), game.mousepos[0] + game.xview, game.mousepos[1] + game.yview)
        
        if self.refirealarm <= 0:
            self.refirealarm = 0.0
        else:
            self.refirealarm -= frametime

        if game.leftmouse and self.refirealarm == 0:
            self.fire_primary(game, state)

        if game.rightmouse and self.refirealarm == 0:
            self.fire_secondary(game, state)

    # override this
    def fire_primary(self, game, state): pass
    def fire_secondary(self, game, state): pass
    
    def interpolate(self, next_object, alpha):
        self.direction = function.interpolate_angle(self.direction, next_object.direction, alpha)

class ScattergunDrawer(entity.EntityDrawer):
    weapon_rotate_point = (6, 2) # where is the handle of the gun, where to rotate around
    weaponoffset = (10, 8) # where the character should carry it's gun
    weaponoffset_flipped = (8, 6)
    
    def __init__(self, game, state, entity_id):
        super(ScattergunDrawer, self).__init__(game, state, entity_id)
        
        self.weaponsprite = function.load_image("weapons/scatterguns/0")
        self.firingsprite = function.load_image("weapons/scatterguns/2")
        
    def draw(self, game, state):
        weapon = state.get_entity(self.entity_id)
        owner = state.get_entity(weapon.owner)
        
        image = self.weaponsprite
        offset = self.weaponoffset
        
        if weapon.refiretime - weapon.refirealarm < 0.1:
            image = self.firingsprite
            
        if owner.flip:
            image = pygame.transform.flip(image, 0, 1)
            offset = self.weaponoffset_flipped
        
        # get starting offset
        xoff, yoff = owner.x, owner.y
        xoff += offset[0]
        yoff += offset[1]
        
        xoff, yoff = int(xoff), int(yoff)
        
        # rotate 
        image, offset = function.rotate_surface_point(image, weapon.direction, self.weapon_rotate_point)
        
        # compensate for rotation
        xoff -= offset[0]
        yoff -= offset[1]
        
        game.draw_world(image, (xoff, yoff))

class Scattergun(Weapon):
    Drawer = ScattergunDrawer

    maxammo = 6
    refiretime = 0.5
    reloadtime = 1
    
    def fire_primary(self, game, state):
        for i in range(6):
            projectile.Shot(game, state, self.id)
        
        self.refirealarm = self.refiretime