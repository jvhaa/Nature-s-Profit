from scripts.envObject.resource import resource

class tree(resource):
    def __init__(self, x, y, game):
        super().__init__(x, y, game)
        self.image = self.game.assets['tree']
        self.animation = self.game.assets['tree'].copy()
        self.width = 300
        self.height = 900
        self.y -= 100
        self.yoffset = -800
        self.hbWidth = 300
        self.hbHeight = 100
        self.hp = 20

    def tick(self):
        super().tick()
        
    def render(self):
        super().render()