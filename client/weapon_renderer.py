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
            sprite.position = renderer.get_screen_coords(owner.x + self.weaponoffset_flipped[0], owner.y + self.weaponoffset_flipped[1])
            weapon_rotate = self.weapon_rotate_flipped
        else:
            sprite.flip_y = False
            sprite.position = renderer.get_screen_coords(owner.x + self.weaponoffset[0], owner.y + self.weaponoffset[1])
            weapon_rotate = self.weapon_rotate_point

        sprite.anchor = weapon_rotate
        sprite.rotation = 360 - weapon.direction

        renderer.world_sprites.append(sprite)

class ScattergunRenderer(WeaponRenderer):
    weapon_rotate_point = (5, 6) # where is the handle of the gun, where to rotate around
    weapon_rotate_flipped = (5, 6)
    weaponoffset = (7, 10) # where the character should carry it's gun
    weaponoffset_flipped = (7, 10)

    def __init__(self):
        self.depth = 1
        self.weaponsprite = pygrafix.image.load("weapons/scatterguns/0.png")
        self.firingsprite = pygrafix.image.load("weapons/scatterguns/2.png")

class FlamethrowerRenderer(WeaponRenderer):
    weapon_rotate_point = (8, 2) #Where is the handle of the gun, where to rotate around
    weapon_rotate_flipped = (8,8)
    weaponoffset = (4, 11) #Where the character should carry it's gun
    weaponoffset_flipped = (8, 11)

    def __init__(self):
        self.depth = 1
        self.weaponsprite = pygrafix.image.load("weapons/flamethrowers/0.png")
        self.firingsprite = pygrafix.image.load("weapons/flamethrowers/2.png")

class RocketlauncherRenderer(WeaponRenderer):
    weapon_rotate_point = (10, 6) # where is the handle of the gun, where to rotate around
    weapon_rotate_flipped = (10, 6)
    weaponoffset = (1, 7) # where the character should carry it's gun
    weaponoffset_flipped = (12, 7)

    def __init__(self):
        self.depth = 1
        self.weaponsprite = pygrafix.image.load("weapons/rocketlaunchers/0.png")
        self.firingsprite = pygrafix.image.load("weapons/rocketlaunchers/2.png")

class MinigunRenderer(WeaponRenderer):
    weapon_rotate_point = (14, 3) # where is the handle of the gun, where to rotate around
    weapon_rotate_flipped = (14,17)
    weaponoffset = (7, 10) # where the character should carry it's gun
    weaponoffset_flipped = (8, 10)

    def __init__(self):
        self.depth = 1
        self.weaponsprite = pygrafix.image.load("weapons/miniguns/0.png")
        self.firingsprite = pygrafix.image.load("weapons/miniguns/2.png")
        
class MedigunRenderer(WeaponRenderer):
    weapon_rotate_point = (10, -1) # where is the handle of the gun, where to rotate around
    weapon_rotate_flipped = (10,11)
    weaponoffset = (10, 9) # where the character should carry it's gun
    weaponoffset_flipped = (2, 9)

    def __init__(self):
        self.depth = 1
        self.weaponsprite = pygrafix.image.load("weapons/mediguns/0.png")
        self.firingsprite = pygrafix.image.load("weapons/mediguns/0.png")


class ShotgunRenderer(WeaponRenderer):
    weapon_rotate_point = (10, -1) # where is the handle of the gun, where to rotate around
    weapon_rotate_flipped = (10,11)
    weaponoffset = (10, 9) # where the character should carry it's gun
    weaponoffset_flipped = (2, 9)

    def __init__(self):
        self.depth = 1
        self.weaponsprite = pygrafix.image.load("weapons/shotguns/0.png")
        self.firingsprite = pygrafix.image.load("weapons/shotguns/2.png")

class RevolverRenderer(WeaponRenderer):
    weapon_rotate_point = (-1, 6) # where is the handle of the gun, where to rotate around
    weapon_rotate_flipped = (-1,6)
    weaponoffset = (5, 9) # where the character should carry it's gun
    weaponoffset_flipped = (8, 9)

    def __init__(self):
        self.depth = 1
        self.weaponsprite = pygrafix.image.load("weapons/revolver2s/0.png")
        self.firingsprite = pygrafix.image.load("weapons/revolver2s/2.png")

    def render(self, renderer, game, state, weapon):
        if not state.entities[weapon.owner].cloaking:#FIXME: or player.team == out team
            WeaponRenderer.render(self, renderer, game, state, weapon)
        else:
            pass# TODO: Transparent drawing
