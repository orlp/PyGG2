import pygame, math, random
from pygame.locals import *
from gameobject import GameObject
from functions import sign, place_free, point_direction, load_image
from shot import Shot

class Weapon(GameObject):
    def __init__(self, root, x, y):
        GameObject.__init__(self, root, x, y)

        self.owner = None
        self.firingSprite = None

        self.ammo = 0
        self.maxAmmo = 0
        self.justShot = False
        self.readyToShoot = True
        self.refireAlarm = 0

        self.direction = 0

    def step(self, frametime):
        if self.refireAlarm <= 0:
            self.refireAlarm = 0
            self.readyToShoot = True
        else:
            self.refireAlarm -= 1 * (frametime / 1000.0)

        if self.owner.LMB and self.refireAlarm == 0:
            self.FirePrimary()

        if self.owner.RMB and self.refireAlarm == 0:
            self.FireSecondary()


    def endStep(self, frametime):
        self.rect.topleft = (self.x - self.xRectOffset, self.y - self.yRectOffset)


    def posUpdate(self):
        self.x = self.owner.x
        self.y = self.owner.y
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.direction = point_direction(self.x, self.y, mouse_x + self.root.Xview, mouse_y + self.root.Yview)

    def FirePrimary(self):
        pass

    def FireSecondary(self):
        pass


    def draw(self):
        if not self.sprite: return

        tempSprite = self.sprite.copy()

        if self.justShot:
            self.sprite = self.firingSprite.copy()

        if self.owner.flip:
            self.sprite = pygame.transform.flip(self.sprite, 0, 1)

        self.sprite = pygame.transform.rotate(self.sprite, self.direction)
        
        
        GameObject.draw(self)
        self.sprite = tempSprite



class ScatterGun(Weapon):
    def __init__(self, root, x, y):
        Weapon.__init__(self, root, x, y)

        self.sprite, self.rect = load_image("Sprites/Weapons/Scattergun/ScatterGunS.png")
        self.firingSprite, unusedRect = load_image("Sprites/Weapons/Scattergun/ScatterGunS-firing.png")

        self.maxAmmo = 6
        self.ammo = self.maxAmmo

        self.refireTime = 20
        self.reloadTime = 15

        self.xImageOffset = -6
        self.yImageOffset = -6

    def FirePrimary(self):
        for i in range(6):
            shot = Shot(self.root, self.x, self.y)
            shot.owner = self.owner
            shot.direction = self.direction + (7 - random.randint(0, 15))

            shot.speed = 10 + (2 - random.randint(0, 4))

            radDirection = math.radians(shot.direction)
            shot.hspeed = math.cos(radDirection) * shot.speed + self.owner.hspeed/2
            shot.vspeed = math.sin(radDirection) * -shot.speed

            shot.speed = math.hypot(shot.hspeed, shot.vspeed)
            self.refireAlarm = self.refireTime
