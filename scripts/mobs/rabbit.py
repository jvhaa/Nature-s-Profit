from scripts.mobs.mobs import mobs

class rabbit(mobs):
    def __init__(self, x, y, game):
        super().__init__(x, y, 64, 56, game, 10)
        self.speed = 10
        
    def tick(self):
        super().tick()
        
    def render(self, image):
        super().render(self.game.assets["rabbit/idle"].update())