import pygame
from pygame.locals import *
from load_image import load_image
from collision import characterHitObstacle, objectCheckCollision
from gameobject import GameObject
from functions import sign, place_free, lengthdir, point_direction
from Weapons import Weapon, ScatterGun

class Character(GameObject):

    def __init__(self, root):

        GameObject.__init__(self, root, 400, 400)
        self.up, self.left, self.right, self.LMB, self.RMB = 0, 0, 0, 0, 0
        self.hp = 0
        self.flip = 0


    def lateInit(self):

        # This is called -after- the child's init event, so it can set things that are known only later.
        self.maxHp = self.hp


    def step(self):

        if self.up:
            self.vspeed -= 2

        if self.left:
            self.hspeed -= 1
        elif self.right:
            self.hspeed += 1


        self.vspeed += 0.2

        if self.vspeed > 5:
            self.vspeed = 5
        elif self.vspeed < -5:
            self.vspeed = -5

        if self.hspeed > 5:
            self.hspeed = 5
        elif self.hspeed < -5:
            self.hspeed = -5


    def endStep(self):

        GameObject.endStep(self)

        self.weapon.posUpdate()


    def collide(self):

        check = objectCheckCollision(self)

        if check:
            characterHitObstacle(self)

        GameObject.collide(self)


    def draw(self):

        (mouse_x, mouse_y) = pygame.mouse.get_pos()

        if point_direction(self.x, self.y, mouse_x+self.root.Xview, mouse_y+self.root.Yview) > 90 and point_direction(self.x, self.y, mouse_x+self.root.Xview, mouse_y+self.root.Yview) < 270:

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

        self.sprite, self.rect = load_image('Sprites/Characters/Scout/Red/ScoutRedS_fr1.png')

        # The Scout hitbox: left = -6; right = 6; top = -10; bottom = 23
        self.rect = pygame.Rect(self.x-6, self.y-10, 12, 33)

        self.xImageOffset = -30
        self.yImageOffset = -30

        self.hp = 100

        self.weapon = ScatterGun(self.root, self.x, self.y)
        self.weapon.owner = self

        self.xRectOffset = self.x-self.rect.centerx
        self.yRectOffset = self.y-self.rect.centery

        Character.lateInit(self)
