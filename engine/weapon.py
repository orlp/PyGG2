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
        self.ammo = self.maxammo
        self.direction = state.entities[self.owner].get_player(game, state).aimdirection

    def beginstep(self, game, state, frametime):
        owner = state.entities[self.owner]
        self.direction = owner.get_player(game, state).aimdirection

    def step(self, game, state, frametime):
        owner = state.entities[self.owner]

        if self.refirealarm <= 0:
            self.refirealarm = 0.0
        else:
            self.refirealarm -= frametime

        if owner.get_player(game, state).leftmouse and self.refirealarm == 0:
            self.fire_primary(game, state)

        if owner.get_player(game, state).rightmouse and self.refirealarm == 0:
            self.fire_secondary(game, state)

    # override this
    def fire_primary(self, game, state): pass
    def fire_secondary(self, game, state): pass

    def interpolate(self, prev_obj, next_obj, alpha):
        self.refirealarm = (1 - alpha) * prev_obj.refirealarm + alpha * next_obj.refirealarm
        self.direction = function.interpolate_angle(prev_obj.direction, next_obj.direction, alpha)

class Scattergun(Weapon):
    maxammo = 6
    refiretime = .05
    reloadtime = 1
    shotdamage = 8

    def fire_primary(self, game, state):
        random.seed(str(state.entities[self.owner].get_player(game, state).id) + ";" + str(state.time))

        for i in range(10):
            projectile.Shot(game, state, self.id, self.shotdamage)

        self.refirealarm = self.refiretime

class Rocketlauncher(Weapon):
    maxammo = 4
    refiretime = 1
    reloadtime = 5/6

    def fire_primary(self, game, state):
        projectile.Rocket(game, state, self.id)
        self.refirealarm = self.refiretime

class Minigun(Weapon):
    maxammo = 200
    refiretime = 1/15
    reloadtime = 1/2
    shotdamage = 8

    def fire_primary(self, game, state):
        random.seed(str(state.entities[self.owner].get_player(game, state).id) + ";" + str(state.time))
        projectile.Shot(game, state, self.id, self.shotdamage)

        self.refirealarm = self.refiretime

class Shotgun(Weapon):
    maxammo = 4
    refiretime = 2/3
    reloadtime = 1/2
    shotdamage = 7

    def fire_primary(self, game, state):
        random.seed(str(state.entities[self.owner].get_player(game, state).id) + ";" + str(state.time))
        for i in range(5):
            projectile.Shot(game, state, self.id, self.shotdamage)

        self.refirealarm = self.refiretime

class Revolver(Weapon):
    maxammo = 6
    refiretime = 3/5
    reloadtime = .5

    def fire_primary(self, game, state):
        print("Cloaking: ", state.entities[self.owner].cloaking, "| is very unresponsive; print statement in line 89 of weapon.py")
        if not state.entities[self.owner].cloaking:
            random.seed(str(state.entities[self.owner].player_id) + ";" + str(state.time))
            projectile.Shot(game, state, self.id, 28) # 28 == damage
            self.refirealarm = self.refiretime
        #else: Stab

    def fire_secondary(self, game, state):
        state.entities[self.owner].cloaking = not state.entities[self.owner].cloaking# Any ideas how to add a good gradient?
