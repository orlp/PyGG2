#!/usr/bin/env python

from __future__ import division, print_function

import math
import struct

import function
import entity
import weapon
import mask

class Character(entity.MovingObject):
    acceleration = 1200
    friction = 0.035 # friction factor per second of null movement

    def __init__(self, game, state, player_id):
        super(Character, self).__init__(game, state)
        
        
        self.player_id = player_id

        self.flip = False # are we flipped around?
        self.intel = False # has intel (for drawing purposes)
        self.just_spawned = False # have we just spawned?
        # time tracker for the moving of the character's legs
        self.animoffset = 0.0
        self.hp_offset = -1 # FIXME: REMOVE; THIS ONLY EXISTS FOR HEALTH HUD TESTING

        self.can_doublejump = False
        self.desired_direction = 0
        
        self.issynced = True

    def step(self, game, state, frametime):

        player = self.get_player(game, state)

        # this is quite important, if hspeed / 20 drops below 1 self.animoffset will rapidly change and cause very fast moving legs (while we are moving very slow)
        if abs(self.hspeed) > 20:
            self.animoffset += frametime * abs(self.hspeed) / 20
            self.animoffset %= 2
        if abs(self.hspeed) == 0:
            self.animoffset = 0

        self.flip = not (player.aimdirection < 90 or player.aimdirection > 270)

        # awesome handy movement code
        # current code essentially goes in the most recent direction pressed,
        # unlike the null movement in Source or the "preferred direction" that's
        # present in a lot of indie games (aigh)
        # rewrite acceptable if it makes it less shitload of code :[
        apply_friction = False
        if player.left and not player.last_left:    # left  movement
            self.desired_direction = -1
        elif player.last_left and not player.left:  # right movement
            if player.right:
                self.desired_direction =  1
            else:                                   # null  movement
                self.desired_direction =  0
        if player.right and not player.last_right:  # right movement
            self.desired_direction =  1
        elif player.last_right and not player.right:# left  movement
            if player.left:
                self.desired_direction = -1
            else:                                   # null  movement
                self.desired_direction =  0
            
        if self.desired_direction == -1:            # left  movement
            if hspeed > 0:
                self.hspeed *= self.friction  ** frametime
            self.hspeed -= self.acceleration * frametime
        if self.desired_direction ==  1:            # right movement
            if hspeed < 0:
                self.hspeed *= self.friction  ** frametime
            self.hspeed += self.acceleration * frametime
        if self.desired_direction ==  0:            # null movement
            self.hspeed *= self.friction  ** frametime
        
        if abs(self.hspeed) < 10:
            self.hspeed = 0

        if player.up and not player.old_up:
            self.jump(game, state)
        player.old_up = player.up

        # gravitational force
        self.vspeed += 700 * frametime

        # TODO: air resistance, not hard limit
        self.vspeed = min(800, self.vspeed)
        # note: air resistance might have awkward side effects if implemented "naturally".
        # Please consider resistance that's amplified at higher speeds & a threshold.
        
        # hspeed limit
        self.hspeed = min(self.max_speed, max(-self.max_speed, self.hspeed))
        
        self.hp+=self.hp_offset # test health change
        if self.hp < 0:
            self.hp_offset = 1
        if self.hp > self.maxhp:
            self.hp_offset = -1
        
    def endstep(self, game, state, frametime):
        
        player = self.get_player(game, state)
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
            
        player.last_left = player.left;
        player.last_right = player.right;

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
                self.vspeed = -300

    def die(self, game, state):
        # first we must unregister ourselves from our player
        self.get_player(game, state).character_id = None
        self.get_player(game, state).respawntimer = 1# in seconds

        # Then we have to destroy our weapon
        state.entities[self.weapon].destroy(state)
        # TODO: destroy our sentry
        self.destroy(state)

    def get_player(self, game, state):
        return state.players[self.player_id]

    def serialize(self, state):
        packetstr = ""
        packetstr += struct.pack(">IIii", self.x, self.y, self.hspeed, self.vspeed)

        # Serialize intel, doublejump, etc... in one byte. Should we merge this with the input serialization in Player? Move the input ser. here?
        byte = 0
        byte |= self.intel << 0
        byte |= self.can_doublejump << 1
        #byte |= self.sentry << 2
        packetstr += struct.pack(">B", byte)

        packetstr += state.entities[self.weapon].serialize(state)

        return packetstr

    def deserialize(self, state, packetstr):
        self.x, self.y, self.hspeed, self.vspeed = struct.unpack_from(">IIii", packetstr)
        packetstr = packetstr[16:]
        byte = struct.unpack_from(">B", packetstr)[0]
        packetstr = packetstr[1:]
        self.intel = byte & (1 << 0)
        self.can_doublejump = byte & (1 << 1)
        #self.sentry = byte & (1 << 2)

        weapon_string_length = state.entities[self.weapon].deserialize(state, packetstr)
        return struct.calcsize(">IIiiB")+weapon_string_length

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
            self.vspeed = -300
            self.can_doublejump = True
        elif self.can_doublejump:
            self.vspeed = -300
            self.can_doublejump = False

