from __future__ import division, print_function

import math
import pygrafix

import function

class WeaponRenderer(object):

    def __init__(self):
        pass

    def render(self, renderer, game, state, weapon):
        owner = state.entities[weapon.owner]

        if weapon.refiretime - weapon.refirealarm < 0.02:
            sprite = pygrafix.sprite.Sprite(self.firingsprite)
        else:
            sprite = pygrafix.sprite.Sprite(self.weaponsprite)

        if owner.flip:
            sprite.flip_y = True

        sprite.anchor = self.weapon_rotate_point
        sprite.rotation = 360 - weapon.direction
        sprite.position = renderer.get_screen_coords(owner.x + self.weaponoffset[0], owner.y + self.weaponoffset[1])

        renderer.world_sprites.add_sprite(sprite)

class ScattergunRenderer(WeaponRenderer):
    weapon_rotate_point = (4, 8) # where is the handle of the gun, where to rotate around
    weaponoffset = (12, 13) # where the character should carry it's gun
    weaponoffset_flipped = (4, 8)

    def __init__(self):
        self.weaponsprite = function.load_image("weapons/scatterguns/0")
        self.firingsprite = function.load_image("weapons/scatterguns/2")

class RocketlauncherRenderer(WeaponRenderer):
    weapon_rotate_point = (8, 8) # where is the handle of the gun, where to rotate around
    weaponoffset = (-1, 8) # where the character should carry it's gun
    weaponoffset_flipped = (18, 8)

    def __init__(self):
        self.weaponsprite = function.load_image("weapons/rocketlaunchers/0")
        self.firingsprite = function.load_image("weapons/rocketlaunchers/2")

class ShotgunRenderer(WeaponRenderer):
    weapon_rotate_point = (2, 8) # where is the handle of the gun, where to rotate around
    weaponoffset = (12, 17) # where the character should carry it's gun
    weaponoffset_flipped = (6, 8)

    def __init__(self):
        self.weaponsprite = function.load_image("weapons/shotguns/0")
        self.firingsprite = function.load_image("weapons/shotguns/2")

class RevolverRenderer(WeaponRenderer):
    weapon_rotate_point = (6, 8) # where is the handle of the gun, where to rotate around
    weaponoffset = (11, 14) # where the character should carry it's gun
    weaponoffset_flipped = (8, 8)

    def __init__(self):
        self.weaponsprite = function.load_image("weapons/revolvers/0")
        self.firingsprite = function.load_image("weapons/revolvers/2")

    def render(self, renderer, game, state, weapon):
        if not state.entities[weapon.owner].cloaking:#FIXME: or player.team == out team
            WeaponRenderer.render(self, renderer, game, state, weapon)
        else:
            pass# TODO: Transparent drawing
