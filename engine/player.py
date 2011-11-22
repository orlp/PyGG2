from __future__ import division, print_function

import character
import struct

class Player(object):
    def __init__(self, game, state):
        self.id = 0

        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.leftmouse = False
        self.middlemouse = False
        self.rightmouse = False
        self.aimdirection = 0

        self.character = character.Scout(game, state, self)
        self.character.x = 2300
        self.character.y = 50

    def serialize_input(self):
        keybyte = 0

        keybyte |= self.left << 0
        keybyte |= self.right << 1
        keybyte |= self.up << 2
        keybyte |= self.leftmouse << 3
        keybyte |= self.rightmouse << 4

        aim = int((self.aimdirection % 360) / 360 * 65535)

        bytestr = struct.pack("!BH", keybyte, aim)

        return bytestr

    def deserialize_input(self, bytestr):
        keybyte, aim = struct.unpack("!BH", bytestr)

        self.left = keybyte & (1 << 0)
        self.right = keybyte & (1 << 1)
        self.up = keybyte & (1 << 2)
        self.leftmouse = keybyte & (1 << 3)
        self.rightmouse = keybyte & (1 << 4)

        self.aimdirection = aim * 360 / 65535
