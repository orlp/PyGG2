from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import function, constants
from networking import event_serialize

def Client_Event_Changeclass(networker, game, senderplayer, event):
    player = game.current_state.players[senderplayer.id]
    # TODO: If any, add classlimits here
    newclass = function.convert_class(event.newclass)
    if player.nextclass == newclass:
        return
    player.nextclass = newclass

    classchange_event = event_serialize.ServerEventChangeclass(senderplayer.id, event.newclass)
    networker.sendbuffer.append(classchange_event)

    # Kill the character
    try:
        character = game.current_state.entities[player.character_id]
        character.die(game, game.current_state)
        death_event = event_serialize.ServerEventDie(player.id)
        networker.sendbuffer.append(death_event)
    except KeyError:
        # Character is already dead, we don't need to do anything here
        pass

    # Resurrect him with new class. FIXME: REMOVE THIS
    player.spawn(game, game.current_state)
    spawn_event = event_serialize.ServerEventSpawn(player.id, 2300, 50)
    networker.sendbuffer.append(spawn_event)

def Client_Event_Jump(networker, game, senderplayer, event):
    player = game.current_state.players[senderplayer.id]
    # TODO: Add lag compensation, if any, here.
    player.up = True

def Client_Inputstate(networker, game, senderplayer, event):
    player = game.current_state.players[senderplayer.id]
    player.deserialize_input(event.bytestr)

def Client_Event_Disconnect(networker, game, senderplayer, event):
    player = game.current_state.players[senderplayer.id]
    print(player.name +" has disconnected")
    senderplayer.destroy(networker, game)

# Gather the functions together to easily be called by the event ID
eventhandlers = {}
eventhandlers[constants.EVENT_PLAYER_CHANGECLASS] = Client_Event_Changeclass
eventhandlers[constants.EVENT_JUMP] = Client_Event_Jump
eventhandlers[constants.INPUTSTATE] = Client_Inputstate
eventhandlers[constants.EVENT_PLAYER_DISCONNECT] = Client_Event_Disconnect
