from __future__ import division, print_function

import pygrafix

import engine.gamestate
import constants

import function

import map_renderer
import character_renderer
import weapon_renderer
import projectile_renderer
import spectator
import engine.character
import engine.weapon
import engine.projectile

class GameRenderer(object):
    def __init__(self, client):
        self.window = client.window

        self.interpolated_state = engine.gamestate.Gamestate()
        self.renderers = {}
        self.focus_object_id = None

        self.view_width = constants.GAME_WIDTH
        self.view_height = constants.GAME_HEIGHT

        self.maprenderer = map_renderer.MapRenderer(self, "twodforttwo_remix")

        self.overlayblits = []

        self.renderers = {
            engine.character.Scout: character_renderer.ScoutRenderer(),
            engine.character.Soldier: character_renderer.SoldierRenderer(),
            engine.character.Heavy: character_renderer.HeavyRenderer(),
            engine.character.Engineer: character_renderer.EngineerRenderer(),
            engine.character.Spy: character_renderer.SpyRenderer(),
            engine.weapon.Scattergun: weapon_renderer.ScattergunRenderer(),
            engine.weapon.Rocketlauncher: weapon_renderer.RocketlauncherRenderer(),
            engine.weapon.Minigun: weapon_renderer.MinigunRenderer(),
            engine.weapon.Shotgun: weapon_renderer.ShotgunRenderer(),
            engine.weapon.Revolver: weapon_renderer.RevolverRenderer(),
            engine.projectile.Shot: projectile_renderer.ShotRenderer(),
            engine.projectile.Rocket: projectile_renderer.RocketRenderer()
        }

        self.world_sprites = pygrafix.sprite.SpriteGroup(scale_smoothing = False)
        self.hud_sprites = pygrafix.sprite.SpriteGroup(scale_smoothing = False)

    def render(self, client, game, frametime):
        # reset spritegroups
        self.world_sprites = pygrafix.sprite.SpriteGroup(scale_smoothing = False)
        self.hud_sprites = pygrafix.sprite.SpriteGroup(scale_smoothing = False)

        self.window = client.window
        alpha = game.accumulator / constants.PHYSICS_TIMESTEP

        self.interpolated_state.interpolate(game.previous_state, game.current_state, alpha)
        focus_object = self.interpolated_state.entities[self.interpolated_state.players[client.our_player_id].character_id]

        if focus_object != None:
            client.spectator.x = focus_object.x
            client.spectator.y = focus_object.y

        # update view
        self.xview = int(int(client.spectator.x) - self.view_width / 2)
        self.yview = int(int(client.spectator.y) - self.view_height / 2)

        # clear screen if needed
        if client.spectator.x <= self.view_width / 2 or client.spectator.x + self.view_width >= game.map.width or client.spectator.y <= self.view_height / 2 or self.yview + self.view_height >= game.map.height:
            self.window.clear()

        # draw background
        self.maprenderer.render(self, self.interpolated_state)

        # draw entities
        for entity in self.interpolated_state.entities.values():
            self.renderers[type(entity)].render(self, game, self.interpolated_state, entity)

        self.world_sprites.draw()
        self.hud_sprites.draw()

    def get_screen_coords(self, x, y):
        # calculate drawing position
        draw_x = int(x - self.xview)
        draw_y = int(y - self.yview)

        return draw_x, draw_y
