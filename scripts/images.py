import pygame
import os

def loadImage(path):
    return pygame.image.load("assets/" + path +".png").convert_alpha()

def loadImages(path):
    images = []
    arr = os.listdir("assets/" + path)
    arr = sorted(arr, key=lambda x: int(x.split(".")[0]))
    for i, name in enumerate(arr):
        images.append(loadImage(path + "/" + str(i)))
    
    return images
        
class Animation():
    def __init__(self, path, loop = False):
        self.frame = 0
        self.images = loadImages(path)
        self.ticks = len(self.images)
        self.length = len(self.images)
        self.loop = loop
        self.tick = 0
    
    def update(self):
        self.image = self.images[self.frame]
        self.tick += 1
        if self.tick >= 4:
            if self.loop:
                self.frame = (self.frame+1)%self.ticks
            else:
                self.frame = min(self.frame+1, self.ticks-1)
            self.tick = 0
        return self.image
    