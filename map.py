import pygame

class Map():
    def __init__(self, game, mapname):
        self.image = pygame.image.load("sprites/maps/" + mapname + ".png").convert()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*6, self.image.get_height()*6))

    def draw(self, game):        
        game.window.blit(self.image, (0, 0), (game.xview, game.yview, game.view_width, game.view_height))

class Collisionmap():
    def __init__(self, game, mapname):        
        self.image = pygame.image.load("sprites/collisionmaps/" + mapname + ".png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*6, self.image.get_height()*6))
        self.image.set_colorkey((255, 0, 255), pygame.RLEACCEL)
        
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()