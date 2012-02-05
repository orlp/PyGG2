from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import function, constants
from networking import event_serialize


def Server_Event_Changeclass(networker, game, event):
    player = game.current_state.players[event.playerid]
    player.nextclass = event.newclass

def Server_Event_Die(networker, game, event):
    player = game.current_state.players[event.playerid]
    character = game.current_state.enities[player.character_id]
    character.die(game, game.current_state)

def Server_Event_Spawn(network, game, event):
    player = game.current_state.players[event.playerid]
    player.spawn(game, state)

def Server_Snapshot_Update(networker, game, event):
    state = game.current_state
    for playerid, player in state.players:
        player.deserialize_input(event.bytestr)

        character = state.entities[player.character_id]
        character.deserialize(state)

def Server_Full_Update(networker, game, event):
    numof_players = struct.unpack_from(">B", event.bytestr)
    event.bytestr = event.bytestr[1:]

    for index in range(numof_players):
        player = engine.player.Player(game, game.current_state, index)

        player.name, player_class = struct.unpack_from(">32pB", event.bytestr)
        player.nextclass = function.convert_class(player_class)
        event.bytestr = event.bytestr[33:]

    Server_Snapshot_Update(networker, game, event)


# Gather the functions together to easily be called by the event ID
eventhandlers = {}
eventhandlers[constants.EVENT_PLAYER_CHANGECLASS] = Server_Event_Changeclass
eventhandlers[constants.SNAPSHOT_UPDATE] = Server_Snapshot_Update
eventhandlers[constants.FULL_UPDATE] = Server_Full_Update
