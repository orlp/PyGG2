#!/usr/bin/env python

from __future__ import division

from gg2 import GG2
import pygame
from pygame.locals import *

import cProfile

# global settings
framerate = 60

# the main function
def GG2main():
    # initialize
    pygame.init()
    game = GG2()

    # game loop
    while True:        
        # check if user exited the game
        if QUIT in {event.type for event in pygame.event.get()}:
            break
        
        # update the game and render
        game.update(game.clock.get_time() / 1000)
        game.render()

        # wait to get steady frame rate
        game.clock.tick(framerate)
        
    # clean up
    pygame.quit()

cProfile.run("GG2main()")