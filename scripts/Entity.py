import pygame
import math

class Entity():
    def __init__(self, x, y, width, height, game):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.game = game
        self.facingLeft = False
        self.movement = [0, 0]
        self.vel = [0, 0]
        
    def tick(self):
        if self.movement[0] != 0:
            if self.movement[0] < 0:
                self.facingLeft = True
            else:
                self.facingLeft = False
        self.x += self.movement[0] + self.vel[0]
        self.y += self.movement[1] + self.vel[1]
        
    def render(self, image):
        if self.facingLeft:
            image = pygame.transform.flip(image, True, False)

        self.game.screen.blit(image, (self.x-self.game.camera[0], self.y-self.game.camera[1]))
        
    def onBlock(self):
        return (self.x//self.game.tileMap.tileSize, self.y//self.game.tileMap.tileSize)