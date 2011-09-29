from __future__ import division

import math, pygame
from pygame.locals import *

def sign(x):
    # Returns the sign of the number given
    return cmp(x, 0)

def place_free((x, y), wallmask):
    return wallmask.get_at((x, y))

def point_direction(x1, y1, x2, y2):
    angle = -math.degrees(math.atan2(y2 - y1, x2 - x1))
    if angle < 0: angle += 360
    return angle

def load_image(filename):
    image = pygame.image.load(filename).convert()
    image.set_colorkey((255, 0, 255), RLEACCEL)
    return image
    
