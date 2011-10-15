from __future__ import division

import pygame
from pygame.locals import *
from gameobject import GameObject
from functions import sign, place_free, point_direction, load_image
from weapons import Weapon, ScatterGun, ShotGun, Revolver

class Character(GameObject):
    def __init__(self, root):
        GameObject.__init__(self, root, 400*6, 50)
        self.flip = 0

    def step(self, frametime):
        if self.root.left: self.hspeed -= 1000 * frametime
        if self.root.right: self.hspeed += 1000 * frametime
        if not (self.root.left or self.root.right):
            if abs(self.hspeed) < 10: self.hspeed = 0
            else: self.hspeed -= sign(self.hspeed) * min(abs(self.hspeed), 1000 * frametime)
        if self.root.up:
            if self.onground():
                self.vspeed = -200
                
        # gravitational force
        self.vspeed += 300  * frametime

        # TODO: air resistance, not hard limit
        self.vspeed = min(800, self.vspeed)
        
        # TODO: speed limit based on class
        self.hspeed = min(120, max(-120, self.hspeed))


    def endstep(self, frametime):
        # check if we are on the ground before moving (for walking over 1 unit walls)
        onground = self.onground()
        
        # first we move, ignoring walls
        self.x += self.hspeed * frametime
        
        # if we are in a wall now, we must move back
        if self.root.collisionmap.mask.overlap(self.mask, (int(self.x), int(self.y))):
            # but if we just walked onto a one-unit wall it's ok
            # but we had to be on the ground
            if onground and not self.root.collisionmap.mask.overlap(self.mask, (int(self.x), int(self.y - 6))):
                # only walk up if necessary
                while self.root.collisionmap.mask.overlap(self.mask, (int(self.x), int(self.y))):
                    self.y -= 1
            else:
                self.x = float(int(self.x)) # move back to a whole pixel
                
                # and if one pixel wasn't enough
                while self.root.collisionmap.mask.overlap(self.mask, (int(self.x), int(self.y))):
                    self.x -= sign(self.hspeed)
                
                self.hspeed = 0
        
        # same stuff, but now vertically
        self.y += self.vspeed * frametime
        
        if self.root.collisionmap.mask.overlap(self.mask, (int(self.x), int(self.y))):
            self.y = float(int(self.y))
            
            while self.root.collisionmap.mask.overlap(self.mask, (int(self.x), int(self.y))):
                self.y -= sign(self.vspeed)
        
            self.vspeed = 0
        
        # just to be sure
        self.x = max(self.x, 0)
        self.y = max(self.y, 0)
    
        self.weapon.posUpdate()

    def draw(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if point_direction(self.x, self.y, mouse_x + self.root.xview, mouse_y + self.root.yview) > 90 and point_direction(self.x, self.y, mouse_x + self.root.xview, mouse_y + self.root.yview) < 270:
            if self.flip == 0:
                self.image = pygame.transform.flip(self.image, 1, 0)
                self.flip = 1
        else:
            if self.flip:
                self.image = pygame.transform.flip(self.image, 1, 0)
                self.flip = 0

        GameObject.draw(self)
    
    def onground(self):
        # are we on the ground? About half an unit from the ground is enough to qualify for this
        return self.root.collisionmap.mask.overlap(self.mask, (int(self.x), int(self.y + 3)))


class Scout(Character):
    def __init__(self, root):
        Character.__init__(self, root)
        
        # The Scout hitbox: left = 24; top = 30; width = 12; height = 33;
        self.rect = pygame.Rect(24, 30, 12, 33)

        self.image = load_image("sprites/characters/scoutreds/0.png")
        self.mask = pygame.mask.Mask((12, 33)) # width, height of scout - rectangle collision
        self.mask.fill()

        self.hp = 100
        self.maxHp = 100

        self.weapon = ScatterGun(self.root, self, self.x, self.y)
