from scripts.envObject.envObject import envObject

class resource(envObject):
    def __init__(self, x, y, game):
        super().__init__(x, y, game)
        self.shakeTimer = 0
        
    def tick(self):
        super().tick()
        if self.shakeTimer % 11 == 1:
            self.shakeTimer -= 1
            self.shake()
        
    def render(self):
        super().render()
        
    def shake(self):
        self.xvel = 10
        self.yvel = 10
        