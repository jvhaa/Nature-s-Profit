import pygame
from scripts.Object import Object

class envObject(Object):
    def __init__(self, x, y, game, image=None):
        super().__init__(x, y, game)
        self.image = image
        self.hit = False
        
    def tick(self):
        super().tick()
        
    def render(self):
        super().render()
        
    def hitByTool(self, tool):
        self.hit = True
        
    