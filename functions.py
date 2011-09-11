import math, pygame

def sign(x):

	if x > 0:
		return 1
	elif x < 0:
		return -1
	else:
		return 0


def lengthdir(x, y):

	x = x**2
	y = y**2

	return math.sqrt(x+y)


def place_free(x, y, wallmask):

	placeFree = True

	for index in range(len(wallmask)):

		if wallmask[index].collidepoint(x, y):
			placeFree = False
			break

	return placeFree
