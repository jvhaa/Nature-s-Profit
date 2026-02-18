from scripts.Entity import Entity
import pygame

class player(Entity):
    def __init__(self, x, y, width, height, game):
        super().__init__(x, y, width, height, game, speed=10)
        
        
    def tick(self):
        self.movement = [0, 0]
        if pygame.key.get_pressed()[pygame.K_w]:
            self.movement[1] = -1
        if pygame.key.get_pressed()[pygame.K_s]:
            self.movement[1] = 1
        if pygame.key.get_pressed()[pygame.K_a]:
            self.movement[0] = -1
        if pygame.key.get_pressed()[pygame.K_d]:
            self.movement[0] = 1
        super().tick()
        
    def render(self, image):
        super().render(image)