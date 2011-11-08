#!/usr/bin/env python

from __future__ import division, print_function

import pygame
from pygame.locals import *

# fix for py2exe dependency detection
try: import pygame._view
except: pass

# DEBUG ONLY
import cProfile
import pstats
import os

import gg2
import constants

# http://pygame.org/wiki/toggle_fullscreen
def toggle_fullscreen():
    # save data before restarting the screen
    screen = pygame.display.get_surface()
    tmp = screen.convert()
    caption = pygame.display.get_caption()
    cursor = pygame.mouse.get_cursor()
    w, h = screen.get_width(), screen.get_height()
    flags = screen.get_flags()
    bits = screen.get_bitsize()
    
    # restart the screen
    pygame.display.quit()
    pygame.display.init()
    
    # toggle fullscreen flag and get the new state
    flags ^= FULLSCREEN
    fullscreen = flags & FULLSCREEN
    
    # restore settings, this time with fullscreen toggled.
    screen = pygame.display.set_mode((w, h), flags, bits)
    screen.blit(tmp, (0, 0))
    pygame.display.set_caption(*caption)
    pygame.mouse.set_cursor(*cursor)
 
    pygame.key.set_mods(0) # HACK: work-a-round for a SDL bug??
 
    return screen, fullscreen

# the main function
def GG2main():
    # initialize pygame
    pygame.init()
    
    # set display mode
    fullscreen = False # are we fullscreen? pygame doesn't track this
    window = pygame.display.set_mode((800, 600), (fullscreen * FULLSCREEN) | DOUBLEBUF)

    # keep state of keys stored for one frame so we can detect down/up events
    keys = pygame.key.get_pressed()
    
    # create game object
    game = gg2.GG2()
    
    # pygame time tracking
    clock = pygame.time.Clock()
    accumulator = 0.0 # this counter will accumulate time to be used by the physics
    
    # DEBUG code: show fps    
    fps_font = pygame.font.Font(None, 17)
    fps_text = fps_font.render("%d FPS" % clock.get_fps(), True, (255, 255, 255), (159, 182, 205))
    
    # game loop
    while True:        
        # check if user exited the game
        if QUIT in {event.type for event in pygame.event.get()}:
            break
        
        # handle input
        oldkeys = keys
        keys = pygame.key.get_pressed()
        leftmouse, middlemouse, rightmouse = pygame.mouse.get_pressed()
        
        game.mouse_x, game.mouse_y = pygame.mouse.get_pos()
        game.up = keys[K_w]
        game.down = keys[K_s]
        game.left = keys[K_a]
        game.right = keys[K_d]
        game.leftmouse = leftmouse
        game.middlemouse = middlemouse
        game.rightmouse = rightmouse
        
        # DEBUG quit game with escape
        if keys[K_ESCAPE]: break
        
        # did we just release the F11 button? if yes, go fullscreen
        if oldkeys[K_F11] and not keys[K_F11]:
            fullscreen = not fullscreen
            if not pygame.display.toggle_fullscreen():
                game.window = toggle_fullscreen()

        # update the game and render
        frame_time = clock.tick() / 1000
        frame_time = min(0.25, frame_time) # a limit of 0.25 seconds to prevent complete breakdown
        
        accumulator += frame_time
        while accumulator > constants.PHYSICS_TIMESTEP:
            accumulator -= constants.PHYSICS_TIMESTEP
            game.update(constants.PHYSICS_TIMESTEP)
            fps_text = fps_font.render("%d FPS" % clock.get_fps(), True, (255, 255, 255), (159, 182, 205))
        
        game.render(accumulator / constants.PHYSICS_TIMESTEP, frame_time)
        
        game.window.blit(fps_text, (0, 0))
        
        pygame.display.flip()
    
    # clean up
    pygame.quit()

def profileGG2():
    cProfile.run("GG2main()", "game_profile")
    p = pstats.Stats("game_profile", stream=open("profile.txt", "w"))
    p.sort_stats("cumulative")
    p.print_stats(30)
    os.remove("game_profile")
    
if __name__ == "__main__":
    # when profiling:
    profileGG2()
    # GG2main()