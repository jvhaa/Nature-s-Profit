from scripts.Entity import Entity
import pygame
import random

class mobs(Entity):
    def __init__(self, x, y, width, height, game, speed):
        super().__init__(x, y, width, height, game)
        self.action = "none"
        self.target = [None, None]
        self.roamTimer = 0
        self.speed = speed
        self.targetEntities = []
        self.dangerEntities = []
        self.prey = {"mobs": [], "player": []}
        self.detectionRange = 200
        
    def tick(self):
        for entity in self.game.entities:
            if entity != self and self.distanceFrom(entity) < self.detectionRange:
                if entity.__class__.__name__ in self.prey[self.__class__.__name__]:
                    self.targetEntities.append(entity)
                elif self.__class__.__name__ in self.prey[entity.__class__.__name__]:
                    self.dangerEntities.append(entity)
        self.movement = [0, 0]
        if self.roamTimer == 0:
            self.roaming()
            self.roamTimer = random.randint(60, 180)
        if self.action == "none":
            self.roamTimer -= 1
        if self.target != [None, None]:
            if self.target == [self.x, self.y] and self.action == "roaming":
                self.action = "none"
            if self.x < self.target[0]:
                self.movement[0] = min(self.speed, self.target[0] - self.x)
            elif self.x > self.target[0]:
                self.movement[0] = max(-self.speed, self.target[0] - self.x)
            else:
                self.movement[0] = 0
            if self.y < self.target[1]:
                self.movement[1] = min(self.speed, self.target[1] - self.y)
            elif self.y > self.target[1]:
                self.movement[1] = max(-self.speed, self.target[1] - self.y)
            else:
                self.movement[1] = 0
        super().tick()
        
    def render(self, image):
        super().render(image)
        
    def roaming(self):
        self.action = "roaming"
        self.target = [
            self.x + random.randint(-300, 300),
            self.y + random.randint(-300, 300),
        ]
        
    def distanceFrom(self, entity):
        return ((self.x - entity.x) ** 2 + (self.y - entity.y) ** 2) ** 0.5
    
    def shortestPath(self, entities):
        closestEntity = None
        distance = float('inf')
        
        for entity in entities:
            d = (self.x - entity.x) ** 2 + (self.y - entity.y) ** 2
            if d < distance:
                distance = d
                closestEntity = entity
                
        return closestEntity
    
    def runAway(self, entities):
        closestEntity = self.shortestPath(entities)
        if closestEntity is not None:
            self.target = [
                self.x + (self.x - closestEntity.x),
                self.y + (self.y - closestEntity.y),
            ]
    
    def runTowards(self, entities):
        closestEntity = self.shortestPath(entities)
        if closestEntity is not None:
            self.target = [
                self.x + (closestEntity.x - self.x),
                self.y + (closestEntity.y - self.y),
            ]