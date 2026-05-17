from scripts.Object import Object
import pygame

class player(Object):
    def __init__(self, x, y, game):
        super().__init__(x, y, game)
        self.speed = 20
        self.width = 50
        self.height = 50
        self.hbWidth = 20
        self.hbHeight = 40
        self.hp = 100
        self.animation = self.game.assets["default"].copy()
        
    def tick(self):
        self.movement = [0, 0]
        if pygame.key.get_pressed()[pygame.K_w]:
            self.movement[1] -= 1
        if pygame.key.get_pressed()[pygame.K_s]:
            self.movement[1] += 1
        if pygame.key.get_pressed()[pygame.K_a]:
            self.movement[0] -= 1
        if pygame.key.get_pressed()[pygame.K_d]:
            self.movement[0] += 1
            
        super().tick()
        
    def render(self):
        super().render()