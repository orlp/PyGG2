#!/usr/bin/env python

from __future__ import division, print_function

# add our main folder as include dir
import sys, uuid
sys.path.append("../")

import precision_timer
import engine.game
import constants
import networker
import lobby
import json

# DEBUG ONLY
import cProfile
import pstats
import os

# the main function
class Server(object):
    def __init__(self):
        self.load_config()

        self.port = self.config.setdefault('port', 8190)
        self.name = str(self.config.setdefault('name', 'Development Server'))
        self.password = str(self.config.setdefault('password', ''))
        self.ID = uuid.uuid4()

        # create game engine object
        self.game = engine.game.Game()
        self.game.servername = self.name
        self.game.isserver = True

        # create packet handler
        self.networker = networker.Networker(self.port)

        # create lobby announcer
        self.lobbyannouncer = lobby.Lobby()

        # time tracking
        self.clock = precision_timer.Clock()

        print("Hosting " + str(self.name) + " on port " + str(self.port) + " with password " + "\"" + str(self.password) + "\"")

        self.save_config()

    def run(self):
        # game loop
        while True:
            try:
                # update the game and render
                frametime = self.clock.tick()
                frametime = min(0.25, frametime) # a limit of 0.25 seconds to prevent complete breakdown

                self.networker.recieve(self, self.game)
                self.game.update(self.networker, frametime)
                self.networker.update(self, self.game, frametime)
                self.lobbyannouncer.update(self, frametime)

            except KeyboardInterrupt:
                self.destroy()
                sys.exit()

    def load_config(self):
        if os.path.exists('server_cfg.json'):
            with open('server_cfg.json', 'r') as fp:
                self.config = json.load(fp)
        else:
            self.config = {}

    def save_config(self):
        with open('server_cfg.json', 'w') as fp:
            json.dump(self.config, fp, indent=4)


    def destroy(self):
        self.lobbyannouncer.destroy(self)


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
