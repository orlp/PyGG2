from __future__ import division, print_function

import math, pygame
from pygame.locals import *

import function

class ClassRenderer(object):
    def __init__(self):
        pass

    def render(self, renderer, game, state, character):
        anim_frame = int(character.animoffset)

        if not character.onground(game, state):
            anim_frame = 1

        if character.intel:
            anim_frame += 2

        image = self.sprites[anim_frame]

        if character.flip: image = pygame.transform.flip(image, 1, 0)

        xoff = character.x + self.spriteoffset[0]
        yoff = character.y + self.spriteoffset[1]

        renderer.draw_world(image, (xoff, yoff))

class ScoutRenderer(ClassRenderer):
    def __init__(self):
        self.sprites = list([
            function.load_image("characters/scoutreds/%s" % i) for i in range(4)
        ])
        self.spriteoffset = (-24, -30)

class SoldierRenderer(ClassRenderer):
    def __init__(self):
        self.sprites = list([
            function.load_image("characters/soldierreds/%s" % i) for i in range(4)
        ])
        self.spriteoffset = (-24, -30)

class EngineerRenderer(ClassRenderer):
    def __init__(self):
        self.sprites = list([
            function.load_image("characters/engineerreds/%s" % i) for i in range(4)
        ])
        self.spriteoffset = (-24, -30)
