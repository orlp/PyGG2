import os
import glob

import pygame
from load_image import load_image

from pygame.locals import *

# This is used later to check all the surrounding pixels of one.
global edgeList
edgeList = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]

global rectList
rectList = []

path = 'Maps/'

for infile in glob.glob( os.path.join(path, '*_wm.png') ):

	surface = pygame.image.load(infile)

	for x in range(0, surface.get_width()):

		for y in range(0, surface.get_height()):

			# Check if pixel is black or not.

			pixelColor = tuple(surface.get_at((x, y)))

			if pixelColor[0] == 0 and pixelColor[1] == 0 and pixelColor[2] == 0:

				# Light optimization: Check if the surrounding pixels are black too.

				surrounded = True
				if not (x > 1 and x < surface.get_width()-1 and y > 1 and y < surface.get_height()-1):# Don't do it for the edges
					surrounded = False
				else:
					for a in range(len(edgeList)):

						color = tuple(surface.get_at((x+(edgeList[a])[0], y+(edgeList[a])[1])))

						if color[0] != 0 or color[1] != 0 or color[2] != 0:

							surrounded = False
							break


				if not surrounded:

					newRect = [x, y]
					rectList.append(newRect)


	text = open((infile.split('.'))[0], 'w')

	for a in range(len(rectList)):

		newRect = rectList[a]

		writeString = str(newRect[0])+";"+str(newRect[1])+"\n"

		text.write(writeString)
