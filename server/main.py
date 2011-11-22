#!/usr/bin/env python

from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import precision_timer
import engine.game
import engine.player
import constants

# DEBUG ONLY
import cProfile
import pstats
import os

# the main function
class Server(object):
    def __init__(self):
        # create game engine object
        self.game = engine.game.Game()

        # TODO REMOVE THIS
        # create player
        self.engine.player.Player(game, game.current_state, 0)

        # pygame time tracking
        self.clock = precision_timer.Clock()
        self.networking_accumulator = 0.0 # this counter is used for sending networking packets at a constant rate

    def run(self):
        # game loop
        while True:
            # update the game and render
            frametime = self.clock.tick()
            frametime = min(0.25, frametime) # a limit of 0.25 seconds to prevent complete breakdown

            self.game.update(frametime)

            self.networking_accumulator += frametime
            while self.networking_accumulator > constants.NETWORK_UPDATE_RATE:
                self.networking_accumulator -= constants.NETWORK_UPDATE_RATE

def profileGG2():
    cProfile.run("Server().run()", "game_profile")
    p = pstats.Stats("game_profile", stream=open("profile.txt", "w"))
    p.sort_stats("cumulative")
    p.print_stats(30)
    os.remove("game_profile")

def GG2main():
    Server().run()

if __name__ == "__main__":
    # when profiling:
    profileGG2()
    # GG2main()
