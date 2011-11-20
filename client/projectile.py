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

class ShotRenderer(entity.EntityRenderer):
    shotsprite_angles = {} # rotating is expensive, we save each rotated sprite per angle (integers)

    def __init__(self, renderer, state, entity_id):
        super(ShotRenderer, self).__init__(renderer, state, entity_id)
    
        self.shotsprite = function.load_image("projectiles/shots/0")
        
    def render(self, renderer, state, frametime):
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

        renderer.draw_world(image, (shot.x, shot.y))

class RocketRenderer(entity.EntityRenderer):
    rocketsprite_angles = {} # rotating is expensive, we save each rotated sprite per angle (integers)
    
    def __init__(self, renderer, state, entity_id):
        super(RocketRenderer, self).__init__(renderer, state, entity_id)
    
        self.rocketsprite = function.load_image("projectiles/rockets/0")
    
    def render(self, renderer, state, frametime):
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
        
        renderer.draw_world(image, (rocket.x, rocket.y))