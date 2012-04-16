#!/usr/bin/env python

from __future__ import division, print_function

import entity
import mask

class Building_Sentry(entity.MovingObject):
    max_hp = 100 # Maximum hitpoints the sentry can ever have
    starting_hp = 25 # At what hitpoints the sentry will start building
    collision_mask = mask.Mask(26, 19, True) # TODO: Implement changing masks
    build_time = 2 # Number of secs it takes to build
    hp_increment = (max_hp-starting_hp)/build_time
    animation_increment = 10/build_time # 10 == number of frames in sentry build animation

    def __init__(self, game, state, owner):
        super(Building_Sentry, self).__init__(game, state)

        self.hp = self.starting_hp
        self.isfalling = True
        self.animation_frame = 0
        self.building_time = 0

        self.owner_id = owner.id
        character = state.entities[owner.character_id]
        self.x = character.x
        self.y = character.y

    def step(self, game, state, frametime):
        if self.isfalling:
            # If we've hit the floor, get us back out and build
            while game.map.collision_mask.overlap(self.collision_mask, (int(self.x), int(self.y))):
                self.y -= 1
                self.isfalling = False

            # Gravity
            self.vspeed += 300 * frametime

            # TODO: air resistance, not hard limit
            self.vspeed = min(800, self.vspeed)

        if not self.isfalling:
            print(self.animation_frame)
            self.hspeed = 0
            self.vspeed = 0

            if self.hp <= 0:
                self.destroy(state)
                return

            if self.building_time >= self.build_time:
                # Cap hp at max hp
                if self.hp >= self.max_hp:
                    self.hp = self.max_hp
                # Create a finished sentry, and destroy the building sentry object
                owner = state.players[self.owner_id]
                owner.sentry = Sentry(game, state, self.owner_id, self.x, self.y, self.hp)
                self.destroy(state)
            else:
                # Continue building
                self.hp += self.hp_increment * frametime
                self.building_time += frametime
                self.animation_frame += self.animation_increment * frametime

    def interpolate(self, prev_obj, next_obj, alpha):
        super(Building_Sentry, self).interpolate(prev_obj, next_obj, alpha)
        self.animation_frame = prev_obj.animation_frame + (next_obj.animation_frame - prev_obj.animation_frame) * alpha
        self.hp = prev_obj.hp + (next_obj.hp - prev_obj.hp) * alpha
        self.build_time = prev_obj.build_time + (next_obj.build_time - prev_obj.build_time) * alpha

    def destroy(self, state):
        # TODO: Sentry destruction syncing, bubble
        super(Building_Sentry, self).destroy(state)
        owner = state.players[self.owner_id]
        owner.sentry = None


class Sentry(entity.MovingObject):
    collision_mask = mask.Mask(26, 19, True)

    def __init__(self, game, state, owner_id, x, y, hp):
        self.owner_id = owner_id
        self.aiming_direction = 0
        self.x = x
        self.y = y
        self.hp = hp

    def step(self, game, state, frametime):
        # TODO: Aim at nearest enemy
        if hp <= 0:
            self.destroy(state)

    def interpolate(self, prev_obj, next_obj, alpha):
        super(Sentry, self).interpolate(prev_obj, next_obj, alpha)
        self.hp = prev_obj.hp + (next_obj.hp - prev_obj.hp) * alpha

    def destroy(self, state):
        # TODO: Sentry destruction syncing, bubble
        super(Sentry, self).destroy(state)
        owner = state.players[self.owner_id]
        owner.sentry = None
