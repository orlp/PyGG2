from __future__ import division, print_function

import pyglet
from pyglet.gl import *
import function

class Map(object):
    def __init__(self, game, mapname):
        self.mapname = mapname
    
        self.image = pyglet.sprite.Sprite(function.load_image("maps/" + mapname))
        self.image.scale = 6
        
        self.collision_mask = function.load_mask("collisionmaps/" + mapname)
        x, y = self.collision_mask.get_size()
        self.collision_mask = self.collision_mask.scale(x*6, y*6)
        
    def draw(self, game):
        self.image.x = -game.xview
        self.image.y = -game.yview
        
        self.image.draw()