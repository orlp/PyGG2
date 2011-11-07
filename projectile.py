#!/usr/bin/env python

from __future__ import division, print_function

import pygame, math
from pygame.locals import *
import random

import entity
import function

class ShotDrawer(entity.EntityDrawer):
    shotsprite_angles = {} # rotating is expensive, we save each rotated sprite per angle (integers)

    def __init__(self, game, state, entity_id):
        super(ShotDrawer, self).__init__(game, state, entity_id)
    
        self.shotsprite = function.load_image("projectiles/shots/0")
    
    def draw(self, game, state):
        shot = self.get_entity(state)
        maxsize = max(self.shotsprite.get_size())
        
        # OPTIMIZATION don't bother doing anything at all if we are offscreen
        if game.is_onscreen((shot.x, shot.y), (maxsize, maxsize)):
            dir = int(shot.direction) % 360
            
            if dir in self.shotsprite_angles:
                sprite = self.shotsprite_angles[dir]
            else:
                sprite = pygame.transform.rotate(self.shotsprite, dir)
                self.shotsprite_angles[dir] = sprite
            
            game.draw_world(sprite, (shot.x, shot.y))

class Shot(entity.MovingObject):
    Drawer = ShotDrawer
    
    max_flight_time = 1.5
    damage = 8
    
    def __init__(self, game, state, sourceweapon):
        super(Shot, self).__init__(game, state)
        
        self.direction = 0.0
        self.flight_time = 0.0
        self.sourceweapon = sourceweapon
        
        srcwep = state.entities[sourceweapon]
        srcplayer = state.entities[srcwep.owner]
        
        self.x = srcplayer.x
        self.y = srcplayer.y
        
        self.direction = srcwep.direction + (7 - random.randint(0, 15))
        self.mask = pygame.mask.from_surface(pygame.transform.rotate(self.drawer.shotsprite, self.direction))
        
        # add user speed to bullet speed but don't change direction of the bullet
        playerdir = math.degrees(math.atan2(-srcplayer.vspeed, srcplayer.hspeed))
        diffdir = self.direction - playerdir
        playerspeed = math.hypot(srcplayer.hspeed, srcplayer.vspeed)
        speed = 500 + math.cos(math.radians(diffdir)) * playerspeed
        
        self.hspeed = math.cos(math.radians(self.direction)) * speed
        self.vspeed = math.sin(math.radians(self.direction)) * -speed

    def step(self, game, state, frametime):
        # gravitational force
        self.vspeed += 50 * frametime
        
        # calculate direction
        self.direction = function.point_direction(self.x - self.hspeed, self.y - self.vspeed, self.x, self.y)
    
    def endstep(self, game, state, frametime):
        super(Shot, self).endstep(game, state, frametime)

        self.flight_time += frametime
        
        if game.map.collision_mask.overlap(self.mask, (int(self.x), int(self.y))) or self.flight_time > self.max_flight_time:
            self.destroy(state)
    
    def interpolate(self, next_object, alpha):
        super(Shot, self).interpolate(next_object, alpha)
        self.direction = function.interpolate_angle(self.direction, next_object.direction, alpha)