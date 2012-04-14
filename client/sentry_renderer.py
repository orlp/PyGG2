from __future__ import division, print_function

import math
import pygrafix
import random

import function

class BuildingSentryRenderer(object):
    def __init__(self):
        self.depth = 1

    def render(self, renderer, game, state, sentry):
        self.sprite = pygrafix.image.load("sprites/ingameelements/sentryred/"+str(int(sentry.animation_frame))+".png")
        sprite = pygrafix.sprite.Sprite(self.sprite)

        # TODO: Sprite offset correctly
        sprite.position = renderer.get_screen_coords(sentry.x, sentry.y)

        renderer.world_sprites.append(sprite)

    def return_depth(self):
        return self.depth
