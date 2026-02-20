from scripts.mobs.mobs import mobs


class Smart(mobs):
    def __init__(self, x, y, width, height, game, speed):
        super().__init__(x, y, width, height, game, speed)
        
        
    def tick(self):
        super().tick()
        
    def render(self, image):
        return super().render(image)
    
    