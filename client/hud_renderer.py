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
    
    def __init__(self, renderer, character):
        self.sprite_location = (10, renderer.view_height - 75) # Where is the location on screen of the sprite
        
        self.health_location = (52,renderer.view_height - 54) # where the little green rectangle shows up
        self.health_size = (40,40)
        self.health_color = (0.3,0.5,0.2,1) # last is alpha
        self.class_number = str(function.convert_class(character))
        self.hudsprite  = pygrafix.image.load("huds/characterhud/"+ self.class_number + ".png")
        
    def render(self, renderer, health_percentage):
        HudRenderer.render(self,renderer)
        self.health_size = (40, 40 * health_percentage)
        self.health_location = (52, ((renderer.view_height - 54) + (40 - 40 * health_percentage)))
        renderer.draw_health.append(self)