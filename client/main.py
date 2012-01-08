#!/usr/bin/env python

from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import pygame
from pygame.locals import *

# fix for py2exe dependency detection
try: import pygame._view
except: pass

import precision_timer
import engine.game
import engine.player
import rendering
import constants
import function

# DEBUG ONLY
import cProfile
import pstats
import os

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

    # toggle fullscreen flag
    flags ^= FULLSCREEN

    # restore settings, this time with fullscreen toggled.
    screen = pygame.display.set_mode((w, h), flags, bits)
    screen.blit(tmp, (0, 0))
    pygame.display.set_caption(*caption)
    pygame.mouse.set_cursor(*cursor)

    pygame.key.set_mods(0) # HACK: work-a-round for a SDL bug??

    return screen

# the main client class
class Client(object):
    def __init__(self):
        # initialize pygame
        pygame.init()

        # set display mode
        self.fullscreen = False # are we fullscreen? pygame doesn't track this
        self.window = pygame.display.set_mode((800, 600), (self.fullscreen * FULLSCREEN) | DOUBLEBUF)

        # keep state of keys stored for one frame so we can detect down/up events
        self.keys = pygame.key.get_pressed()
        self.oldkeys = self.keys

        # create game engine object
        self.game = engine.game.Game()

        # TODO REMOVE THIS
        # create player
        self.our_player = engine.player.Player(self.game, self.game.current_state, 0)

        # create renderer object
        self.renderer = rendering.GameRenderer(self)

        # pygame time tracking
        self.clock = precision_timer.Clock()
        self.inputsender_accumulator = 0.0 # this counter will accumulate time to send input at a constant rate
        # DEBUG code: show fps
        self.fps_font = pygame.font.Font(None, 17)
        self.fps_text = self.fps_font.render("%d FPS" % self.clock.getfps(), True, (255, 255, 255), (159, 182, 205))

    def run(self):
        # game loop
        while True:
            # check if user exited the game
            if QUIT in {event.type for event in pygame.event.get()}:
                break
            pygame.event.clear()

            # handle input
            self.oldkeys = self.keys
            self.keys = pygame.key.get_pressed()
            leftmouse, middlemouse, rightmouse = pygame.mouse.get_pressed()

            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.our_player.up = self.keys[K_w]
            self.our_player.down = self.keys[K_s]
            self.our_player.left = self.keys[K_a]
            self.our_player.right = self.keys[K_d]
            self.our_player.leftmouse = leftmouse
            self.our_player.middlemouse = middlemouse
            self.our_player.rightmouse = rightmouse
            self.our_player.aimdirection = function.point_direction(constants.GAME_WIDTH / 2, constants.GAME_HEIGHT / 2, mouse_x, mouse_y)

            if self.keys[K_l] and self.our_player.character_id != None:
                # Kill ourself. FIXME: Remove
                self.game.current_state.entities[self.our_player.character_id].die(self.game, self.game.current_state)

            # DEBUG quit game with escape
            if self.keys[K_ESCAPE]: break

            # did we just release the F11 button? if yes, go fullscreen
            if self.oldkeys[K_F11] and not self.keys[K_F11]:
                self.fullscreen = not self.fullscreen
                if not pygame.display.toggle_fullscreen():
                    self.window = toggle_fullscreen()

            # update the game and render
            frame_time = self.clock.tick()
            frame_time = min(0.25, frame_time) # a limit of 0.25 seconds to prevent complete breakdown

            self.game.update(frame_time)
            self.renderer.render(self, self.game, frame_time)

            self.fps_text = self.fps_font.render("%d FPS" % self.clock.getfps(), True, (255, 255, 255), (159, 182, 205))
            self.window.blit(self.fps_text, (0, 0))

            pygame.display.update()

        self.quit()

    def quit(self):
        # clean up
        pygame.quit()

def profileGG2():
    cProfile.run("client.main.GG2main()", "game_profile")
    p = pstats.Stats("game_profile", stream=open("profile.txt", "w"))
    p.sort_stats("cumulative")
    p.print_stats(30)
    os.remove("game_profile")

def GG2main():
    Client().run()

if __name__ == "__main__":
    # when profiling:
    profileGG2()
    # GG2main()
