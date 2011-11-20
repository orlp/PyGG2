from __future__ import division, print_function

import pygame

import engine.gamestate
import constants
import map

import character
import weapons
import projectile
import engine.character
import engine.weapons
import engine.projectile

class GameRenderer(object):
    def __init__(self, window):
        self.window = window
        self.backgroundcolor = pygame.Color(0, 0, 0, 255)
    
        self.interpolated_state = engine.gamestate.Gamestate()
        self.renderers = {}
        self.focus_object_id = None
        
        self.view_width = constants.GAME_WIDTH
        self.view_height = constants.GAME_HEIGHT
        
        self.map = map.MapRenderer(self, "twodforttwo_remix")
        
        self.overlayblits = []
        
        self.renderers = {
            engine.character.Scout: character.ScoutRenderer(),
            engine.weapons.Scattergun: weapons.ScattergunRenderer(),
            engine.projectile.Shot: projectile.ShotRenderer(),
            engine.projectile.Rocket: projectile.RocketRenderer()
        }
        
    def render(self, game, alpha, frametime):
        self.interpolated_state.interpolate(game.previous_state, game.current_state, alpha)
        self.focus_object_id = game.client_player_id
        
        # update view
        focus_object = self.interpolated_state.entities[self.focus_object_id]
        self.xview = int(int(focus_object.x) - self.view_width / 2)
        self.yview = int(int(focus_object.y) - self.view_height / 2)
        
        # clear screen if needed
        if focus_object.x <= self.view_width / 2 or focus_object.x + self.view_width >= self.map.image.get_width() or focus_object.y <= self.view_height / 2 or self.yview + self.view_height >= self.map.image.get_height():
            self.window.fill(self.backgroundcolor)
            
        # draw background
        self.map.draw(self, self.interpolated_state)
        
        # draw entities
        for entity in self.interpolated_state.entities.values():
            self.renderers[type(entity)].render(self, self.interpolated_state, entity)
        
        # blit overlay last
        for surface, offset in self.overlayblits:
            self.window.blit(surface, offset)
        self.overlayblits = []
    
    # this function is called to draw on the game's window with game world coordinate
    def draw_world(self, surface, offset = (0, 0)):
        width, height = surface.get_size()
        
        # calculate drawing position
        draw_x = int(offset[0] - self.xview)
        draw_y = int(offset[1] - self.yview)
        
        # even if we see a tiny little bit of the object, blit it - otherwise don't even blit
        if draw_x + width >= 0 and draw_x - width < self.view_width and draw_y + height >= 0 and draw_y - height < self.view_height:
            self.window.blit(surface, (draw_x, draw_y))
    
    # this function is called to draw over the game world with screen coordinates
    def draw_overlay(self, surface, offset = (0, 0)):
        width, height = surface.get_size()
        
        if offset[0] + width >= 0 and offset[0] - width < self.view_width and offset[1] + height >= 0 and offset[1] - height < self.view_height:
            self.overlayblits.append((surface, offset))
