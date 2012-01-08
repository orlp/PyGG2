#!/usr/bin/env python

from __future__ import division, print_function

import math
import struct

import function
import entity
import weapon
import mask

class Character(entity.MovingObject):
    acceleration = 1500

    def __init__(self, game, state, player_id):
        super(Character, self).__init__(game, state)

        self.player_id = player_id

        self.flip = False # are we flipped around?
        self.intel = False # has intel (for drawing purposes)
        self.can_doublejump = False

        # time tracker for the moving of the character's legs
        self.animoffset = 0.0

    def step(self, game, state, frametime):
        player = self.get_player(game, state)

        # this is quite important, if hspeed / 20 drops below 1 self.animoffset will rapidly change and cause very fast moving legs (while we are moving very slow)
        if abs(self.hspeed) > 20:
            self.animoffset += frametime * abs(self.hspeed) / 20
            self.animoffset %= 2

        self.flip = not (player.aimdirection < 90 or player.aimdirection > 270)

        # if we are holding down movement keys, move
        if player.left: self.hspeed -= self.acceleration * frametime
        if player.right: self.hspeed += self.acceleration * frametime

        # if we're not, slow down
        if not (player.left or player.right):
            if abs(self.hspeed) < 10: self.hspeed = 0
            else: self.hspeed -= function.sign(self.hspeed) * min(abs(self.hspeed), 600 * frametime)

        if player.up:
            self.jump(game, state)

        # gravitational force
        self.vspeed += 300 * frametime

        # TODO: air resistance, not hard limit
        self.vspeed = min(800, self.vspeed)

        # TODO: speed limit based on class
        self.hspeed = min(self.max_speed, max(-self.max_speed, self.hspeed))

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

    def jump(self, game, state):
        player = self.get_player(game, state)

        if player.up:
            if self.onground(game, state):
                self.vspeed = -200

    def die(self, game, state):
        # first we must unregister ourselves from our player
        self.get_player(game, state).character_id = None

        self.destroy()

    def get_player(self, game, state):
        return state.players[self.player_id]

class Scout(Character):
    # width, height of scout - rectangle collision
    collision_mask = mask.Mask(12, 33, True)
    max_speed = 252
    maxhp = 100

    def __init__(self, game, state, player_id):
        Character.__init__(self, game, state, player_id)

        self.hp = self.maxhp
        self.weapon = weapon.Scattergun(game, state, self.id).id
        self.can_doublejump = True

    def jump(self, game, state):
        if self.onground(game, state):
             self.vspeed = -200
    	     self.can_doublejump = True
        elif self.can_doublejump:
            self.vspeed = -200
            self.can_doublejump = False

class Soldier(Character):
    # width, height of scout - rectangle collision
    collision_mask = mask.Mask(12, 33, True)
    max_speed = 162
    maxhp = 150

    def __init__(self, game, state, player_id):
        Character.__init__(self, game, state, player_id)

        self.hp = self.maxhp
        self.weapon = weapon.Rocketlauncher(game, state, self.id).id
