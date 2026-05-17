from scripts.mobs.mobs import mobs

class rabbit(mobs):
    def __init__(self, x, y, game):
        super().__init__(x, y, game)
        self.width = 64
        self.height = 56
        self.hbWidth = 64
        self.hbHeight = 56
        self.speed = 12
        self.hp = 10
        self.animation = self.game.assets["rabbit/idle"].copy()
        
    def tick(self):
        super().tick()
        
    def render(self):
        super().render()