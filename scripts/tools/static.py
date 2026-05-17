import math
from scripts.pygameExtend import cos, sin
from scripts.tool import tool

class static(tool):
    def __init__(self, x, y, game, angle, speed):
        super().__init__(x, y, game, angle)
        self.speed = speed
        self.offset = 0
        self.x += cos(self.angle) * (self.offset)
        self.y += sin(self.angle) * (self.offset)
        
    def tick(self):
        super().tick()
        
        self.offset += self.speed
        
    def render(self):
        super().render()
        