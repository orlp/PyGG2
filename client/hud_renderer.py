from __future__ import division, print_function

import math
import pygrafix

import function

class HudRenderer(object):
    def __init__(self):
        pass

    def render(self, renderer):
        self.sprite = pygrafix.sprite.Sprite(self.hudsprite)
        self.sprite.position = self.sprite_location
        return (self.sprite)
        
class HealthRenderer(HudRenderer):
    
    def __init__(self):
        self.sprite_location = (25, 550) # Where is the location on screen of the sprite
        self.hudsprite  = pygrafix.image.load("huds/characterhud/0.png")