#!/usr/bin/env python

from __future__ import division, print_function

import math
import struct

import function
import entity
import weapon
import mask

class Character(entity.MovingObject):
    def __init__(self, game, state, player):
        super(Character, self).__init__(game, state)

        self.player = player

        self.flip = False # are we flipped around?
        self.intel = False # has intel (for drawing purposes)

        # time tracker for the moving of the character's legs
        self.animoffset = 0.0

    def step(self, game, state, frametime):
        # this is quite important, if hspeed / 20 drops below 1 self.animoffset will rapidly change and cause very fast moving legs (while we are moving very slow)
        if abs(self.hspeed) > 20:
            self.animoffset += frametime * abs(self.hspeed) / 20
            self.animoffset %= 2

        self.flip = not (self.player.aimdirection < 90 or self.player.aimdirection > 270)

        # if we are holding down movement keys, move
        if self.player.left: self.hspeed -= 1000 * frametime
        if self.player.right: self.hspeed += 1000 * frametime

        # if we're not, slow down
        if not (self.player.left or self.player.right):
            if abs(self.hspeed) < 10: self.hspeed = 0
            else: self.hspeed -= function.sign(self.hspeed) * min(abs(self.hspeed), 600 * frametime)

        if self.player.up:
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

        self.animoffset = prev_obj.animoffset + (next_obj.animoffset - prev_obj.animoffset) * alpha

        if alpha > 0.5: refobj = next_obj
        else: refobj = prev_obj

        self.flip = refobj.flip

    #def serialize(self, game, updatetype):
    #    if updatetype == "SNAPSHOT_UPDATE" or updatetype == "COMPLETE_UPDATE":
    #      bytestring += struct.pack("!BHffffB", keybyte, self.aimdirection, self.x, self.y, self.hspeed, self.vspeed, self.hp) # TODO: Ammo and cloak.
    #
    #    return bytestring

class Scout(Character):
    # width, height of scout - rectangle collision
    collision_mask = mask.Mask(12, 33, True)

    maxhp = 100
    def __init__(self, game, state, player):
        Character.__init__(self, game, state, player)

        self.hp = self.maxhp
        self.weapon = weapon.Scattergun(game, state, self.id).id
