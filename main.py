from __future__ import division, print_function

import math
import os

import pyglet
from pyglet.gl import *
from pyglet.window import key

import game
import constants

# debug
import cProfile, pstats
    
class GG2main(object):
    def __init__(self):
        # set pyglet settings
        pyglet.options["shadow_window"] = False
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
        # create window
        self.window = pyglet.window.Window(width=800, height=600, caption="PyGG2")
        self.window.switch_to()

        # time tracking
        self.accumulator = 0.0
        self.clock = pyglet.clock.Clock()
        self.fpsdisplay = pyglet.clock.ClockDisplay(clock=self.clock)
        
        # create game object
        self.game = game.Game(self.window)
        
        # key tracking
        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)
        self.oldkeys = self.keys.copy()
        
        # set hooks
        pyglet.clock.schedule(self.tick)
        
    def on_mouse_motion(x, y, dx, dy):
        self.game.mouse_x = x
        self.game.mouse_y = y
    
    def tick(self, dt):
        # use our own time management
        dt = self.clock.tick()
        
        # handle input
        self.game.left = self.keys[key.LEFT]
        self.game.right = self.keys[key.RIGHT]
        self.game.up = self.keys[key.UP] 
        self.game.down = self.keys[key.DOWN]
        self.game.leftmouse = False
        self.game.middlemouse = False
        self.game.rightmouse = False
        
        self.accumulator += dt
        
        while self.accumulator > constants.PHYSICS_TIMESTEP:
            self.game.update(constants.PHYSICS_TIMESTEP)
            self.accumulator -= constants.PHYSICS_TIMESTEP
        
        self.game.render(self.accumulator / constants.PHYSICS_TIMESTEP, dt)
        self.fpsdisplay.draw()
        
        self.oldkeys = self.keys.copy()
    
    def run(self):
        pyglet.app.run()
    
def profileGG2():
    cProfile.run("GG2main().run()", "game_profile")
    p = pstats.Stats("game_profile")
    p.sort_stats("cumulative")
    p.print_stats(30)
        
if __name__ == "__main__":
    profileGG2()
    # GG2main().run()