#!/usr/bin/env python

from __future__ import division, print_function

import math

import map
import character
import gamestate
import function
import constants

# the main engine class
class Game:
    def __init__(self):
        # client input
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.leftmouse = False
        self.middlemouse = False
        self.rightmouse = False
        self.mouse_x = 0
        self.mouse_y = 0

        # map data
        self.map = map.Map(self, "twodforttwo_remix")

        # game states
        self.current_state = gamestate.Gamestate()

        # if we are a client, then this is our player
        self.client_player_id = None

        # TODO MOVE THIS ELSEWHERE
        # start up by adding entities
        player = character.Scout(self, self.current_state)
        player.x = 2300
        player.y = 50
        self.client_player_id = player.id

        self.previous_state = self.current_state.copy()

        # this accumulator is used to update the engine in fixed timesteps
        self.accumulator = 0.0

    def sendinput(self, game, state):
        # Set Character input to this, later on we'll also send stuff here to the server.
        client = state.entities[self.client_player_id]

        client.up = self.up
        client.down = self.down
        client.left = self.left
        client.right = self.right
        client.leftmouse = self.leftmouse
        client.middlemouse = self.middlemouse
        client.rightmouse = self.rightmouse
        client.aimdirection = function.point_direction(constants.GAME_WIDTH / 2, constants.GAME_HEIGHT / 2, self.mouse_x, self.mouse_y)

    def update(self, frametime):
        self.accumulator += frametime

        while self.accumulator >= constants.PHYSICS_TIMESTEP:
            self.accumulator -= constants.PHYSICS_TIMESTEP

            self.previous_state = self.current_state.copy()
            self.current_state.update(self, constants.PHYSICS_TIMESTEP)
