#!/usr/bin/env python

from __future__ import division, print_function

import entity
import mask

class Building_Sentry(entity.MovingObject):
    max_hp = 100 # Maximum hitpoints the sentry can ever have
    starting_hp = 25 # At what hitpoints the sentry will start building
    build_time = 2 # Number of secs it takes to build
    collision_mask = mask.Mask(26, 19, True) # TODO: Implement changing masks

    hp_increment = (max_hp-starting_hp)/build_time
    animation_increment = 10/build_time # 10 == number of frames in sentry build animation

    def __init__(self, game, state, owner):
        super(Building_Sentry, self).__init__(game, state)

        self.hp = self.starting_hp
        self.isfalling = True
        self.animation_frame = 0

        self.owner_id = owner.id
        self.x = owner.x
        self.y = owner.y

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
            self.hspeed = 0
            self.vspeed = 0

            if self.hp >= self.max_hp:
                self.hp = self.max_hp
                # Create a finished sentry, and destroy the building sentry object
                #self.owner.sentry = Sentry(game, state, self.owner)
                self.destroy(state)
            else:
                self.hp += self.hp_increment * frametime
                self.animation_frame += self.animation_increment * frametime
