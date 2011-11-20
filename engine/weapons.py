#!/usr/bin/env python

from __future__ import division, print_function

import math
import random
import function
import entity
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
        owner = state.entities[self.owner]
    
        self.direction = owner.aimdirection
        
        if self.refirealarm <= 0:
            self.refirealarm = 0.0
        else:
            self.refirealarm -= frametime

        if owner.leftmouse and self.refirealarm == 0:
            self.fire_primary(game, state)

        if owner.rightmouse and self.refirealarm == 0:
            self.fire_secondary(game, state)
            
    # override this
    def fire_primary(self, game, state): pass
    def fire_secondary(self, game, state): pass
    
    def interpolate(self, prev_obj, next_obj, alpha):
        self.direction = function.interpolate_angle(prev_obj.direction, next_obj.direction, alpha)
        self.refirealarm = (1 - alpha) * prev_obj.refirealarm + alpha * next_obj.refirealarm

class Scattergun(Weapon):
    maxammo = 6
    refiretime = .05
    reloadtime = 1
    
    def fire_primary(self, game, state):
        for i in range(10):
            projectile.Shot(game, state, self.id)
        
        self.refirealarm = self.refiretime
