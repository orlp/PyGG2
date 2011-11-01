from __future__ import division, print_function

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
    def fire_primary(self, game, state): pass
    def fire_secondary(self, game, state): pass

    def draw(self, game, state, surface):
        owner = state.entities[self.owner]
        
        image = self.weaponsprite
        offset = owner.weaponoffset
        
        if self.refiretime - self.refirealarm < 0.1:
            image = self.firingsprite
            
        if owner.flip:
            image = pygame.transform.flip(image, 0, 1)
            offset = owner.weaponoffset_flipped
        
        
        # get starting offset
        xoff, yoff = owner.x, owner.y
        xoff += offset[0]
        yoff += offset[1]
        
        xoff, yoff = int(xoff), int(yoff)
        
        # rotate 
        image, offset = function.rotate_surface_point(image, self.direction, self.weapon_rotate_point)
        
        # compensate for rotation
        xoff -= offset[0]
        yoff -= offset[1]
        
        game.draw_world(image, (xoff, yoff))
    
    def interpolate(self, next_object, alpha):
        gameobject.Gameobject.interpolate(self, next_object, alpha)
        self.direction = function.interpolate_angle(self.direction, next_object.direction, alpha)

class Scattergun(Weapon):
    weaponsprite = function.load_image("weapons/scatterguns/0")
    firingsprite = function.load_image("weapons/scatterguns/2")
    
    weapon_rotate_point = (6, 2) # where is the handle of the gun, where to rotate around
    maxammo = 6
    refiretime = 0.5
    reloadtime = 1
    
    def fire_primary(self, game, state):
        for i in range(6):
            shot.Shot(game, state, self.id)
        
        self.refirealarm = self.refiretime