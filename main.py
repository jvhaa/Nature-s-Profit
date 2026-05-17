import math
import sys
import random

import pygame
from scripts.envObject.tree import tree
from scripts.mobs.rabbit import rabbit
from scripts.mobs.wolf import wolf
from scripts.player import player
from scripts.mobs.mobs import mobs
from scripts.images import Animation, loadImages, loadImage
from scripts.sparks import Spark
from scripts.tools.axe import axe
from scripts.tools.sword import sword
from scripts.mapGenerator import map
from scripts.pygameExtend import angleBetweenTwoPoints, collision, cos, sin
import random

pygame.init()

class main():
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True
        self.mousePressed = False 
        self.assets = {
            "default" : Animation("default") ,
            "0" : loadImage("0"),
            "1" : loadImage("1"),
            "2" : loadImage("2"),
            "3" : loadImage("3"),
            "4" : loadImage("4"),
            "tools/axe" : Animation("tools/axe", loop=False),
            "tools/sword" : Animation("tools/sword", loop=False),  
            "rabbit/idle" : Animation("rabbit/idle", loop=True),
            "wolf/idle" : Animation("wolf/idle", loop=True),
            "tree" : Animation("tree", loop=True)
        }
        self.player = player(100, 100, self)
        self.objects = [
            self.player,
            ]
        self.entities = [self.player]
        self.tools = []
        self.sparks = []

        self.entities.extend([rabbit(random.randint(-2000, 2000), random.randint(-2000, 2000), self) for i in range(1000)])
        self.camera = [0, 0]
        self.tileMap = map(90, 70, self, 300) 
        for arr in [self.entities, self.tools, self.sparks]:
            self.objects.extend(arr)

    def run(self):
        while self.running:
            self.tick()
            self.render()
            
    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        mousePressed = pygame.mouse.get_pressed()[0]
        if self.mousePressed and not mousePressed:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle = angleBetweenTwoPoints(self.screen.get_width()//2, self.screen.get_height()//2, mouse_x, mouse_y)
            t = sword(self.player.x, self.player.y, self, angle, self.player)
            self.tools.append(t)
        
        self.mousePressed = mousePressed  
        self.clock.tick(60)
        for object in self.objects[:]:
            obj_rect = pygame.Rect(object.x-self.camera[0], object.y-self.camera[1]+object.yoffset, object.width, object.height)
            world_rect = pygame.Rect(-0.5*self.screen.get_width(), -0.5*self.screen.get_height(), 2*self.screen.get_width(), 2*self.screen.get_height())
            
            if not obj_rect.colliderect(world_rect):
                continue
            object.tick()
            
        for entity in self.entities.copy():
            if entity.iframes == 0:
                for tool in self.tools:
                    if collision(entity.hitboxCorner, tool.hitboxCorner) and entity not in tool.touched:
                        entity.iframes = 10
                        tool.touched.add(entity)
                        entity.hp -= 10
                        for i in range(5):
                            self.sparks.append(Spark(self, entity.x + entity.width / 2, entity.y + entity.height / 2 + entity.yoffset/2, tool.angle + random.uniform(-30, 30), random.randint(5, 10), (255, 255, 255)))
                        if entity.hp <= 0:
                            self.entities.remove(entity)
        
        self.sparks = [spark for spark in self.sparks if not getattr(spark, 'dead', False)]
        self.objects = []
        for arr in [sorted(self.entities + self.tools, key=lambda x: x.y), sorted(self.sparks, key=lambda x: x.y)]:
            self.objects.extend(arr)
        
    def render(self):
        self.camera = [self.player.x-self.screen.width//2+self.player.width//2, self.player.y-self.screen.height//2+self.player.height//2]
        self.tileMap.render()
        
        for object in self.objects:
            obj_rect = pygame.Rect(object.x-self.camera[0], object.y-self.camera[1]+object.yoffset, object.width, object.height)
            world_rect = pygame.Rect(0, 0, self.screen.get_width(), self.screen.get_height())
            
            if not obj_rect.colliderect(world_rect):
                continue
            object.render()
        pygame.display.flip()
        
main().run()