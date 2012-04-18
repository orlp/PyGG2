#!/usr/bin/env python

from client.handler import ClientManager
from client.main import GameClientHandler
from client.menus import MainMenuHandler

import pygrafix

# DEBUG ONLY
import cProfile
import pstats
import os

# add resource locations
if os.path.isdir("sprites"):
    pygrafix.resource.add_location("sprites")
if os.path.isfile("sprites.zip"):
    pygrafix.resource.add_location("sprites.zip")

def profileGG2():
    cProfile.run("GG2main()", sort="time")

def GG2main(skipmenu=False):
    if skipmenu:
        cm = ClientManager(GameClientHandler)
    else:
        cm = ClientManager(MainMenuHandler)
    cm.run()

if __name__ == "__main__":
    # when profiling:
    profileGG2()
    # GG2main()
