#!/usr/bin/env python

from __future__ import division, print_function

import math, pygame
from pygame.locals import *

import function
import entity
import weapons

class Character(entity.MovingObject):
    def __init__(self, game, state):
        super(Character, self).__init__(game, state)
        
        self.flip = False # are we flipped around?
        self.walkframe = 0 # walk anim

    def step(self, game, state, frametime):
        angle = state.entities[self.weapon].direction % 360
        self.flip = not (angle < 90 or angle > 270)
        self.walkframe = (self.walkframe+abs(self.hspeed)/20) % 2
        
        # if we are holding down movement keys, move
        if game.left: self.hspeed -= 1000 * frametime
        if game.right: self.hspeed += 1000 * frametime
        
        # if we're not, slow down
        if not (game.left or game.right):
            if abs(self.hspeed) < 10: self.hspeed = 0
            else: self.hspeed -= function.sign(self.hspeed) * min(abs(self.hspeed), 600 * frametime)
        
        if game.up:
            if self.onground(game, state):
                self.vspeed = -200
                
        # gravitational force
        self.vspeed += 300 * frametime

        # TODO: air resistance, not hard limit
        self.vspeed = min(800, self.vspeed)
        
        # TODO: speed limit based on class
        self.hspeed = min(200, max(-200, self.hspeed))

    def endstep(self, game, state, frametime):
        # check if we are on the ground before moving (for walking over 1 unit walls)
        onground = True
        
        # first we move, ignoring walls
        self.x += self.hspeed * frametime
        # if we are in a wall now, we must move back
        
        if game.map.collision_mask.overlap(self.collision_mask, (int(self.x), int(self.y))):
            # but if we just walked onto a one-unit wall it's ok
            # but we had to be on the ground
            if onground and not game.map.collision_mask.overlap(self.collision_mask, (int(self.x), int(self.y - 6))):
                while game.map.collision_mask.overlap(self.collision_mask, (int(self.x), int(self.y))):
                    self.y -= 1
            # but sometimes we are so fast we will need to take two stairs at the same time
            elif onground and not game.map.collision_mask.overlap(self.collision_mask, (int(self.x), int(self.y - 12))) and game.map.collision_mask.overlap(self.collision_mask, (int(self.x - 6 * function.sign(self.hspeed)), int(self.y))):
                while game.map.collision_mask.overlap(self.collision_mask, (int(self.x), int(self.y))):
                    self.y -= 1
            else:
                self.x = math.floor(self.x) # move back to a whole pixel - TODO math.floor/math.ceil depending on direction
                
                # and if one pixel wasn't enough
                while game.map.collision_mask.overlap(self.collision_mask, (int(self.x), int(self.y))):
                    self.x -= function.sign(self.hspeed)
                
                self.hspeed = 0
        
        # same stuff, but now vertically
        self.y += self.vspeed * frametime
        
        if game.map.collision_mask.overlap(self.collision_mask, (int(self.x), int(self.y))):
            self.y = float(int(self.y))
            
            while game.map.collision_mask.overlap(self.collision_mask, (int(self.x), int(self.y))):
                self.y -= function.sign(self.vspeed)
        
            self.vspeed = 0
        
        # just to be sure
        self.x = max(self.x, 0)
        self.y = max(self.y, 0)
    
    def onground(self, game, state):
        # are we on the ground? About one third of an unit from the ground is enough to qualify for this
        return game.map.collision_mask.overlap(self.collision_mask, (int(self.x), int(self.y + 1)))


class ScoutDrawer(entity.EntityDrawer):    
    def __init__(self, game, state, entity_id):
        super(ScoutDrawer, self).__init__(game, state, entity_id)
        
        self.sprites = [
            function.load_image("characters/scoutreds/0"),
            function.load_image("characters/scoutreds/1")
        ]
        self.spriteoffset = (-24, -30)

    def draw(self, game, state):
        character = self.get_entity(state)

        image = self.sprites[int(character.walkframe)]
        if character.flip: image = pygame.transform.flip(image, 1, 0)
        
        xoff = character.x + self.spriteoffset[0]
        yoff = character.y + self.spriteoffset[1]
        
        game.draw_world(image, (xoff, yoff))
        

class Scout(Character):
    Drawer = ScoutDrawer

    # width, height of scout - rectangle collision
    collision_mask = pygame.mask.Mask((12, 33))
    collision_mask.fill()
    
    maxhp = 100
    
    def __init__(self, game, state):
        Character.__init__(self, game, state)

        self.hp = self.maxhp
        self.weapon = weapons.Scattergun(game, state, self.id).id