import math, pygame

def sign(x):
    # Returns the sign of the number given
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

# nightcracker - DEPRECATED, this is math.hypot
# def lengthdir(x, y):

    # # Returns the length of a line described by the x and y components given

    # x = x**2
    # y = y**2

    # return math.sqrt(x+y)


def place_free((x, y), wallmask):
    return wallmask.get_at((x, y))


def point_direction(x1, y1, x2, y2):
    angle = -math.degrees(math.atan2(y2-y1, x2-x1))
    if angle < 0: angle += 360
    return angle