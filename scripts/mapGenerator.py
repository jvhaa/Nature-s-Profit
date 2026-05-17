import pygame
from scripts.perlinNoise import PerlinNoise
from scripts.envObject.tree import tree
import math
import random

class map():
    def __init__(self, width, height, game, tileSize=20):
        self.width = width
        self.height = height
        self.pNoise = PerlinNoise(width, height)
        self.tile = {}
        self.game = game
        self.tileSize = tileSize
        self.tilemap()
        
    def tilemap(self):
        for y in range(-self.height, self.height):
            for x in range(-self.width, self.width):
                tileNumber = (self.pNoise.value(x, y)+0.6)/0.27
                self.tile[(x, y)] = self.game.assets[str(int(tileNumber))]
                if tileNumber < 2.5 and random.random() < 0.1/tileNumber:
                    self.game.entities.append(tree(x*self.tileSize, y*self.tileSize, self.game))
                    
    def render(self):
        left = (self.game.camera[0]-self.game.screen.width//2)//self.tileSize-5
        right = (self.game.camera[0]+self.game.screen.width//2)//self.tileSize+5
        top = (self.game.camera[1]-self.game.screen.height//2)//self.tileSize-5
        bottom = (self.game.camera[1]+self.game.screen.height//2)//self.tileSize+5
        
        for y in range(top, bottom):
            for x in range(left, right):
                try:
                    self.game.screen.blit(self.tile[x, y], (x*self.tileSize-self.game.camera[0], y*self.tileSize-self.game.camera[1]))
                except KeyError:
                    pass