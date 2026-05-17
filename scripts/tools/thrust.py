import math
from scripts.pygameExtend import cos, sin
from scripts.tool import tool

class thrust(tool):
    def __init__(self, x, y, game, angle, speed):
        super().__init__(x, y, game, angle)
        self.speed = speed
        self.offset = 0
        
    def tick(self):
        super().tick()
        
        self.x += cos(self.angle) * (self.offset)
        self.y += sin(self.angle) * (self.offset)
        
        self.offset += self.speed
        
    def render(self):
        super().render()
        