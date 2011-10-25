from __future__ import division

import math, pygame
from pygame.locals import *

def sign(x):
    # Returns the sign of the number given
    return cmp(x, 0)

def point_direction(x1, y1, x2, y2):
    angle = -math.degrees(math.atan2(y2 - y1, x2 - x1))
    if angle < 0: angle += 360
    return angle

def rotate_surface_point(surface, angle, px, py):
    width, height = surface.get_size()
    rotated_surface = pygame.transform.rotate(surface, angle)

    angle = math.radians(angle)
    
    xoff = (height - py) * math.sin(angle) + px * math.cos(angle)
    yoff = (width - px) * math.sin(angle) + py * math.cos(angle)
    
    return rotated_surface, xoff, yoff

# prevent double-loading, only load a filename once
images = {}
def load_image(filename):
    if filename in images:
        return images[filename].copy()
    
    image = pygame.image.load(filename).convert()
    image.set_colorkey((255, 0, 255), RLEACCEL)
    images[filename] = image
    
    return image
    
