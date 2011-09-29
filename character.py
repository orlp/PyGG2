from __future__ import division

import pygame
from pygame.locals import *
from collision import characterHitObstacle, objectCheckCollision
from gameobject import GameObject
from functions import sign, place_free, point_direction, load_image
from weapons import Weapon, ScatterGun

class Character(GameObject):
    def __init__(self, root):
        GameObject.__init__(self, root, 0, 0)
        self.flip = 0

    def step(self, frametime):
        if self.root.left: self.hspeed -= 1000 * frametime
        if self.root.right: self.hspeed += 1000 * frametime
        if not (self.root.left or self.root.right):
            if abs(self.hspeed) < 10: self.hspeed = 0
            else: self.hspeed -= sign(self.hspeed) * min(abs(self.hspeed), 1000 * frametime)
        if self.root.up:
            #TODO if onground:
            self.vspeed = -80
        
        # gravitational force
        self.vspeed += 100  * frametime

        # TODO: air resistance, not hard limit
        self.vspeed = min(100, self.vspeed)
        
        # TODO: speed limit based on class
        self.hspeed = min(120, max(-120, self.hspeed))


    def endStep(self, frametime):
        GameObject.endStep(self, frametime)
        self.weapon.posUpdate()

    def collide(self, frametime):
        check = objectCheckCollision(self)
        
        if check: characterHitObstacle(self, frametime)

        GameObject.collide(self, frametime)


    def draw(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if point_direction(self.x, self.y, mouse_x + self.root.Xview, mouse_y + self.root.Yview) > 90 and point_direction(self.x, self.y, mouse_x + self.root.Xview, mouse_y + self.root.Yview) < 270:
            if self.flip == 0:
                self.sprite = pygame.transform.flip(self.sprite, 1, 0)
                self.flip = 1
        else:
            if self.flip:
                self.sprite = pygame.transform.flip(self.sprite, 1, 0)
                self.flip = 0

        GameObject.draw(self)



class Scout(Character):
    def __init__(self, root):
        Character.__init__(self, root)

        self.sprite = load_image("Sprites/Characters/ScoutRedS/0.png")

        # The Scout hitbox: left = -6; right = 6; top = -10; bottom = 23
        self.rect = pygame.Rect(self.x - 6, self.y - 10, 12, 33)

        self.xImageOffset = 30
        self.yImageOffset = 40

        self.hp = 100
        self.maxHp = 100

        self.weapon = ScatterGun(self.root, self.x, self.y)
        self.weapon.owner = self

        self.xRectOffset = self.x - self.rect.centerx
        self.yRectOffset = self.y - self.rect.centery
