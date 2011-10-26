#!/usr/bin/env python

from __future__ import division

from gg2 import GG2
import pygame
from pygame.locals import *

# fix for py2exe dependency detection
try: import pygame._view 
except: pass

# DEBUG ONLY
import cProfile

# global settings
framerate = 80

# the main function
def GG2main():
    # initialize
    pygame.init()
    
    # create game object
    game = GG2()
    
    physics_timestep = 1/25 # always update physics in steps of 1/25th second
    current_time = pygame.time.get_ticks() / 1000
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
        new_time = pygame.time.get_ticks() / 1000
        frame_time = min(0.25, new_time - current_time) # a limit of 0.25 seconds to prevent complete breakdown
        current_time = new_time
        
        accumulator += frame_time
        while accumulator > physics_timestep:
            accumulator -= physics_timestep
            game.update(frame_time)
        
        game.render()
        
    # clean up
    pygame.quit()

# when profiling:
cProfile.run("GG2main()")
# GG2main()