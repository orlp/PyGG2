import pygame

class Map():
    def __init__(self, root):
        self.root = root
        
        self.image = pygame.image.load("sprites/maps/egypt.png").convert()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*6, self.image.get_height()*6))

    def draw(self):
        self.root.Surface.blit(self.image, (0, 0), (self.root.Xview, self.root.Yview, self.root.Wview, self.root.Hview))

class CollisionMap():
    def __init__(self, root):
        self.root = root
        
        self.image = pygame.image.load("sprites/collisionmaps/egypt.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*6, self.image.get_height()*6))
        self.image.set_colorkey((255, 0, 255), pygame.RLEACCEL)
        
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        
    def draw(self):
        self.root.Surface.blit(self.image, (0, 0), (self.root.Xview, self.root.Yview, self.root.Wview, self.root.Hview))