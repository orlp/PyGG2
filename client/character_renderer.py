from __future__ import division, print_function

import math, pygame
from pygame.locals import *

import function

class ScoutRenderer(object):
    def __init__(self):
        self.sprites = list([
            function.load_image("characters/scoutreds/%s" % i) for i in range(4)
        ])
        self.spriteoffset = (-24, -30)

    def render(self, renderer, state, character):
        anim_frame = int(character.animoffset)

        if anim_frame == 1 and not character.onground(renderer, state):
            anim_frame = 1
            character.animoffset = 1.0

        if character.intel:
            anim_frame += 2

        image = self.sprites[anim_frame]

        if character.flip: image = pygame.transform.flip(image, 1, 0)

        xoff = character.x + self.spriteoffset[0]
        yoff = character.y + self.spriteoffset[1]

        renderer.draw_world(image, (xoff, yoff))
