from __future__ import division, print_function

import math
import pygrafix
import random

import function

class BuildingSentryRenderer(object):
    def __init__(self):
        self.depth = -1
        self.sprites = list([pygrafix.image.load("sprites/ingameelements/sentryred/{0}.png".format(i)) for i in range(10)])
        
    def render(self, renderer, game, state, sentry):
        self.sprite = self.sprites[min(int(sentry.animation_frame), 9)] # TODO, get rid of this min and figure out how to cap an image index
        sprite = pygrafix.sprite.Sprite(self.sprite)

        # TODO: Sprite offset correctly
        sprite.position = renderer.get_screen_coords(sentry.x-8, sentry.y-20)

        renderer.world_sprites.append(sprite)
        
        #draw mask
        #w, h = sentry.collision_mask.get_size()
        #location =  renderer.get_screen_coords(sentry.x, sentry.y)
        #size = (w,h)
        #color = (153,0,153)
        #pygrafix.draw.rectangle(location,size,color)
        
class SentryRenderer(object):
    def __init__(self):
        self.depth = -1
        self.base = pygrafix.image.load("sprites/ingameelements/sentryred/11.png")
        self.turrets = list([pygrafix.image.load("sprites/ingameelements/sentryturrets/{0}.png".format(i)) for i in range(3)])
        
    def render(self, renderer, game, state, sentry):
        
        basesprite = self.base
        basesprite = pygrafix.sprite.Sprite(basesprite)
        # TODO: Sprite offset correctly
        basesprite.position = renderer.get_screen_coords(sentry.x-8, sentry.y-20)
        
        turretsprite = self.turrets[0]
        turretsprite = pygrafix.sprite.Sprite(turretsprite)
        # TODO: Sprite offset correctly
        turretsprite.position = renderer.get_screen_coords(sentry.x-4, sentry.y-4)
        
        renderer.world_sprites.append(turretsprite)
        renderer.world_sprites.append(basesprite)
        
        #draw mask
        #w, h = sentry.collision_mask.get_size()
        #location =  renderer.get_screen_coords(sentry.x, sentry.y)
        #size = (w,h)
        #color = (153,0,153)
        #pygrafix.draw.rectangle(location,size,color)