import pygame

class Map():
    def __init__(self, root):
        self.root = root
        
        self.sprite = pygame.image.load("sprites/maps/egypt.png").convert()
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width()*6, self.sprite.get_height()*6))

    def draw(self):
        self.root.Surface.blit(self.sprite, (0, 0), (self.root.Xview, self.root.Yview, self.root.Wview, self.root.Hview))

class CollisionMap():
    def __init__(self, root):
        self.root = root
        
        