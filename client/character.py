#!/usr/bin/env python

from __future__ import division, print_function

import math, pygame
from pygame.locals import *

import function
import entity
import weapons
import mask

class ScoutRenderer(entity.EntityRenderer):    
    def __init__(self, renderer, state, entity_id):
        super(ScoutRenderer, self).__init__(renderer, state, entity_id)
        
        self.sprites = list([
            function.load_image("characters/scoutreds/%s" % i) for i in range(4)
        ])
        self.spriteoffset = (-24, -30)
        
        # time tracker for the moving of the character's legs
        self.animoffset = 0.0

    def render(self, renderer, state, frametime):
        character = self.get_entity(state)
        
        anim_frame = 0
        # this is quite important, if hspeed / 20 drops below 1 self.animoffset will rapidly change and cause very fast moving legs (while we are moving very slow)
        if abs(character.hspeed) > 20: 
            self.animoffset += frametime * abs(character.hspeed) / 20
            self.animoffset %= 2
            anim_frame = int(self.animoffset)
            
            if anim_frame == 1 and not character.onground(renderer, state):
                anim_frame = 1
                self.animoffset = 1.0
        
        if character.intel:
            anim_frame += 2
        
        image = self.sprites[anim_frame]
        
        if character.flip: image = pygame.transform.flip(image, 1, 0)
        
        xoff = character.x + self.spriteoffset[0]
        yoff = character.y + self.spriteoffset[1]
        
        renderer.draw_world(image, (xoff, yoff))