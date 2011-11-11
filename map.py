#!/usr/bin/env python

from __future__ import division, print_function

import function
import pygame

class Map(object):
    def __init__(self, game, mapname):
        self.mapname = mapname
    
        self.image = function.load_image("maps/" + mapname)
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*6, self.image.get_height()*6))
        self.image.set_colorkey(None)
        self.image = self.image.convert()
        
        self.collision_mask = function.load_mask("collisionmaps/" + mapname)
        x, y = self.collision_mask.get_size()
        self.collision_mask = self.collision_mask.scale(x*6, y*6)

    def draw(self, game):        
        game.window.blit(self.image, (0, 0), (game.xview, game.yview, game.view_width, game.view_height))