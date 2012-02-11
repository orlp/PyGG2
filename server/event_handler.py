from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import function, constants
from networking import event_serialize

def Client_Event_Changeclass(networker, game, senderplayer, event):
    player = game.current_state.players[senderplayer.id]
    # TODO: If any, add classlimits here
    player.nextclass = function.convert_class(event.newclass)
    classchange_event = event_serialize.Server_Event_Changeclass(senderplayer.id, event.newclass)
    networker.sendbuffer.append(classchange_event)

def Client_Event_Jump(networker, game, senderplayer, event):
    player = game.current_state.players[senderplayer.id]
    # TODO: Add lag compensation, if any, here.
    player.up = True

def Client_Inputstate(networker, game, senderplayer, event):
    player = game.current_state.players[senderplayer.id]
    player.deserialize_input(event.bytestr)


# Gather the functions together to easily be called by the event ID
eventhandlers = {}
eventhandlers[constants.EVENT_PLAYER_CHANGECLASS] = Client_Event_Changeclass
eventhandlers[constants.EVENT_JUMP] = Client_Event_Jump
eventhandlers[constants.INPUTSTATE] = Client_Inputstate
