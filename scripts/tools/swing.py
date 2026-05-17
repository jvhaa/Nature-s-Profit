import math
from scripts.tool import tool

class swing(tool):
    def __init__(self, x, y, game, angle, speed):
        super().__init__(x, y, game, angle)
        self.speed = speed
        self.angle += 45
        
    def tick(self):
        super().tick()
        
        if self.timer >= 7:
            self.angle = (self.angle - self.speed) % 360
        
    def render(self):
        super().render()
        