#!/usr/bin/env python

from __future__ import division

from gg2 import GG2
import pygame
from pygame.locals import *

# global settings
framerate = 60

# main game initialize
pygame.init()
game = GG2()
clock = pygame.time.Clock()

# game loop
while True:
    print(clock.get_fps())
    
    # check if user exited the game
    if QUIT in {event.type for event in pygame.event.get()}:
        break
    
    # update the game and render
    game.update(clock.get_time())
    game.render()

    # wait to get steady frame rate
    clock.tick(framerate)

# clean up
pygame.quit()