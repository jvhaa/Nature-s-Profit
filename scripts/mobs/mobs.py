from scripts.Object import Object
import pygame
import random
import math
import heapq

class mobs(Object):
    def __init__(self, x, y, width, height, game, speed):
        super().__init__(x, y, width, height, game, speed)
        self.action = "none"
        self.target = []
        self.roamTimer = 0
        self.targetObjects = []
        self.dangerObjects = []
        self.interactions = {
            "rabbit": {"player": "none", "rabbit": "none", "wolf": "flee"}, 
            "wolf": {"player": "none", "rabbit": "fight", "wolf": "none"}
                             }
        self.lurkRange = 200
        self.attackRange = 40
        self.dangerRange = 1000
        self.heightenedAwarenessRange = 50
        self.health = 100
        self.damage = 20
        
    def tick(self):
        self.targetObjects = []
        self.dangerObjects = []
        for object in self.game.objects:
            if object != self and self.distanceFromObject(object) < self.lurkRange:
                if self.interactions[self.__class__.__name__][object.__class__.__name__] == "fight":
                    self.targetObjects.append(object)
            if object != self and self.distanceFromObject(object) < self.dangerRange:
                if self.interactions[self.__class__.__name__][object.__class__.__name__] == "flee":
                    self.dangerObjects.append(object)
        
        if self.dangerObjects:
            self.runAway(self.dangerObjects)
            self.action = "flee"
        elif self.targetObjects:
            self.runTowards(self.targetObjects)
            self.action = "fight"
        else:
            if self.action in ["flee", "fight"]:
                self.action = "none"
                self.target = []
        
        self.movement = [0, 0]
        if self.roamTimer == 0:
            self.roaming()
            self.roamTimer = random.randint(60, 180)
        if self.action == "none":
            self.roamTimer -= 1
        if self.target != []:
            tar = self.target[0]
            self.movement[0] = tar[0] - self.x
            self.movement[1] = tar[1] - self.y
            distance = self.distanceFrom(tar[0], tar[1])
            if distance < self.speed+10 and self.action == "roaming":
                self.action = "none"
                self.movement = [0, 0]
                self.target.pop(0)

        super().tick()
        
    def render(self, image):
        super().render(image)
        
    def roaming(self):
        self.action = "roaming"
        angle = random.uniform(0, 2*math.pi)
        rand = random.randint(10, 100)
        self.target = [[
            self.x + math.cos(angle)*self.speed*rand,
            self.y + math.sin(angle)*self.speed*rand,
        ]]
        
    def distanceFrom(self, x, y):
        return ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5
    
    def distanceFromObject(self, object):
        return ((self.x - object.x) ** 2 + (self.y - object.y) ** 2) ** 0.5
    
    def shortestPath(self, objects):
        closestObject = None
        distance = float('inf')
        
        for object in objects:
            d = (self.x - object.x) ** 2 + (self.y - object.y) ** 2
            if d < distance:
                distance = d
                closestObject = object
                
        return closestObject
    
    def runAway(self, objects):
        grid = [[0 for _ in range(11)] for _ in range(11)]
        pos = self.onBlock()
        
        for object in objects:
            x, y = object.onBlock()
            relx, rely = x - pos[0], y - pos[1]
            if isinstance(object, mobs):
                initial = min(math.floor(object.damage/self.health * 10), 10)
                radius = math.ceil(object.lurkRange/self.game.tileMap.tileSize)
                rateOfChange = initial/radius
                for i in range(-radius, radius+1):
                    for j in range(-radius, radius+1):
                        dist = math.sqrt(i*i + j*j)
                        xPos, yPos = relx+5+i, rely+5+j
                        if 0 <= xPos < 11 and 0 <= yPos < 11:
                            grid[xPos][yPos] += max(0, initial - math.ceil(dist*rateOfChange))
                            
        minimum = 10000
        low_threat_cells = []
        
        for y, line in enumerate(grid):
            for x, cell in enumerate(line):
                if type(cell) == int and not (x == 5 and y == 5):
                    if cell < minimum:
                        minimum = cell
                        low_threat_cells = [(x, y)]
                    elif cell == minimum:
                        low_threat_cells.append((x, y))
        
        if low_threat_cells:
            target = random.choice(low_threat_cells)
        else:
            target = (5, 5)
                        
        path = self.aStar(grid, (5, 5), target)
        if path:
            self.target = [[t[0]* self.game.tileMap.tileSize, t[1] * self.game.tileMap.tileSize] for t in path]
        else:
            self.target = []
        
    def aStar(self, grid, start, goal):
        row, col = len(grid), len(grid)
        
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        openSet = []
        heapq.heappush(openSet, (heuristic(start, goal), 0, start, [start]))
        
        visited = set()
        
        while openSet:
            f_score, g_score, cur, path = heapq.heappop(openSet)
            if cur in visited: continue
            visited.add(cur)
            
            if cur == goal:
                return path
            
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (cur[0] + dx, cur[1] + dy)
                if 0 <= neighbor[0] < row and 0 <= neighbor[1] < col and grid[neighbor[0]][neighbor[1]] != "U":
                    newG = g_score + 1
                    newF = newG + heuristic(neighbor, goal) + grid[neighbor[0]][neighbor[1]]
                    heapq.heappush(openSet, (newF, newG, neighbor, path + [neighbor]))
        return None
            
            
    def runTowards(self, objects):
        closestObject = self.shortestPath(objects)
        if closestObject is not None:
            self.target = [[closestObject.x, closestObject.y]]