#!/usr/bin/env python

from __future__ import division, print_function

import pygame, math
from pygame.locals import *
import random

import entity
import character
import function
import mask
import Image

class ShotDrawer(entity.EntityDrawer):
    shotsprite_angles = {} # rotating is expensive, we save each rotated sprite per angle (integers)

    def __init__(self, game, state, entity_id):
        super(ShotDrawer, self).__init__(game, state, entity_id)
    
        self.shotsprite = function.load_image("projectiles/shots/0")
        
        # initiate shot sprite for every angle 0 <= a <= 360
        if not self.shotsprite_angles:
            for angle in range(361):
                self.shotsprite_angles[angle] = pygame.transform.rotate(self.shotsprite, angle)
        
    def draw(self, game, state, frametime):
        shot = self.get_entity(state)
        angle = int(shot.direction) % 360
        
        image = self.shotsprite_angles[angle]
        
        if shot.max_flight_time - shot.flight_time < shot.fade_time:
            image.set_alpha(255 * (shot.max_flight_time - shot.flight_time) / shot.fade_time)
        else: image.set_alpha(255)
        
        game.draw_world(image, (shot.x, shot.y))

class Shot(entity.MovingObject):
    Drawer = ShotDrawer
    
    shot_hitmasks = {} # rotating is expensive, we save each rotated mask per angle (integers)
    
    fade_time = .2 # seconds of fading when max_flight_time is being reached
    max_flight_time = 1.5
    damage = 8
    
    def __init__(self, game, state, sourceweapon):
        super(Shot, self).__init__(game, state)
        
        # initiate shot hitmask for every angle 0 <= a <= 360
        if not self.shot_hitmasks:
            collisionmask = mask.from_image("sprites/projectiles/shots/0.png")
            for angle in range(361):
                self.shot_hitmasks[angle] = collisionmask.rotate(angle)
        
        self.direction = 0.0
        self.flight_time = 0.0
        self.sourceweapon = sourceweapon
        
        srcwep = state.entities[sourceweapon]
        srcplayer = state.entities[srcwep.owner]
        
        self.x = srcplayer.x
        self.y = srcplayer.y
        
        self.direction = srcwep.direction + (7 - random.randint(0, 15))
        
        # add user speed to bullet speed but don't change direction of the bullet
        playerdir = math.degrees(math.atan2(-srcplayer.vspeed, srcplayer.hspeed))
        diffdir = self.direction - playerdir
        playerspeed = math.hypot(srcplayer.hspeed, srcplayer.vspeed)
        speed = 330 + random.randint(0, 4)*30 + math.cos(math.radians(diffdir)) * playerspeed
        
        self.hspeed = math.cos(math.radians(self.direction)) * speed
        self.vspeed = math.sin(math.radians(self.direction)) * -speed

    def step(self, game, state, frametime):
        # gravitational force
        self.vspeed += 4.5 * frametime
        
        # calculate direction
        self.direction = function.point_direction(self.x - self.hspeed, self.y - self.vspeed, self.x, self.y)
    
    def endstep(self, game, state, frametime):
        super(Shot, self).endstep(game, state, frametime)

        self.flight_time += frametime
        
        dir = int(self.direction) % 360
        if game.map.collision_mask.overlap(self.shot_hitmasks[dir], (int(self.x), int(self.y))) or self.flight_time > self.max_flight_time:
            self.destroy(state)
    
    def interpolate(self, prev_obj, next_obj, alpha):
        super(Shot, self).interpolate(prev_obj, next_obj, alpha)
        self.direction = function.interpolate_angle(prev_obj.direction, next_obj.direction, alpha)

class RocketDrawer(entity.EntityDrawer):
    rocketsprite_angles = {} # rotating is expensive, we save each rotated sprite per angle (integers)
    
    def __init__(self, game, state, entity_id):
        super(RocketDrawer, self).__init__(game, state, entity_id)
    
        self.rocketsprite = function.load_image("projectiles/rockets/0")
        
        # initiate rocket sprite for every angle 0 <= a <= 360
        if not self.rocketsprite_angles:
            for angle in range(361):
                self.rocketsprite_angles[angle] = pygame.transform.rotate(self.rocketsprite, angle)
    
    def draw(self, game, state, frametime):
        rocket = self.get_entity(state)
        angle = int(rocket.direction) % 360
        
        image = self.rocketsprite_angles[angle]
        
        if rocket.max_flight_time - rocket.flight_time < rocket.fade_time:
            image.set_alpha(255 * (rocket.max_flight_time - rocket.flight_time) / rocket.fade_time)
        else: image.set_alpha(255)
        
        game.draw_world(image, (rocket.x, rocket.y))

class Rocket(entity.MovingObject):
    Drawer = RocketDrawer
    
    fade_time = .3 # seconds of fading when max_flight_time is being reached
    max_flight_time = 20
    damage = 35
    blastradius = 65
    knockback = 1200
    
    rocket_hitmasks = {} # rotating is expensive, we save each rotated mask per angle (integers)
    
    def __init__(self, game, state, sourceweapon):
        super(Rocket, self).__init__(game, state)
        
        # initiate shot hitmask for every angle 0 <= a <= 360
        if not self.rocket_hitmasks:
            collisionmask = mask.from_image("sprites/projectiles/rockets/0.png")
            for angle in range(361):
                self.rocket_hitmasks[angle] = collisionmask.rotate(angle)
        
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
        
        angle = int(self.direction) % 360
        if game.map.collision_mask.overlap(self.rocket_hitmasks[angle], (int(self.x), int(self.y))) or self.flight_time > self.max_flight_time:
            self.destroy(game, state)
    
    def interpolate(self, prev_obj, next_obj, alpha):
        super(Rocket, self).interpolate(prev_obj, next_obj, alpha)
        self.direction = function.interpolate_angle(prev_obj.direction, next_obj.direction, alpha)