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

class RocketRenderer(object):
    def __init__(self):
        self.rocketsprite = function.load_image("projectiles/rockets/0")

    def render(self, renderer, game, state, rocket):
        sprite = pygrafix.sprite.Sprite(self.rocketsprite)
        sprite.rotation = 360 - rocket.direction

        if rocket.max_flight_time - rocket.flight_time < rocket.fade_time:
            sprite.alpha (rocket.max_flight_time - rocket.flight_time) / rocket.fade_time

        sprite.position = renderer.get_screen_coords(rocket.x, rocket.y)

        renderer.world_sprites.add_sprite(sprite)
