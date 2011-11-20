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
        
    def draw(self, game, state, frametime):
        shot = self.get_entity(state)
        angle = int(shot.direction) % 360
        
        if angle in self.shotsprite_angles:
            image = self.shotsprite_angles[angle]
        else:
            image = pygame.transform.rotate(self.shotsprite, angle)
            self.shotsprite_angles[angle] = image
        
        if shot.max_flight_time - shot.flight_time < shot.fade_time:
            image.set_alpha(255 * (shot.max_flight_time - shot.flight_time) / shot.fade_time)
        else: image.set_alpha(255)

        game.draw_world(image, (shot.x, shot.y))

class Shot(entity.MovingObject):
    Drawer = ShotDrawer
    
    shot_hitmasks = {}
    
    fade_time = 0.8 # seconds of fading when max_flight_time is being reached
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
        
        angle = int(self.direction) % 360
        if angle in self.shot_hitmasks:
            mask = self.shot_hitmasks[angle]
        else:
            mask = function.load_mask("projectiles/shots/0").rotate(angle)
            self.shot_hitmasks[angle] = mask
        
        if game.map.collision_mask.overlap(mask, (int(self.x), int(self.y))) or self.flight_time > self.max_flight_time:
            # calculate unit speeds (speeds normalized into the range 0-1)
            h_unit_speed = math.cos(math.radians(self.direction))
            v_unit_speed = -math.sin(math.radians(self.direction))
            
            x, y = self.x, self.y
            
            # move back until we're not colliding anymore - this is the colliding point
            while game.map.collision_mask.overlap(mask, (int(x), int(y))):
                x -= h_unit_speed
                y -= v_unit_speed
                
            self.destroy(state)
    
    def interpolate(self, prev_obj, next_obj, alpha):
        super(Shot, self).interpolate(prev_obj, next_obj, alpha)
        self.direction = function.interpolate_angle(prev_obj.direction, next_obj.direction, alpha)

class RocketDrawer(entity.EntityDrawer):
    rocketsprite_angles = {} # rotating is expensive, we save each rotated sprite per angle (integers)
    
    def __init__(self, game, state, entity_id):
        super(RocketDrawer, self).__init__(game, state, entity_id)
    
        self.rocketsprite = function.load_image("projectiles/rockets/0")
    
    def draw(self, game, state, frametime):
        rocket = self.get_entity(state)
        angle = int(rocket.direction) % 360
        
        if angle in self.rocketsprite_angles:
            image = self.rocketsprite_angles[angle]
        else:
            image = pygame.transform.rotate(self.rocketsprite, angle)
            self.rocketsprite_angles[angle] = image
        
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
    knockback = 8/30
    
    rocket_hitmasks = {}
    
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
                    force = (1-(math.hypot(self.x - obj.x, self.y - obj.y)/self.blastradius))*(self.knockback*frametime)# TODO: Fix Frametime
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
        if angle in self.rocket_hitmasks:
            mask = self.rocket_hitmasks[angle]
        else:
            mask = function.load_mask("projectiles/rockets/0").rotate(angle)
            self.rocket_hitmasks[angle] = mask
        
        if game.map.collision_mask.overlap(mask, (int(self.x), int(self.y))) or self.flight_time > self.max_flight_time:
            self.destroy(game, state)
    
    def interpolate(self, prev_obj, next_obj, alpha):
        super(Rocket, self).interpolate(prev_obj, next_obj, alpha)
        self.direction = function.interpolate_angle(prev_obj.direction, next_obj.direction, alpha)
