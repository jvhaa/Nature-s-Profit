from scripts.tools.thrust import thrust

class sword(thrust):
    tool_width = 50
    tool_height = 100
    hitbox_width = 50
    hitbox_height = 100

    def __init__(self, x, y, game, angle, owner):
        self.owner = owner
        super().__init__(x, y, game, angle, 10)
        self.animation = self.game.assets["tools/sword"].copy()
        
    def tick(self):
        super().tick()
        
    def render(self):
        super().render()