class Pyro(Character):
    #FIXME: width, height of pyro - rectangle collision
    collision_mask = mask.Mask(12, 33, True)
    max_speed = 198
    maxhp = 120

    def __init__(self, game, state, player_id):
        Character.__init__(self, game, state, player_id)

        self.hp = self.maxhp
        self.weapon = weapon.Flamethrower(game, state, self.id).id

class Soldier(Character):
    # FIXME: width, height of soldier - rectangle collision
    collision_mask = mask.Mask(12, 33, True)
    max_speed = 162
    maxhp = 150

    def __init__(self, game, state, player_id):
        Character.__init__(self, game, state, player_id)

        self.hp = self.maxhp
        self.weapon = weapon.Rocketlauncher(game, state, self.id).id
        
class Demoman(Character):
    #TODO: this class
    # FIXME: width, height of heavy - rectangle collision
    collision_mask = mask.Mask(12, 33, True)
    max_speed = 144
    maxhp = 200

    def __init__(self, game, state, player_id):
        Character.__init__(self, game, state, player_id)

        self.hp = self.maxhp
        self.weapon = weapon.Minigun(game, state, self.id).id

    def step(self, game, state, frametime):
        Character.step(self, game, state, frametime)
        if self.get_player(game, state).leftmouse:
            self.hspeed = min(54, max(-54, self.hspeed))

class Heavy(Character):
    # FIXME: width, height of heavy - rectangle collision
    collision_mask = mask.Mask(12, 33, True)
    max_speed = 144
    maxhp = 200

    def __init__(self, game, state, player_id):
        Character.__init__(self, game, state, player_id)

        self.hp = self.maxhp
        self.weapon = weapon.Minigun(game, state, self.id).id

    def step(self, game, state, frametime):
        Character.step(self, game, state, frametime)
        if self.get_player(game, state).leftmouse:
            self.hspeed = min(54, max(-54, self.hspeed))
            
class Medic(Character):
    # FIXME: width, height of Medic - rectangle collision
    # FIXME: offsets to be proper
    collision_mask = mask.Mask(12, 33, True)
    max_speed = 175
    maxhp = 120

    def __init__(self, game, state, player_id):
        Character.__init__(self, game, state, player_id)

        self.hp = self.maxhp
        self.weapon = weapon.Medigun(game, state, self.id).id
        
class Engineer(Character):
    # FIXME: width, height of engineer - rectangle collision
    collision_mask = mask.Mask(12, 33, True)
    max_speed = 180
    maxhp = 120

    def __init__(self, game, state, player_id):
        Character.__init__(self, game, state, player_id)

        self.hp = self.maxhp
        self.weapon = weapon.Shotgun(game, state, self.id).id

class Spy(Character):
    # FIXME: width, height of spy - rectangle collision
    collision_mask = mask.Mask(12, 33, True)
    max_speed = 194.4
    maxhp = 100

    def __init__(self, game, state, player_id):
        Character.__init__(self, game, state, player_id)

        self.hp = self.maxhp
        self.weapon = weapon.Revolver(game, state, self.id).id
        self.cloaking = False

class Sniper(Character):
    # FIXME: width, height of heavy - rectangle collision
    # TODO: this class
    collision_mask = mask.Mask(12, 33, True)
    max_speed = 144
    maxhp = 200

    def __init__(self, game, state, player_id):
        Character.__init__(self, game, state, player_id)

        self.hp = self.maxhp
        self.weapon = weapon.Minigun(game, state, self.id).id
