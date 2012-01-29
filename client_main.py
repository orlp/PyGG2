#!/usr/bin/env python

from __future__ import division, print_function

import pygrafix
from pygrafix.window import key
from pygrafix.window import mouse

import precision_timer
import client.spectator
import engine.game
import engine.player
import engine.character
import client.rendering
import constants
import function

# DEBUG ONLY
import cProfile
import pstats
import os

def get_input(window):
    return {
        "up": window.is_key_pressed(key.W),
        "down": window.is_key_pressed(key.S),
        "left": window.is_key_pressed(key.A),
        "right": window.is_key_pressed(key.D),
    }

# the main client class
class Client(object):
    def __init__(self):
        # set display mode
        self.window = pygrafix.window.Window(800, 600, title = "PyGG2 - 0 FPS", fullscreen = False, vsync = False)

        # keep state of keys stored for one frame so we can detect down/up events
        self.keys = get_input(self.window)
        self.oldkeys = self.keys

        # create game engine object
        self.game = engine.game.Game()

        # TODO REMOVE THIS
        # create player
        self.our_player_id = engine.player.Player(self.game, self.game.current_state, 0).id
        self.spectator = client.spectator.Spectator(self.our_player_id)

        # create renderer object
        self.renderer = client.rendering.GameRenderer(self)

        # pygame time tracking
        self.clock = precision_timer.Clock()
        self.inputsender_accumulator = 0.0 # this counter will accumulate time to send input at a constant rate
        self.fpscounter_accumulator = 0.0 # this counter will tell us when to update the fps info in the title

    def run(self):
        # game loop
        while True:
            self.window.poll_events()

            # check if user exited the game
            if not self.window.is_open() or self.window.is_key_pressed(key.ESCAPE):
                break

            # handle input
            self.oldkeys = self.keys
            self.keys = get_input(self.window)
            leftmouse = self.window.is_mouse_button_pressed(mouse.LEFT)
            middlemouse = self.window.is_mouse_button_pressed(mouse.MIDDLE)
            rightmouse = self.window.is_mouse_button_pressed(mouse.RIGHT)

            mouse_x, mouse_y = self.window.get_mouse_position()
            our_player = self.game.current_state.players[self.our_player_id]
            our_player.up = self.keys["up"]
            our_player.down = self.keys["down"]
            our_player.left = self.keys["left"]
            our_player.right = self.keys["right"]
            our_player.leftmouse = leftmouse
            our_player.middlemouse = middlemouse
            our_player.rightmouse = rightmouse
            our_player.aimdirection = function.point_direction(self.window.width / 2, self.window.height / 2, mouse_x, mouse_y)

            if self.window.is_key_pressed(key._1):
                if our_player.character_id != None: # Kill ourself if not dead yet
                    self.game.current_state.entities[our_player.character_id].die(self.game, self.game.current_state)
                our_player.nextclass = engine.character.Scout # Change class
                our_player.spawn(self.game, self.game.current_state) # Spawn
            elif self.window.is_key_pressed(key._2):
                if our_player.character_id != None: # Kill ourself if not dead yet
                    self.game.current_state.entities[our_player.character_id].die(self.game, self.game.current_state)
                our_player.nextclass = engine.character.Pyro # Change class
                our_player.spawn(self.game, self.game.current_state) # Spawn
            elif self.window.is_key_pressed(key._3):
                if our_player.character_id != None: # Kill ourself if not dead yet
                    self.game.current_state.entities[our_player.character_id].die(self.game, self.game.current_state)
                our_player.nextclass = engine.character.Soldier # Change class
                our_player.spawn(self.game, self.game.current_state) # Spawn
            elif self.window.is_key_pressed(key._4):
                if our_player.character_id != None: # Kill ourself if not dead yet
                    self.game.current_state.entities[our_player.character_id].die(self.game, self.game.current_state)
                our_player.nextclass = engine.character.Heavy # Change class
                our_player.spawn(self.game, self.game.current_state) # Spawn
            elif self.window.is_key_pressed(key._7):
                if our_player.character_id != None: # Kill ourself if not dead yet
                    self.game.current_state.entities[our_player.character_id].die(self.game, self.game.current_state)
                our_player.nextclass = engine.character.Engineer # Change class
                our_player.spawn(self.game, self.game.current_state) # Spawn
            elif self.window.is_key_pressed(key._8):
                if our_player.character_id != None: # Kill ourself if not dead yet
                    self.game.current_state.entities[our_player.character_id].die(self.game, self.game.current_state)
                our_player.nextclass = engine.character.Spy # Change class
                our_player.spawn(self.game, self.game.current_state) # Spawn

            # did we just release the F11 button? if yes, go fullscreen
            if self.window.is_key_pressed(key.F11):
                self.window.toggle_fullscreen()

            # update the game and render
            frame_time = self.clock.tick()
            frame_time = min(0.25, frame_time) # a limit of 0.25 seconds to prevent complete breakdown

            self.fpscounter_accumulator += frame_time

            self.game.update(frame_time)
            self.renderer.render(self, self.game, frame_time)

            if self.fpscounter_accumulator > 0.5:
                self.window.set_title("PyGG2 - %d FPS" % self.window.get_fps())
                self.fpscounter_accumulator = 0.0

            self.window.flip()

        self.quit()

    def quit(self):
        # clean up
        self.window.close()

def profileGG2():
    cProfile.run("GG2main()", sort="time")

def GG2main():
    Client().run()

if __name__ == "__main__":
    # when profiling:
    profileGG2()
    # GG2main()
