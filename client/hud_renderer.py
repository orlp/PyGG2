from __future__ import division, print_function

import math
import pygrafix
import random

import function

class HealthRenderer(object):
    def __init__(self):
        self.healthsprite = pygrafix.image.load("projectiles/rockets/0.png")

    def render(self, renderer, game, state, rocket):
        sprite = pygrafix.sprite.Sprite(self.healthsprite)

        sprite.alpha = 1

        sprite.position = (100,100)

        renderer.world_sprites.append(sprite)
        print (str(self.x)+ " " + str(self.y))