from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import struct
import engine.map
import engine.player
import function, constants
from networking import event_serialize


def Server_Event_Hello(client, networker, game, event):
    # Stop saying hello
    networker.has_connected = True
    # TODO: Some version check using event.version and constants.GAME_VERSION_NUMBER
    # Set all the important values to the game
    game.servername = event.servername
    player_id = event.playerid
    game.maxplayers = event.maxplayers
    game.map = engine.map.Map(game, event.mapname)
    client.start_game(player_id)

def Server_Event_Player_Join(client, networker, game, event):
    newplayer = engine.player.Player(game, game.current_state, event.id)
    newplayer.name = event.name

def Server_Event_Changeclass(client, networker, game, event):
    player = game.current_state.players[event.playerid]
    player.nextclass = function.convert_class(event.newclass)

def Server_Event_Die(client, networker, game, event):
    player = game.current_state.players[event.playerid]
    character = game.current_state.entities[player.character_id]
    character.die(game, game.current_state)

def Server_Event_Spawn(client, networker, game, event):
    player = game.current_state.players[event.playerid]
    player.spawn(game, game.current_state)

def Server_Snapshot_Update(client, networker, game, event):
    # Copy the current game state, and replace it with everything the server knows
    time = struct.unpack_from(">I", event.bytestr)[0]
    event.bytestr= event.bytestr[4:]

    if len(game.old_states) > 0:
        keys = game.old_states.keys()
        if max(keys) > time:
            if time in keys:
                state = game.old_states[time]
            else:
                times = keys
                keys.sort()
                times.sort(lambda a, b: (abs(a-time) < abs(b-time)))
                key1 = times[0]
                key2 = keys[keys.index(key1) + (key1<time)]

                if key1 == key2:
                    state = game.old_states[key1]
                else:
                    state_1 = game.old_states[key1]
                    state_2 = game.old_states[key2]
                    state = state_1.copy()
                    state.interpolate(state_1, state_2, (time-key1)/(key2-key1))

        else:
            state = game.current_state

        # Delete all the old states, they are useless
        keys = game.old_states.keys()
        while len(game.old_states) > 0:
            if keys[0] < time:
                del game.old_states[keys[0]]
                del keys[0]
            else:
                break

    else:
        state = game.current_state

    for player in state.players.values():
        length = player.deserialize_input(event.bytestr)
        event.bytestr = event.bytestr[length:]

        try:
            character = state.entities[player.character_id]
            length = character.deserialize(state, event.bytestr)
            event.bytestr = event.bytestr[length:]
        except KeyError:
            # Character is dead
            pass
    if game.lag_comp:
        # Update this state with all the input information that appeared in the meantime
        for time, old_state in game.old_states.items():
            state.update_all_objects(game, state, constants.PHYSICS_TIMESTEP)

def Server_Full_Update(client, networker, game, event):
    game.current_state.time, numof_players = struct.unpack_from(">IB", event.bytestr)
    event.bytestr = event.bytestr[5:]

    for index in range(numof_players):
        player = engine.player.Player(game, game.current_state, index)

        player.name, player_class, character_exists = struct.unpack_from(">32pBB", event.bytestr)
        player.nextclass = function.convert_class(player_class)
        event.bytestr = event.bytestr[34:]

        if character_exists:
            player.spawn(game, game.current_state)

def Server_Event_Disconnect(client, networker, game, event):
    player = game.current_state.players[event.playerid]
    print (player.name +" has disconnected")
    player.destroy(game, game.current_state)

# Gather the functions together to easily be called by the event ID
eventhandlers = {}
eventhandlers[constants.EVENT_HELLO] = Server_Event_Hello
eventhandlers[constants.EVENT_PLAYER_JOIN] = Server_Event_Player_Join
eventhandlers[constants.EVENT_PLAYER_CHANGECLASS] = Server_Event_Changeclass
eventhandlers[constants.EVENT_PLAYER_DIE] = Server_Event_Die
eventhandlers[constants.EVENT_PLAYER_SPAWN] = Server_Event_Spawn
eventhandlers[constants.SNAPSHOT_UPDATE] = Server_Snapshot_Update
eventhandlers[constants.FULL_UPDATE] = Server_Full_Update
eventhandlers[constants.EVENT_PLAYER_DISCONNECT] = Server_Event_Disconnect
