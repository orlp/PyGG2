from __future__ import division

import pygame, math
from pygame.locals import *
import random

import gameobject
import function

class Shot(gameobject.Gameobject):
    shotsprite = function.load_image("sprites/projectiles/shots/0.png")
    max_flight_time = 1.5
    damage = 8
    
    def __init__(self, game, state, sourceweapon):
        gameobject.Gameobject.__init__(self, game, state)
        
        self.direction = 0.0
        self.flight_time = 0.0
        self.sourceweapon = sourceweapon
        
        srcwep, srcplayer = state.entities[sourceweapon], state.entities[state.entities[sourceweapon].owner]
        
        self.x = srcwep.x
        self.y = srcwep.y
        
        self.direction = srcwep.direction + (7 - random.randint(0, 15))
        
        speed = 300 + (20 - random.randint(0, 40))# TODO: Put the correct speed
        self.hspeed = math.cos(math.radians(self.direction)) * speed + srcplayer.hspeed/2
        self.vspeed = math.sin(math.radians(self.direction)) * -speed + srcplayer.vspeed/2

    def step(self, game, state, frametime):
        # gravitational force
        self.vspeed += 50 * frametime
        
        # calculate direction
        self.direction = function.point_direction(self.x - self.hspeed, self.y - self.vspeed, self.x, self.y)
        
        
    def endstep(self, game, state, frametime):
        gameobject.Gameobject.endstep(self, game, state, frametime)

        self.flight_time += frametime
        
        image = pygame.transform.rotate(self.shotsprite, self.direction)
        mask = pygame.mask.from_surface(image)
        if game.collisionmap.mask.overlap(mask, (int(self.x), int(self.y))) or self.flight_time > self.max_flight_time:
            self.destroy(state)
    
    def draw(self, game, state, frametime):
        image = pygame.transform.rotate(self.shotsprite, self.direction)
        game.draw_in_view(image, (self.x, self.y))
    
    def interpolate(self, next_object, alpha):
        gameobject.Gameobject.interpolate(self, next_object, alpha)
        self.direction = self.direction * (1 - alpha) + next_object.direction * alpha
