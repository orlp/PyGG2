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

        self.class_number = str(function.convert_class(character))
        self.hudsprite  = pygrafix.image.load("huds/characterhud/"+ self.class_number + ".png")

        self.health_box_background = None
        self.health_box = None

    def render(self, renderer, health_percentage):
        HudRenderer.render(self,renderer)

        self.health_box_background = HealthBar() #background first
        self.health_box_background.health_location = (52, (renderer.view_height - 54))
        self.health_box_background.health_size = (40, 40)
        self.health_box_background.health_color = (0,0,0,1) # last is alpha
        renderer.hud_overlay.append(self.health_box_background)

        self.health_box = HealthBar()
        self.health_box.health_location = (52, min ( (renderer.view_height - 14), (renderer.view_height - 54) + (40 - 40 * abs(health_percentage))) )
        self.health_box.health_size = (40, max(0, 40 * health_percentage))
        if health_percentage > 0.5:
            exponent = 2 # The higher this will be, the quicker will the change happen, and the flatter will the curve be
            # Color it green-yellow
            self.health_box.health_color = ((1 - 2*(health_percentage-0.5))**exponent, 1, 0, 1)
        else:
            exponent = 3 # The higher this will be, the quicker will the change happen, and the flatter will the curve be
            # Color it yellow-red
            self.health_box.health_color = (1, (2*health_percentage)**exponent, 0, 1)
        renderer.hud_overlay.append(self.health_box)

class HealthBar(object):
    def render (self):
        pygrafix.draw.rectangle(self.health_location, self.health_size, self.health_color)
