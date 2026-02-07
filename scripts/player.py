from scripts.rotationalObject import rotationalObject
import pygame

class player(rotationalObject):
    def __init__(self, x, y, width, height, game):
        super().__init__(x, y, width, height, game)
        self.color = (0, 0, 255)
        
        
    def tick(self):
        self.movement = [0, 0]
        if pygame.key.get_pressed()[pygame.K_w]:
            self.movement[1] = -10
        if pygame.key.get_pressed()[pygame.K_s]:
            self.movement[1] = 10
        if pygame.key.get_pressed()[pygame.K_a]:
            self.movement[0] = -10
        if pygame.key.get_pressed()[pygame.K_d]:
            self.movement[0] = 10
        super().tick(self.movement[0], self.movement[1])
        
    def render(self, image):
        super().render(image)