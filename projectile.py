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
    
    def interpolate(self, prev_obj, next_obj, alpha):
        super(Shot, self).interpolate(prev_obj, next_obj, alpha)
        self.direction = function.interpolate_angle(prev_obj.direction, next_obj.direction, alpha)

import character

class RocketDrawer(entity.EntityDrawer):
    def __init__(self, game, state, entity_id):
        super(RocketDrawer, self).__init__(game, state, entity_id)
    
        self.sprite = function.load_image("projectiles/rockets/0")
    
    def draw(self, game, state):
        rocket = self.get_entity(state)
        image = pygame.transform.rotate(self.sprite, rocket.direction)
        game.draw_world(image, (rocket.x, rocket.y))

class Rocket(entity.MovingObject):
    Drawer = RocketDrawer
    max_flight_time = 15
    damage = 35
    blastradius = 65
    knockback = 200
    
    def __init__(self, game, state, sourceweapon):
        super(Rocket, self).__init__(game, state)
        
        self.direction = 0.0
        self.flight_time = 0.0
        self.sourceweapon = sourceweapon
        
        srcwep = state.entities[sourceweapon]
        srcplayer = state.entities[srcwep.owner]
        
        self.x = srcplayer.x
        self.y = srcplayer.y

        self.fade = 0
        self.direction = srcwep.direction

        self.speed = 500
        self.hspeed = math.cos(math.radians(self.direction)) * self.speed
        self.vspeed = math.sin(math.radians(self.direction)) * -self.speed

    def destroy(self, game, state):
        if not self.fade:
            for obj in state.entities.values():
                if isinstance(obj, character.Character) and math.hypot(self.x - obj.x, self.y - obj.y) < self.blastradius:
                    force = (1-(math.hypot(self.x - obj.x, self.y - obj.y)/self.blastradius))*self.knockback
                    obj.hspeed += force*((obj.x-self.x)/math.hypot(self.x - obj.x, self.y - obj.y))
                    obj.vspeed += force*((obj.y-self.y)/math.hypot(self.x - obj.x, self.y - obj.y))/3
                    

        super(Rocket, self).destroy(state)

    def step(self, game, state, frametime):
        self.speed += 30 # Copied from GMK-GG2; should simulate some very basic acceleration+air resistance.
        self.speed *= 0.92

        self.hspeed = math.cos(math.radians(self.direction)) * self.speed
        self.vspeed = math.sin(math.radians(self.direction)) * -self.speed
        
        # calculate direction
        self.direction = function.point_direction(self.x - self.hspeed, self.y - self.vspeed, self.x, self.y)
        
    def endstep(self, game, state, frametime):
        super(Rocket, self).endstep(game, state, frametime)

        self.flight_time += frametime
        
        image = pygame.transform.rotate(self.drawer.sprite, self.direction)
        mask = pygame.mask.from_surface(image)
        if game.map.collision_mask.overlap(mask, (int(self.x), int(self.y))) or self.flight_time > self.max_flight_time:
            self.destroy(game, state)
    
    def interpolate(self, prev_obj, next_obj, alpha):
        super(Rocket, self).interpolate(prev_obj, next_obj, alpha)
        self.direction = function.interpolate_angle(prev_obj.direction, next_obj.direction, alpha)