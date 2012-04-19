from __future__ import division, print_function

import math
import pygrafix

import function
import spritefont

class HudRenderer(object):
    HUD_SCALE=2
    def render(self, renderer):

        self.sprite = pygrafix.sprite.Sprite(self.hudsprite)
        self.sprite.position = self.sprite_location
        self.sprite.scale = self.HUD_SCALE
        renderer.hud_sprites.append(self.sprite)
class HealthRenderer(HudRenderer):

    def __init__(self, renderer, game, state, character):

        self.sprite_location = (10, renderer.view_height - 75) # Where is the location on screen of the sprite
        my_class_type = type(character)
        my_class_number = str(function.convert_class(my_class_type))
       
        self.hudsprite = pygrafix.image.load("huds/characterhud/"+ my_class_number + ".png")

        self.health_box_background = None
        self.health_box = None

        self.health_text = HealthText()
        self.health_text.health_location = (56, renderer.view_height - 52)
        self.health_text.health_size = (36, 36)
        
    def render(self, renderer, game, state, character):

        HudRenderer.render(self,renderer)

        character_hp = character.hp
        character_maxhp = character.maxhp
        #always have at least 1 percent, can't divide by zero!
        health_percentage = max(0.01,(character_hp / character_maxhp))

        self.health_box_background = HealthBar() #background first
        self.health_box_background.health_location = (52, (renderer.view_height - 54))
        self.health_box_background.health_size = (40, 40)
        self.health_box_background.health_color = (0,0,0,1) # last is alpha
        renderer.hud_overlay.append(self.health_box_background)

        self.health_text.text = str(character_hp)

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
        renderer.hud_overlay.append(self.health_text)
        
        spritefont.SpriteFont(bold=True).renderString("{0}, {1}, {2}, {3}".format(player.left, player.lastleft, player.right, player.lastright), 123, 123)

class HealthBar(object):
    def render(self):
        pygrafix.draw.rectangle(self.health_location, self.health_size, self.health_color)

class HealthText(object):
    def __init__(self):
        self.font = spritefont.SpriteFont(bold=True)

    def render(self):
        tw, th = self.font.stringSize(self.text)
        tx = self.health_location[0] + (self.health_size[0] - tw)/2
        ty = self.health_location[1] + (self.health_size[1] - th)/2
        self.font.renderString(self.text, tx, ty)
