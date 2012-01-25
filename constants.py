from __future__ import division, print_function\

import function

# this file contains all kinds of constants

GAME_WIDTH = 800
GAME_HEIGHT = 600

PHYSICS_TIMESTEP = 1/60 # always update physics in these steps

GAME_VERSION_STRING = "py-2.5"
GAME_URL = "http://www.ganggarrison.com/forums/index.php?topic=29530.0"

# Networking
INPUT_SEND_FPS = 1/30 # we send input to the server at this rate
MAX_PACKET_SIZE = 2048

# Lobby
LOBBY_HOST = "ganggarrison.com"
LOBBY_PORT = 29944

# UUIDs
LOBBY_MESSAGE_TYPE_UUID = "b5dae2e8-424f-9ed0-0fcb-8c21c7ca1352"
GG2_LOBBY_UUID = "1ccf16b1-436d-856f-504d-cc1af306aaa7"
PYGG2_COMPATIBILITY_PROTOCOL = "e8b036bf-409d-a71b-2702-c7e443b1fdbe"

# Networked Events
EVENT_HELLO = 0
EVENT_PLAYER_JOIN = 1
EVENT_PLAYER_LEAVE = 2
FULL_UPDATE = 3
SNAPSHOT_UPDATE = 4
INPUTSTATE = 5
EVENT_LEFTMOUSEBUTTON_DOWN = 6
EVENT_RIGHTMOUSEBUTTON_DOWN = 7
EVENT_PLAYER_CHANGETEAM = 8
EVENT_PLAYER_CHANGECLASS = 9
EVENT_JUMP = 10

# Class Constants - To use only in networking
CLASS_SCOUT = 0
CLASS_PYRO = 1
CLASS_SOLDIER = 2
CLASS_HEAVY = 3
CLASS_DEMOMAN = 4
CLASS_MEDIC = 5
CLASS_ENGINEER = 6
CLASS_SPY = 7
CLASS_SNIPER = 8
CLASS_QUOTE = 9
