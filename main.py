#!/usr/bin/env python

from __future__ import division

import math, pygame
from pygame.locals import *
try: import pygame._view # fix for py2exe dependency detection
except: pass

# DEBUG ONLY
import cProfile

# initialize pygame - use HWSURFACE in the case it helps, and DOUBLEBUF to prevent screen tearing
pygame.init()
pygame.display.set_mode((800, 600), HWSURFACE | DOUBLEBUF)

# wait with importing of gg2 until the display is set
# this is because on loading of object classes sprites are loaded
# the sprites are .convert()'ed, and this requires the pygame display mode to be set
import gg2

# global settings
physics_timestep = 1/30 # always update physics in steps of 1/30th second

# the main function
def GG2main():
    # create game object
    game = gg2.GG2()
    
    # pygame time tracking
    clock = pygame.time.Clock()
    
    accumulator = 0.0 # this counter will accumulate time to be used by the physics
    
    # game loop
    while True:        
        # check if user exited the game
        if QUIT in {event.type for event in pygame.event.get()}:
            break
        
        # handle input
        key = pygame.key.get_pressed()
        game.up = key[K_w]
        game.left = key[K_a]
        game.right = key[K_d]

        leftmouse, middlemouse, rightmouse = pygame.mouse.get_pressed()
        game.leftmouse = leftmouse
        game.middlemouse = middlemouse
        game.rightmouse = rightmouse
        
        # update the game and render
        clock.tick()
        frame_time = min(0.25, clock.get_time() / 1000) # a limit of 0.25 seconds to prevent complete breakdown
        
        accumulator += frame_time
        while accumulator > physics_timestep:
            accumulator -= physics_timestep
            game.update(physics_timestep)
        
        game.render(accumulator / physics_timestep)
        
        # print(clock.get_fps())
        
    # clean up
    pygame.quit()

# when profiling:
# cProfile.run("GG2main()")
GG2main()