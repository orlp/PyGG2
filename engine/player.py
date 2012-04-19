from __future__ import division, print_function

import character
import struct
from networking import event_serialize

class Player(object):
    def __init__(self, game, state, id):
        self.id = id
        state.players[id] = self

        self.up = False
        self.old_up = False
        self.down = False
        self.left = False
        self.right = False
        self.last_right = False
        self.last_left = False
        self.leftmouse = False
        self.middlemouse = False
        self.rightmouse = False
        self.aimdirection = 0
        
        self.nextclass = character.Scout
        self.character_id = None
        self.respawntimer = 0
        self.name = "Test name"

        self.issynced = True

    def step(self, game, state, frametime):
        # Only do this on the server
        if game.isserver:
            if self.character_id == None:# If the character is dead
                if self.respawntimer <= 0:
                    # Respawn
                    self.spawn(game, state)
                    # Send it to everyone
                    spawn_event = event_serialize.ServerEventSpawn(self.id, 2300, 50)
                    game.sendbuffer.append(spawn_event)
                else:
                    self.respawntimer -= frametime

    def spawn(self, game, state):
        if self.character_id != None:
            # There is already a character on the field. This should never happen.
            print("Tryed to spawn character while old one was still alive.")

        self.character_id = self.nextclass(game, state, self.id).id
        char = state.entities[self.character_id]
        char.just_spawned = True
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
        keybyte, aim = struct.unpack_from(">BH", bytestr)

        self.left = (keybyte & (1 << 0) > 0)
        self.right = (keybyte & (1 << 1) > 0)
        self.up = (keybyte & (1 << 2) > 0)
        self.leftmouse = (keybyte & (1 << 3) > 0)
        self.rightmouse = (keybyte & (1 << 4) > 0)

        self.aimdirection = aim * 360 / 65535

        return 3 # length of >BH
