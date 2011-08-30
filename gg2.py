import pygame
from pygame.locals import *
from importMapRects import importMapRects
from gameobject import MapObject, PlayerControl, Character
from collision import objectCheckCollision, characterHitObstacle

class GG2:
    """
    Central class
    """
    
    # This is to replace the gmk "all" and also to update everything.
    GameObjectList = []
    
    Xview = 0
    Yview = 0
    
    def __init__(self):
        pygame.init()
        
        # All drawing should be done on the Surface object
        self.Window = pygame.display.set_mode((1280, 1024))
        self.Surface = pygame.display.get_surface()
        
        self.Wview = self.Window.get_width()
        self.Hview = self.Window.get_height()
        
        self.CollisionRectList = importMapRects()
        
        self.gameMap = MapObject(self)
        
        self.PlayerControl = PlayerControl(self)
        
        self.Myself = Character(self)
        
    def step(self):
        """
        'Steps' the engine. Twisted will step this at some point.
        """
        
        for a in range(len(self.GameObjectList)):

                self.GameObjectList[a].BeginStep()

        for a in range(len(self.GameObjectList)):

                self.GameObjectList[a].Step()

        for a in range(len(self.GameObjectList)):

                self.GameObjectList[a].EndStep()

        self.Xview = self.Myself.x-self.Wview/2
        self.Yview = self.Myself.y-self.Hview/2

        self.Surface.fill((255, 255, 255))

        for a in range(len(self.GameObjectList)):

                self.GameObjectList[a].Draw()

        for a in range(len(self.GameObjectList)):

                self.GameObjectList[a].Collide()

        pygame.display.flip()
