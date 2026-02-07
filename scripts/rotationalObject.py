import pygame
import math

class rotationalObject():
    def __init__(self, x, y, width, height, game):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.game = game
        self.angle = 0
        
    def tick(self, xMove, yMove):
        if xMove != 0 or yMove != 0:
            angle = math.atan2(-yMove, xMove)
            angle = math.degrees(angle) 
            smoothing = 0.15 
            delta = (angle - self.angle + 180) % 360 - 180
            self.angle += delta * smoothing
        self.x += xMove
        self.y += yMove
        
    def render(self, image):
        base_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        rotated_image = pygame.transform.rotate(image, self.angle - 90)
        rotated_rect = rotated_image.get_rect()

        self.game.screen.blit(rotated_image, (self.x, self.y))