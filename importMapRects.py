import pygame

def importMapRects():	

	rectList = []

	text = open('Maps/Test_wm', 'r')

	linesList = text.readlines()

	for a in range(len(linesList)):

		x = int(linesList[a].split(';')[0])*6
		y = int(linesList[a].split(';')[1])*6

		rectList.append(pygame.Rect(x, y, 6, 6))

	return rectList
