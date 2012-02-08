from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import function, constants
from networking import event_serialize

def Client_Event_Changeclass(networker, game, senderplayer, event):
    player = game.current_state.entities[senderplayer.id]
    # TODO: If any, add classlimits here
    player.nextclass = function.convert_class(event.newclass)
    classchange_event = event_serialize.Server_Event_Changeclass(0, senderplayer.id, event.newclass)
    networker.sendbuffer.append(classchange_event)

def Client_Event_Jump(networker, game, senderplayer, event):
    player = game.current_state.entities[senderplayer.id]
    # TODO: Add lag compensation, if any, here.
    player.up = True

def Client_Inputstate(networker, game, senderplayer, event):
    player = game.current_state.entities[senderplayer.id]
    player.deserialize_input(event.bytestr)

def Client_Event_Hello(networker, game, senderplayer, event):
    # Bogus handler, exists to catch packets from the client after connection.
    # FIXME: Remove and replace with better and more stable system.
    pass


# Gather the functions together to easily be called by the event ID
eventhandlers = {}
eventhandlers[constants.EVENT_PLAYER_CHANGECLASS] = Client_Event_Changeclass
eventhandlers[constants.EVENT_JUMP] = Client_Event_Jump
eventhandlers[constants.INPUTSTATE] = Client_Inputstate
eventhandlers[constants.EVENT_HELLO] = Client_Event_Hello
