from __future__ import division, print_function

import math
import pygrafix
import random

import function

class ShotRenderer(object):
    def __init__(self):
        self.shotsprite = function.load_image("projectiles/shots/0")

    def render(self, renderer, game, state, shot):
        sprite = pygrafix.sprite.Sprite(self.shotsprite)
        sprite.rotation = 360 - shot.direction

        if shot.max_flight_time - shot.flight_time < shot.fade_time:
            sprite.alpha = (shot.max_flight_time - shot.flight_time) / shot.fade_time

        sprite.position = renderer.get_screen_coords(shot.x, shot.y)

        renderer.world_sprites.add_sprite(sprite)

class FlameRenderer(object):
    def __init__(self):

        self.currentindex = -1
        self.flamesprite = [0,1,2]

        self.flamesprite[0] = function.load_image("projectiles/flames/0")
        self.flamesprite[1] = function.load_image("projectiles/flames/1")
        self.flamesprite[2] = function.load_image("projectiles/flames/2")

    def render(self, renderer, game, state, flame):
        #sprite animation
        if self.currentindex == -1:
            self.currentindex = 0
        else:
            if self.currentindex == 2:
                self.currentindex = 0
            else:
                self.currentindex += 1

        sprite = pygrafix.sprite.Sprite(self.flamesprite[self.currentindex])

        sprite.position = renderer.get_screen_coords(flame.x,flame.y)

        renderer.world_sprites.add_sprite(sprite)

class RocketRenderer(object):
    def __init__(self):
        self.rocketsprite = function.load_image("projectiles/rockets/0")

    def render(self, renderer, game, state, rocket):
        sprite = pygrafix.sprite.Sprite(self.rocketsprite)
        sprite.rotation = 360 - rocket.direction

        sprite.alpha = min((rocket.max_flight_time - rocket.flight_time) / rocket.fade_time, 1)

        sprite.position = renderer.get_screen_coords(rocket.x, rocket.y)

        renderer.world_sprites.add_sprite(sprite)
