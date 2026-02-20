import pygame
from scripts.mobs.rabbit import rabbit
from scripts.player import player
from scripts.mobs.mobs import mobs
from scripts.images import Animation, loadImages, loadImage
from scripts.mapGenerator import map

pygame.init()

class main():
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = player(100, 100, 50, 50, self)
        self.assets = {
            "default" : loadImage("default") ,
            "0" : loadImage("0"),
            "1" : loadImage("1"),
            "2" : loadImage("2"),
            "3" : loadImage("3"),
            "4" : loadImage("4"),
            "rabbit/idle" : Animation("rabbit/idle", loop=True),
        }
        self.entities = [
            self.player,
            rabbit(400, 400, self)]
        self.renderObjects = self.entities.copy()
        self.camera = [0, 0]
        self.tileMap = map(900, 700, self, 300) 

    def run(self):
        while self.running:
            self.tick()
            self.render()
            
    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.clock.tick(60)
        for entity in self.entities:
            entity.tick()
        self.camera = [self.player.x-self.screen.width//2+self.player.width//2, self.player.y-self.screen.height//2+self.player.height//2]
        
    def render(self):
        self.tileMap.render()
        
        self.renderObjects = sorted(self.renderObjects, key=lambda x: x.y)
        for object in self.renderObjects:
            object.render(self.assets["default"])
        pygame.display.flip()
        
main().run()