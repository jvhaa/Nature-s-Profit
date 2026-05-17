import math
import pygame
from scripts.Object import Object
from scripts.pygameExtend import cos, sin

class Spark():
    def __init__(self, game, x, y, angle, speed, color=(255,255,255)):
        self.game = game
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.color = color
        self.forward_x = cos(self.angle)
        self.forward_y = sin(self.angle)
        self.side_x = -self.forward_y
        self.side_y = self.forward_x
        self.yoffset = 0
        self.width = 5
        self.height = 5

    def tick(self):
        self.x += self.forward_x * self.speed
        self.y += self.forward_y * self.speed
        self.speed = max(0, self.speed-0.2)
        if self.speed == 0:
            self.dead = True

    def render(self):
        screen_x = self.x - self.game.camera[0]
        screen_y = self.y - self.game.camera[1] + self.yoffset
        
        fpx = self.forward_x * self.speed
        fpy = self.forward_y * self.speed
        spx = self.side_x * self.speed
        spy = self.side_y * self.speed

        p1 = (screen_x + fpx * 6, screen_y + fpy * 6)
        p2 = (screen_x + spx * 1, screen_y + spy * 1)
        p3 = (screen_x - fpx * 6, screen_y - fpy * 6)
        p4 = (screen_x - spx * 1, screen_y - spy * 1)

        pygame.draw.polygon(self.game.screen, self.color, [p1, p2, p3, p4])