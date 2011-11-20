#!/usr/bin/env python

from __future__ import division, print_function

import math

import function
import entity
import weapons
import mask

class Character(entity.MovingObject):
    def __init__(self, game, state):
        super(Character, self).__init__(game, state)
        
        self.flip = False # are we flipped around?
        self.intel = False # has intel (for drawing purposes)

		# input
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.leftmouse = False
        self.middlemouse = False
        self.rightmouse = False
        self.aimdirection = 0
        
        # time tracker for the moving of the character's legs
        self.animoffset = 0.0
        
    def step(self, game, state, frametime):
        # this is quite important, if hspeed / 20 drops below 1 self.animoffset will rapidly change and cause very fast moving legs (while we are moving very slow)
        if abs(self.hspeed) > 20: 
            self.animoffset += frametime * abs(self.hspeed) / 20
            self.animoffset %= 2
            
        self.flip = not (self.aimdirection < 90 or self.aimdirection > 270)
        
        # if we are holding down movement keys, move
        if self.left: self.hspeed -= 1000 * frametime
        if self.right: self.hspeed += 1000 * frametime
        
        # if we're not, slow down
        if not (self.left or self.right):
            if abs(self.hspeed) < 10: self.hspeed = 0
            else: self.hspeed -= function.sign(self.hspeed) * min(abs(self.hspeed), 600 * frametime)
        
        if self.up:
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
    
    def onground(self, game, state):
        # are we on the ground? About one third of an unit from the ground is enough to qualify for this
        return game.map.collision_mask.overlap(self.collision_mask, (int(self.x), int(self.y + 1)))
        
    def interpolate(self, prev_obj, next_obj, alpha):
        super(Character, self).interpolate(prev_obj, next_obj, alpha)
        
        self.aimdirection = function.interpolate_angle(prev_obj.aimdirection, next_obj.aimdirection, alpha)
        
        if alpha > 0.5: refobj = next_obj
        else: refobj = prev_obj
        
        self.up = refobj.up
        self.down = refobj.down
        self.left = refobj.left
        self.right = refobj.right
        self.leftmouse = refobj.leftmouse
        self.middlemouse = refobj.middlemouse
        self.rightmouse = refobj.rightmouse
        self.flip = refobj.flip

class Scout(Character):
    # width, height of scout - rectangle collision
    collision_mask = mask.Mask(12, 33, True)
    
    maxhp = 100
    def __init__(self, game, state):
        Character.__init__(self, game, state)

        self.hp = self.maxhp
        self.weapon = weapons.Scattergun(game, state, self.id).id
