from __future__ import division

import math, pygame
from pygame.locals import *

import gameobject
import function
import weapons

class Character(gameobject.Gameobject):
    def __init__(self, game, state):
        Gameobject.__init__(self, game, state)
        
        self.flip = False # are we flipped around?

    def step(self, game, state, frametime):
        if game.left: self.hspeed -= 1000 * frametime
        if game.right: self.hspeed += 1000 * frametime
        if not (game.left or game.right):
            if abs(self.hspeed) < 10: self.hspeed = 0
            else: self.hspeed -= function.sign(self.hspeed) * min(abs(self.hspeed), 1000 * frametime)
        if game.up:
            if self.onground():
                self.vspeed = -200
                
        # gravitational force
        self.vspeed += 300 * frametime

        # TODO: air resistance, not hard limit
        self.vspeed = min(800, self.vspeed)
        
        # TODO: speed limit based on class
        self.hspeed = min(120, max(-120, self.hspeed))

    def endstep(self, game, state, frametime):
        # check if we are on the ground before moving (for walking over 1 unit walls)
        onground = self.onground()
        
        # first we move, ignoring walls
        self.x += self.hspeed * frametime
        
        # if we are in a wall now, we must move back
        if game.collisionmap.mask.overlap(self.mask, (int(self.x), int(self.y))):
            # but if we just walked onto a one-unit wall it's ok
            # but we had to be on the ground
            if onground and not game.collisionmap.mask.overlap(self.mask, (int(self.x), int(self.y - 6))):
                # only walk up if necessary
                while game.collisionmap.mask.overlap(self.mask, (int(self.x), int(self.y))):
                    self.y -= 1
            else:
                self.x = math.floor(self.x) # move back to a whole pixel - TODO math.floor/math.ceil depending on direction
                
                # and if one pixel wasn't enough
                while game.collisionmap.mask.overlap(self.mask, (int(self.x), int(self.y))):
                    self.x -= function.sign(self.hspeed)
                
                self.hspeed = 0
        
        # same stuff, but now vertically
        self.y += self.vspeed * frametime
        
        if game.collisionmap.mask.overlap(self.mask, (int(self.x), int(self.y))):
            self.y = float(int(self.y))
            
            while game.collisionmap.mask.overlap(self.mask, (int(self.x), int(self.y))):
                self.y -= sign(self.vspeed)
        
            self.vspeed = 0
        
        # just to be sure
        self.x = max(self.x, 0)
        self.y = max(self.y, 0)
    
        self.weapon.posupdate()

    def draw(self, game, state, surface):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.flip = function.point_direction(self.x, self.y, mouse_x + game.xview, mouse_y + game.yview) > 90 and point_direction(self.x, self.y, mouse_x + game.xview, mouse_y + game.yview) < 270
        
        
        Gameobject.draw(self)
    
    def onground(self):
        # are we on the ground? About half an unit from the ground is enough to qualify for this
        return game.collisionmap.mask.overlap(self.mask, (int(self.x), int(self.y + 3)))


class Scout(Character):
    mask = pygame.mask.Mask((12, 33)) # width, height of scout - rectangle collision
    sprite = function.load_image("sprites/characters/scoutreds/0.png")
    spriteoffset = (-24, -30)
    weaponoffset = (8, 2) # where the character should carry it's gun
    maxhp = 100
    
    def __init__(self, game, state):
        Character.__init__(self, game, state)

        self.hp = self.maxhp
        
        weapon = Scattergun(self, game, state)
        weapon.owner = self.id
        self.weapon = weapon.id
