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
        sprite_offset_flipped = (-12,-20)
        sprite_offset = (-8,-20)
        self.sprite = self.sprites[min(int(sentry.animation_frame), 9)] # TODO, get rid of this min and figure out how to cap an image index
        sprite = pygrafix.sprite.Sprite(self.sprite)
        
        if sentry.flip == True:
            sprite.flip_x = True
            sprite.position = renderer.get_screen_coords(sentry.x + sprite_offset_flipped[0], sentry.y + sprite_offset_flipped[1])
        else:
            sentry.flip_x = False
            sprite.position = renderer.get_screen_coords(sentry.x + sprite_offset[0] , sentry.y + sprite_offset[1] )
        

        renderer.world_sprites.append(sprite)
        
        #draw mask
        w, h = sentry.collision_mask.get_size()
        location =  renderer.get_screen_coords(sentry.x, sentry.y)
        size = (w,h)
        color = (153,0,153)
        pygrafix.draw.rectangle(location,size,color)
        
class SentryRenderer(object):
    def __init__(self):
        self.depth = -1
        self.base = pygrafix.image.load("sprites/ingameelements/sentryred/11.png")
        self.turrets = list([pygrafix.image.load("sprites/ingameelements/sentryturrets/{0}.png".format(i)) for i in range(3)])
        
    def render(self, renderer, game, state, sentry):
        basesprite_position_offset = (-8, -20)
        basesprite_position_offset_flipped = (-13, -20)
        
        turretsprite_position_offset = (-4,-4)
        turretsprite_position_flipped_offset = (-14,-4)
        
        basesprite = self.base
        basesprite = pygrafix.sprite.Sprite(basesprite)
    
        turretsprite = self.turrets[0]
        turretsprite = pygrafix.sprite.Sprite(turretsprite)
        
        if sentry.flip == True:
            basesprite.flip_x = True
            turretsprite.flip_x = True
            basesprite.position = renderer.get_screen_coords(sentry.x + basesprite_position_offset_flipped[0], sentry.y + basesprite_position_offset_flipped[1])
            turretsprite.position = renderer.get_screen_coords(sentry.x + turretsprite_position_flipped_offset[0],sentry.y + turretsprite_position_flipped_offset[1])
        else:
            basesprite.flip_x = False
            turretsprite.flip_x = False
            basesprite.position = renderer.get_screen_coords(sentry.x + turretsprite_position_offset[0], sentry.y + turretsprite_position_offset[1])
            turretsprite.position = renderer.get_screen_coords(sentry.x + turretsprite_position_offset[0],sentry.y + turretsprite_position_offset[1])
        
        renderer.world_sprites.append(turretsprite)
        renderer.world_sprites.append(basesprite)
        
        #draw mask
        w, h = sentry.collision_mask.get_size()
        location =  renderer.get_screen_coords(sentry.x, sentry.y)
        size = (w,h)
        color = (153,0,153)
        pygrafix.draw.rectangle(location,size,color)