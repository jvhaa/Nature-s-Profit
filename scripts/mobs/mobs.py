from scripts.Entity import Entity
import pygame
import random
import math

class mobs(Entity):
    def __init__(self, x, y, width, height, game, speed):
        super().__init__(x, y, width, height, game, speed)
        self.action = "none"
        self.target = [None, None]
        self.roamTimer = 0
        self.targetEntities = []
        self.dangerEntities = []
        self.interactions = {"mobs": {'player': "none"}, "player": {}, "rabbit": {"player": "fight", "rabbit": "flee"}}
        self.lurkRange = 100
        self.attackRange = 40
        self.dangerRange = 200
        self.heightenedAwareness = False
        self.heightendAwarenessTimer = 0
        self.heightenedAwarenessRange = 300
        
    def tick(self):
        self.targetEntities = []
        self.dangerEntities = []
        for entity in self.game.entities:
            if entity != self and self.distanceFromEntity(entity) < (self.dangerRange if not self.heightenedAwareness else self.heightenedAwarenessRange):
                if self.interactions[self.__class__.__name__][entity.__class__.__name__] == "fight":
                    self.targetEntities.append(entity)
            if entity != self and self.distanceFromEntity(entity) < (self.dangerRange if not self.heightenedAwareness else self.heightenedAwarenessRange):
                if self.interactions[self.__class__.__name__][entity.__class__.__name__] == "flee":
                    self.dangerEntities.append(entity)
        
        if self.dangerEntities:
            self.runAway(self.dangerEntities)
            self.action = "flee"
        elif self.targetEntities:
            self.runTowards(self.targetEntities)
            self.action = "attack"
        else:
            if self.action != "roaming":
                self.action = "none"
        
        self.movement = [0, 0]
        if self.roamTimer == 0:
            self.roaming()
            self.roamTimer = random.randint(60, 180)
        if self.action == "none":
            self.roamTimer -= 1
        if self.target != [None, None]:
            self.movement[0] = self.target[0] - self.x
            self.movement[1] = self.target[1] - self.y
            distance = self.distanceFrom(self.target[0], self.target[1])
            if distance < self.speed+10 and self.action == "roaming":
                self.action = "none"
                self.movement = [0, 0]
                self.target = [None, None]

        super().tick()
        
    def render(self, image):
        super().render(image)
        
    def roaming(self):
        self.action = "roaming"
        angle = random.uniform(0, 2*math.pi)
        rand = random.randint(10, 100)
        self.target = [
            self.x + math.cos(angle)*self.speed*rand,
            self.y + math.sin(angle)*self.speed*rand,
        ]
        
    def distanceFrom(self, x, y):
        return ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5
    
    def distanceFromEntity(self, entity):
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
            if self.x == closestEntity.x and self.y == closestEntity.y:
                angle = random.uniform(0, 2*math.pi)
                self.target = [
                    self.x + math.cos(angle)*self.speed*100,
                    self.y + math.sin(angle)*self.speed*100,
                ]
            self.roamTimer = 120
    
    def runTowards(self, entities):
        closestEntity = self.shortestPath(entities)
        if closestEntity is not None:
            self.target = [
                self.x + (closestEntity.x - self.x),
                self.y + (closestEntity.y - self.y),
            ]