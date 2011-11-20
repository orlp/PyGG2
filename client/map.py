#!/usr/bin/env python

from __future__ import division, print_function

import pygame
import function

class MapRenderer(object):
    def __init__(self, renderer, mapname):
        self.image = function.load_image("maps/" + mapname)
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*6, self.image.get_height()*6))
        self.image.set_colorkey(None)
        self.image = self.image.convert()

    def draw(self, renderer):        
        renderer.window.blit(self.image, (0, 0), (renderer.xview, renderer.yview, renderer.view_width, renderer.view_height))