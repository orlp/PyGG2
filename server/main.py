#!/usr/bin/env python

from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import precision_timer
import engine.game
import constants

# DEBUG ONLY
import cProfile
import pstats
import os

# the main function
def GG2main():
    # create game engine object
    game = engine.game.Game()

    # pygame time tracking
    clock = precision_timer.Clock()
    physics_accumulator = 0.0 # this counter will accumulate time to be used by the physics
    networking_accumulator = 0.0 # this counter is used for sending networking packets at a constant rate

    # game loop
    while True:
        # update the game and render
        frametime = clock.tick()
        frametime = min(0.25, frametime) # a limit of 0.25 seconds to prevent complete breakdown

        game.update(frametime)

        networking_accumulator += frametime
        while networking_accumulator > constants.NETWORK_UPDATE_RATE:
            networking_accumulator -= constants.NETWORK_UPDATE_RATE
            #send_update()


def send_update():
    sendbuffer = str()
    for player in self.playerlist: sendbuffer+=player.serialize()

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
