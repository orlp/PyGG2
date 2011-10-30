#!/usr/bin/env python

from __future__ import division

import math, pygame
from pygame.locals import *
try: import pygame._view # fix for py2exe dependency detection
except: pass

# DEBUG ONLY
import cProfile
import pstats

# initialize pygame - DOUBLEBUF to prevent screen tearing
pygame.init()
pygame.display.set_mode((800, 600), DOUBLEBUF)

# wait with importing of gg2 until the display is set
# this is because on loading of object classes sprites are loaded
# the sprites are .convert()'ed, and this requires the pygame display mode to be set
import gg2

# global settings
physics_timestep = 1/60 # always update physics in these steps

# the main function
def GG2main():
    # create game object
    game = gg2.GG2()
    
    # pygame time tracking
    clock = pygame.time.Clock()
    
    # DEBUG code: calculate average fps
    average_fps = 0
    num_average_fps = 0
    
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
        
        # DEBUG quit game with escape
        if key[K_ESCAPE]: break

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
        
        # debug code
        fps = clock.get_fps()
        average_fps = (average_fps * num_average_fps + fps) / (num_average_fps + 1)
        num_average_fps += 1
        
        game.render(accumulator / physics_timestep)
    
    print(average_fps)
    
    # clean up
    pygame.quit()

def profileGG2():
    cProfile.run("GG2main()", "game_profi.txt")
    p = pstats.Stats("game_profi.txt")
    p.sort_stats("cumulative")
    p.print_stats()
    
# when profiling:
# profileGG2()
GG2main()