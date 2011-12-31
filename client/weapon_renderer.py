from __future__ import division, print_function

import pygame, math
from pygame.locals import *

import function

class ScattergunRenderer(object):
    weapon_rotate_point = (6, 8) # where is the handle of the gun, where to rotate around
    weaponoffset = (12, 13) # where the character should carry it's gun
    weaponoffset_flipped = (6, 8)

    def __init__(self):
        self.weaponsprite = function.load_image("weapons/scatterguns/0")
        self.firingsprite = function.load_image("weapons/scatterguns/2")

    def render(self, renderer, game, state, weapon):
        owner = state.entities[weapon.owner]

        image = self.weaponsprite
        offset = self.weaponoffset
        rotate_point = self.weapon_rotate_point

        if weapon.refiretime - weapon.refirealarm < 0.02:
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

        renderer.draw_world(image, (xoff, yoff))


class RocketlauncherRenderer(object):
    weapon_rotate_point = (8, 8) # where is the handle of the gun, where to rotate around
    weaponoffset = (-1, 8) # where the character should carry it's gun
    weaponoffset_flipped = (18, 8)

    def __init__(self):
        self.weaponsprite = function.load_image("weapons/rocketlaunchers/0")
        self.firingsprite = function.load_image("weapons/rocketlaunchers/2")

    def render(self, renderer, game, state, weapon):
        owner = state.entities[weapon.owner]

        image = self.weaponsprite
        offset = self.weaponoffset
        rotate_point = self.weapon_rotate_point

        if weapon.refiretime - weapon.refirealarm < 0.02:
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

        renderer.draw_world(image, (xoff, yoff))

class RevolverRenderer(object):
    # TODO ONCE SPY DONE:
    weapon_rotate_point = (6, 8) # where is the handle of the gun, where to rotate around
    weaponoffset = (12, 13) # where the character should carry it's gun
    weaponoffset_flipped = (6, 8)

    def __init__(self):
        self.weaponsprite = function.load_image("weapons/revolvers/0")
        self.firingsprite = function.load_image("weapons/revolvers/2")

    def render(self, renderer, game, state, weapon):
        owner = state.entities[weapon.owner]

        image = self.weaponsprite
        offset = self.weaponoffset
        rotate_point = self.weapon_rotate_point

        if weapon.refiretime - weapon.refirealarm < 0.02:
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

        renderer.draw_world(image, (xoff, yoff))
