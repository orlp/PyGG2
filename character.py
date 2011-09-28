import pygame
from pygame.locals import *
from collision import characterHitObstacle, objectCheckCollision
from gameobject import GameObject
from functions import sign, place_free, point_direction, load_image
from weapons import Weapon, ScatterGun

class Character(GameObject):
    def __init__(self, root):
        GameObject.__init__(self, root, 400, 400)
        self.up, self.left, self.right, self.LMB, self.RMB = 0, 0, 0, 0, 0
        self.flip = 0

    def step(self, frametime):
        if self.left: self.hspeed -= 3  * (frametime / 1000.0)
        if self.right: self.hspeed += 3 * (frametime / 1000.0)
        if not (self.left or self.right):
            if abs(self.hspeed) < .5: self.hspeed = 0
            else: self.hspeed /= 2.0  * (frametime / 1000.0)
        if self.up:
            #TODO if onground:
            self.vspeed = -8
        
        # gravitational force
        self.vspeed += 0.5  * (frametime / 1000.0)

        # TODO: air resistance, not hard limit
        self.vspeed = min(8, self.vspeed)
        
        # TODO: speed limit based on class
        self.hspeed = min(5, max(-5, self.hspeed))


    def endStep(self, frametime):
        GameObject.endStep(self, frametime)
        self.weapon.posUpdate()

    def collide(self):
        check = objectCheckCollision(self)
        
        if check: characterHitObstacle(self)

        GameObject.collide(self)


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

        self.sprite, self.rect = load_image("Sprites/Characters/Scout/Red/ScoutRedS_fr1.png")

        # The Scout hitbox: left = -6; right = 6; top = -10; bottom = 23
        self.rect = pygame.Rect(self.x - 6, self.y - 10, 12, 33)

        self.xImageOffset = -30
        self.yImageOffset = -30

        self.hp = 100
        self.maxHp = 100

        self.weapon = ScatterGun(self.root, self.x, self.y)
        self.weapon.owner = self

        self.xRectOffset = self.x-self.rect.centerx
        self.yRectOffset = self.y-self.rect.centery
