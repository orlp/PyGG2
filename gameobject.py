import pygame
from pygame.locals import *
from load_image import load_image
from collision import characterHitObstacle, objectCheckCollision

class GameObject(pygame.sprite.Sprite):

	def __init__(self, root, xpos, ypos):

		pygame.sprite.Sprite.__init__(self)

		self.root = root

		self.x = xpos
		self.y = ypos

		self.hspeed = 0
		self.vspeed = 0

		self.sprite = -1
		self.rect = -1

		self.xImageOffset = 0
		self.yImageOffset = 0

		self.root.GameObjectList.append(self)


	def BeginStep(self):

		pass


	def Step(self):

		pass


	def EndStep(self):

		if self.x < 0.0:
			self.x = 0.0

		if self.y < 0.0:
			self.y = 0.0

		self.x += self.hspeed
		self.y += self.vspeed
		if self.rect != -1:
			self.rect.topleft = (self.x, self.y)


	def Collide(self):
		pass

	def Draw(self):

		if self.sprite != -1:
			self.root.Surface.blit(self.sprite, ((self.x+self.xImageOffset)-self.root.Xview, (self.rect.top+self.yImageOffset)-self.root.Yview))
			
class MapObject(GameObject):

	def __init__(self, root):

		GameObject.__init__(self, root, 0, 0)

		self.sprite = pygame.image.load("Maps/MapTesting.png")
		pygame.transform.scale(self.sprite, (self.sprite.get_width()*6, self.sprite.get_height()*6))
		self.rect = pygame.Rect(0, 0, self.sprite.get_width(), self.sprite.get_height()) 


	def Draw(self):

		self.root.Surface.blit(pygame.transform.scale(self.sprite, (self.sprite.get_width()*6, self.sprite.get_height()*6)), (0-self.root.Xview, 0-self.root.Yview))


class Character(GameObject):

	def __init__(self, root):

		GameObject.__init__(self, root, 400, 400)

		self.sprite, self.rect = load_image('Sprites/Characters/Scout/Red/ScoutRedS_fr1.png')

		# The Scout hitbox: left = -6; right = 6; top = -10; bottom = 23
		self.rect = pygame.Rect(self.x-6, self.y-10, 12, 33)

		self.xImageOffset = -30
		self.yImageOffset = -30

		self.up, self.left, self.right, self.LMB, self.RMB = 0, 0, 0, 0, 0


	def Step(self):

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


	def EndStep(self):

		GameObject.EndStep(self)
		self.rect.topleft = (self.x-6, self.y-10)


	def Collide(self):

		check = objectCheckCollision(self, self.root.CollisionRectList)

		if check:
			characterHitObstacle(self, self.root.CollisionRectList)

class PlayerControl(GameObject):

	def __init__(self, root):

		GameObject.__init__(self, root, 0, 0)


	def BeginStep(self):

		up = 0
		left = 0
		right = 0
		LMB = 0
		RMB = 0

		for event in pygame.event.get():
			pass

		key = pygame.key.get_pressed()
		if key[K_w]:
			up = 1

		if key[K_a]:
			left = 1

		elif key[K_d]:
			right = 1

		LMB, middleMouseButton, RMB = pygame.mouse.get_pressed()

		# Send keybyte

		self.root.Myself.up = up
		self.root.Myself.left = left
		self.root.Myself.right = right
		self.root.Myself.LMB = LMB
		self.root.Myself.RMB = RMB
