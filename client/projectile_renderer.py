from __future__ import division, print_function

import math
import pygrafix
import random

import function

class ShotRenderer(object):
    def __init__(self):
        self.shotsprite = pygrafix.image.load("projectiles/shots/0.png")

    def render(self, renderer, game, state, shot):
        sprite = pygrafix.sprite.Sprite(self.shotsprite)
        sprite.rotation = 360 - shot.direction

        if shot.max_flight_time - shot.flight_time < shot.fade_time:
            sprite.alpha = (shot.max_flight_time - shot.flight_time) / shot.fade_time

        sprite.position = renderer.get_screen_coords(shot.x, shot.y)

        renderer.world_sprites.append(sprite)

class FlameRenderer(object):
    def __init__(self):

        self.currentindex = -1
        self.flamesprite = [0,1,2]

        self.flamesprite[0] = pygrafix.image.load("projectiles/flames/0.png")
        self.flamesprite[1] = pygrafix.image.load("projectiles/flames/1.png")
        self.flamesprite[2] = pygrafix.image.load("projectiles/flames/2.png")

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
        self.rocketsprite = pygrafix.image.load("projectiles/rockets/0.png")

    def render(self, renderer, game, state, rocket):
        sprite = pygrafix.sprite.Sprite(self.rocketsprite)
        sprite.rotation = 360 - rocket.direction

        sprite.alpha = min((rocket.max_flight_time - rocket.flight_time) / rocket.fade_time, 1)

        sprite.position = renderer.get_screen_coords(rocket.x, rocket.y)

        renderer.world_sprites.add_sprite(sprite)
