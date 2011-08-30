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
    globalGameObjectList = []
    
    globalXview = 0
    globalYview = 0
    
    def __init__(self):
        pygame.init()
        
        # All drawing should be done on the globalSurface object
        self.globalWindow = pygame.display.set_mode((1280, 1024))
        self.globalSurface = pygame.display.get_surface()
        
        self.globalWview = self.globalWindow.get_width()
        self.globalHview = self.globalWindow.get_height()
        
        self.globalCollisionRectList = importMapRects()
        
        self.gameMap = MapObject(self)
        
        self.globalPlayerControl = PlayerControl(self)
        
        self.globalMyself = Character(self)
        
    def step(self):
        """
        'Steps' the engine. Twisted will step this at some point.
        """
        
        for a in range(len(self.globalGameObjectList)):

                self.globalGameObjectList[a].BeginStep()

        for a in range(len(self.globalGameObjectList)):

                self.globalGameObjectList[a].Step()

        for a in range(len(self.globalGameObjectList)):

                self.globalGameObjectList[a].EndStep()

        self.globalXview = self.globalMyself.x-self.globalWview/2
        self.lobalYview = self.globalMyself.y-self.globalHview/2

        self.globalSurface.fill((255, 255, 255))

        for a in range(len(self.globalGameObjectList)):

                self.globalGameObjectList[a].Draw()

        for a in range(len(self.globalGameObjectList)):

                self.globalGameObjectList[a].Collide()

        pygame.display.flip()