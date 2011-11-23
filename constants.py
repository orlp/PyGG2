from __future__ import division, print_function

import math, pygame
from pygame.locals import *

import function

# this file contains all kinds of constants

GAME_WIDTH = 800
GAME_HEIGHT = 600

PHYSICS_TIMESTEP = 1/60 # always update physics in these steps
INPUT_SEND_FPS = 1/30 # we send input to the server at this rate
NETWORK_UPDATE_RATE = 1/30

# Networked Events
EVENT_HELLO = 0x0
EVENT_PLAYER_JOIN = 0x1
EVENT_PLAYER_LEAVE = 0x2
EVENT_FULL_UPDATE = 0x3
EVENT_SNAPSHOT_UPDATE = 0x4
EVENT_INPUTSTATE = 0x5
EVENT_LEFTMOUSEBUTTON_DOWN = 0x6
EVENT_RIGHTMOUSEBUTTON_DOWN = 0x7
EVENT_PLAYER_CHANGETEAM = 0x8
EVENT_PLAYER_CHANGECLASS = 0x9
EVENT_EXTENDED = 0xFF
