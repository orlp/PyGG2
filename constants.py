from __future__ import division, print_function

import math, pygame
from pygame.locals import *

import function

# this file contains all kinds of constants

GAME_WIDTH = 800
GAME_HEIGHT = 600

PHYSICS_TIMESTEP = 1/50 # always update physics in these steps
INPUT_SEND_FPS = 1/30 # we send input to the server at this rate
NETWORK_UPDATE_RATE = 1/20

# Networked Events
EVENT_HELLO = 0
EVENT_PLAYER_JOIN = 1
EVENT_PLAYER_LEAVE = 2
EVENT_FULL_UPDATE = 3
EVENT_SNAPSHOT_UPDATE = 4
EVENT_INPUTSTATE = 5
EVENT_LEFTMOUSEBUTTON_DOWN = 6
EVENT_RIGHTMOUSEBUTTON_DOWN = 7
EVENT_PLAYER_CHANGETEAM = 8
EVENT_PLAYER_CHANGECLASS = 9
