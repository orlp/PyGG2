from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import constants, event

eventhandlers = {}
# No need for classes here, functions can do the job, since execution is instant and only now.
eventhandlers[constants.PLAYER_CHANGECLASS] = Client_Event_Changeclass

def Client_Event_Changeclass(self, networker, game, senderplayer, event):
    player = game.current_state.entities[senderplayer.id]
    # TODO: If any, add classlimits here
    player.nextclass = event.newclass
    classchange_event = event.Server_Event_Changeclass(senderplayer.id, player.nextclass)
    networker.sendbuffer.append(classchange_event)

def Client_Inputstate(self, networker, game, senderplayer, event):
    player = game.current_state.entities[senderplayer.id]
    player.deserialize_input(event.bytestr)
