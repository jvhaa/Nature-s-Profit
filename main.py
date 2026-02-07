import pygame
from scripts.player import player
from scripts.images import Animation, loadImages, loadImage

pygame.init()

class main():
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = player(100, 100, 50, 50, self)
        self.assets = {
            "default" : loadImage("default") ,
        }

    def run(self):
        while self.running:
            self.tick()
            self.render()
            
    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.player.tick()
        self.clock.tick(60)
        
    def render(self):
        self.screen.fill((255, 255, 255))
        self.player.render(self.assets["default"])
        pygame.display.flip()
        
main().run()