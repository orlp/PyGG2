import pygame
from os.path import join

#define draw image
def load_image(name):
	image = pygame.image.load(name)
	image = image.convert()
	colorkey = image.get_at((0,0))
	image.set_colorkey(colorkey)
	return image, image.get_rect()
