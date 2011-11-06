#!/usr/bin/env python

from __future__ import division, print_function

import math, pygame
from pygame.locals import *
try: import pygame._view # fix for py2exe dependency detection
except: pass

# DEBUG ONLY
import cProfile
import pstats

import gg2

# global settings
physics_timestep = 1/60 # always update physics in these steps

# the main function
def GG2main():
    # initialize pygame
    pygame.init()
    
    # set display mode
    fullscreen = False # are we fullscreen? pygame doesn't track this
    pygame.display.set_mode((800, 600), (fullscreen * FULLSCREEN) | DOUBLEBUF)

    # keep state of keys stored for one frame so we can detect down/up events
    keys = pygame.key.get_pressed()
    
    # create game object
    game = gg2.GG2()
    
    # pygame time tracking
    clock = pygame.time.Clock()
    accumulator = 0.0 # this counter will accumulate time to be used by the physics
    
    # DEBUG code: calculate average fps
    average_fps = 0
    num_average_fps = 0
    
    # game loop
    while True:        
        # check if user exited the game
        if QUIT in {event.type for event in pygame.event.get()}:
            break
        
        # handle input
        oldkeys = keys
        keys = pygame.key.get_pressed()
        game.up = keys[K_w]
        game.left = keys[K_a]
        game.right = keys[K_d]
        
        # DEBUG quit game with escape
        if keys[K_ESCAPE]: break
        
        # did we just release the F11 button? if yes, go fullscreen
        if oldkeys[K_F11] and not keys[K_F11]:
            fullscreen = not fullscreen
            pygame.display.set_mode((800, 600), (fullscreen * FULLSCREEN) | DOUBLEBUF)

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
    cProfile.run("GG2main()", "game_profile")
    p = pstats.Stats("game_profile")
    p.sort_stats("cumulative")
    p.print_stats()
    
if __name__ == "__main__":
    # when profiling:
    # profileGG2()
    GG2main()