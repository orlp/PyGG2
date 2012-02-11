from __future__ import division, print_function

import character
import struct

class Player(object):
    def __init__(self, game, state, id):
        self.id = id
        state.players[id] = self

        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.leftmouse = False
        self.middlemouse = False
        self.rightmouse = False
        self.aimdirection = 0

        self.nextclass = character.Pyro
        self.character_id = None
        self.spawn(game, state)# FIXME: Remove this
        self.respawntimer = 0
        self.name = "Test name"

    # FIXME: Make this actually get executed
    def step(self, game, state, frametime):
        # FIXME: Make this dependent on server input, and not executed on the client.
        if self.character_id == None:# If the character is dead
            if self.respawntimer <= 0:
                self.spawn(self, game, state)# Respawn
            else:
                self.respawntimer -= frametime

    def spawn(self, game, state):
        if self.character_id != None:
            # There is already a character on the field. This should never happen.
            print("Tryed to spawn character while old one was still alive.")

        self.character_id = self.nextclass(game, state, self.id).id
        char = state.entities[self.character_id]
        # FIXME remove
        char.x = 2300
        char.y = 50

    def copy(self):
        new = Player.__new__(Player) # create class without invoking __init__
        new.__dict__.update(self.__dict__)
        return new

    def destroy(self, game, state):
        try:
            character = state.entities[self.character_id]
            character.die(game, state)
        except KeyError:
            # Character is already dead
            pass
        del state.players[self.id]

    def serialize_input(self):
        keybyte = 0

        keybyte |= self.left << 0
        keybyte |= self.right << 1
        keybyte |= self.up << 2
        keybyte |= self.leftmouse << 3
        keybyte |= self.rightmouse << 4

        aim = int((self.aimdirection % 360) / 360 * 65535)

        bytestr = struct.pack(">BH", keybyte, aim)
        return bytestr

    def deserialize_input(self, bytestr):
        keybyte, aim = struct.unpack(">BH", bytestr)

        self.left = keybyte & (1 << 0)
        self.right = keybyte & (1 << 1)
        self.up = keybyte & (1 << 2)
        self.leftmouse = keybyte & (1 << 3)
        self.rightmouse = keybyte & (1 << 4)

        self.aimdirection = aim * 360 / 65535
