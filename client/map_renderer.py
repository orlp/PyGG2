#!/usr/bin/env python

from __future__ import division, print_function

import pygrafix
import function

class MapRenderer(object):
    def __init__(self, renderer, mapname):
        self.set_map(mapname)

    def set_map(self, mapname):
        self.sprite = pygrafix.sprite.Sprite(pygrafix.image.load("maps/" + mapname + ".png"))
        self.sprite.scale = 6

    def render(self, renderer, state):
        self.sprite.x = -renderer.xview
        self.sprite.y = -renderer.yview
        self.sprite.draw(scale_smoothing = False)
