import math, pygame

def sign(x):
    # Returns the sign of the number given
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def place_free((x, y), wallmask):
    return wallmask.get_at((x, y))


def point_direction(x1, y1, x2, y2):
    angle = -math.degrees(math.atan2(y2-y1, x2-x1))
    if angle < 0: angle += 360
    return angle

# easy loading an image
def load_image(name):
	image = pygame.image.load(name)
	image = image.convert()
	colorkey = image.get_at((0,0))
	image.set_colorkey(colorkey)
	return image, image.get_rect()
