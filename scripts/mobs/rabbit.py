from scripts.mobs.mobs import mobs

class rabbit(mobs):
    def __init__(self, x, y, game):
        super().__init__(x, y, 64, 56, game, 10)
        self.speed = 12
        
    def tick(self):
        super().tick()
        print(self.target)
        print(self.x, self.y)
        
    def render(self, image):
        super().render(self.game.assets["rabbit/idle"].update())