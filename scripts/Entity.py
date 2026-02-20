import pygame
import math

class Entity():
    def __init__(self, x, y, width, height, game, speed=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.game = game
        self.facingLeft = False
        self.movement = [0, 0]
        self.vel = [0, 0]
        self.speed = speed
        
    def tick(self):
        if self.movement[0] != 0:
            if self.movement[0] < 0:
                self.facingLeft = True
            else:
                self.facingLeft = False
        if self.movement != [0, 0]:
            angle = math.atan2(self.movement[1], self.movement[0])
            self.movement[0] = int(math.cos(angle) * self.speed)
            self.movement[1] = int(math.sin(angle) * self.speed)
        self.x += self.movement[0] + self.vel[0]
        self.y += self.movement[1] + self.vel[1]
        
    def render(self, image):
        if self.facingLeft:
            image = pygame.transform.flip(image, True, False)

        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        draw_x = center_x - image.get_width() / 2 - self.game.camera[0]
        draw_y = center_y - image.get_height() / 2 - self.game.camera[1]
        self.game.screen.blit(image, (draw_x, draw_y))
        
    def onBlock(self):
        return (self.x//self.game.tileMap.tileSize, self.y//self.game.tileMap.tileSize)