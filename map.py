from __future__ import division, print_function

import pygame
import function

class Map(object):
    def __init__(self, game, mapname):
        self.mapname = mapname
    
        self.image = function.load_image("maps/" + mapname)
        self.collision_image = function.load_image("collisionmaps/" + mapname)
        
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*6, self.image.get_height()*6))
        self.collision_image = pygame.transform.scale(self.collision_image, (self.collision_image.get_width()*6, self.collision_image.get_height()*6))
        
        self.image.set_colorkey((255, 0, 255), pygame.RLEACCEL)
        self.collision_image.set_colorkey((255, 0, 255), pygame.RLEACCEL)
        
        self.collision_mask = pygame.mask.from_surface(self.collision_image)

    def draw(self, game):        
        game.window.blit(self.image, (0, 0), (game.xview, game.yview, game.view_width, game.view_height))