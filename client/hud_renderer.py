from __future__ import division, print_function

import math
import pygrafix

import function

class HudRenderer(object):
    HUD_SCALE=2
    def render(self, renderer):
        self.sprite = pygrafix.sprite.Sprite(self.hudsprite)
        self.sprite.position = self.sprite_location
        self.sprite.scale = self.HUD_SCALE
        renderer.hud_sprites.append(self.sprite)
        
class HealthRenderer(HudRenderer):
    
    def __init__(self, renderer):
        self.sprite_location = (10, renderer.view_height - 75) # Where is the location on screen of the sprite
        self.hudsprite  = pygrafix.image.load("huds/characterhud/0.png")