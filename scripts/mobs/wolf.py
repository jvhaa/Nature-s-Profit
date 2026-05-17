from scripts.mobs.mobs import mobs

class wolf(mobs):
    def __init__(self, x, y, game):
        super().__init__(x, y, game)
        self.width = 64
        self.height = 56
        self.hbWidth = 64
        self.hbHeight = 56
        self.speed = 12
        self.lurkRange = 1000
        self.hp = 20
        self.animation = self.game.assets["wolf/idle"].copy()
        
    def tick(self):
        super().tick()
        
    def render(self):
        super().render()