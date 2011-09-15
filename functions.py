import math, pygame

def sign(x):

    # Returns the sign of the number given
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def lengthdir(x, y):

    # Returns the length of a line described by the x and y components given

    x = x**2
    y = y**2

    return math.sqrt(x+y)


def place_free((x, y), wallmask):

    return wallmask.get_at(x, y)


def point_direction(x1, y1, x2, y2):

    # Returns the angle from point 1 to point 2.

    xDiff = x2-x1
    yDiff = y1-y2

    length = lengthdir(xDiff, yDiff)

    if length == 0:
        return 0

    # --> 'Unit Circle'. Normalizing stuff here to create one.
    x = xDiff/length
    y = yDiff/length

    # In a unit circle, the y coor. of any point on the circle is == to sin(alpha).
    sinAngle1 = math.asin(y)

    # There are always two possible angles for one sinus.
    if sign(sinAngle1) == 1:

        sinAngle2 = math.pi-sinAngle1

    else:

        sinAngle2 = math.pi-sinAngle1
        sinAngle1 = (2*math.pi)+sinAngle1

    # sinAngle1 will always have a positive cos, and sinAngle2 will always have a negative one.

    # Since cos(alpha) == x;
    if sign(x) == -1:
        answer = sinAngle2
    else:
        # I don't really care what happens if x == 0
        answer = sinAngle1


    answer *= 360/(2*math.pi)# Convert it to degrees because math.a* uses radians.

#    print answer

    return answer
