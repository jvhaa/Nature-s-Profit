from scripts.Object import Object
import pygame
import random
import math
import heapq

class mobs(Object):
    def __init__(self, x, y, game):
        super().__init__(x, y, game)
        self.action = "none"
        self.target = []
        self.roamTimer = 0
        self.targetObjects = []
        self.dangerObjects = []
        self.interactions = {
            "rabbit": {"player": "none", "rabbit": "none", "wolf": "flee", "tree" : "none"}, 
            "wolf": {"player": "none", "rabbit": "chase", "wolf": "none", "tree": "none"}
                             }
        
        self.chaseRange = 200
        self.attackRange = 40
        self.dangerRange = 1000
        self.health = 100
        self.damage = 20
        self.downTimer = 0
        
    def tick(self):
        if self.downTimer == 0:
            self.downTimer = 100
            self.targetObjects = []
            self.dangerObjects = []
        
            for entity in self.game.entities:
                if entity != self and self.distanceFromObject(entity) < self.chaseRange:
                    if self.interactions[self.__class__.__name__][entity.__class__.__name__] in ["chase", "attack"]:
                        self.targetObjects.append(entity)
                if entity != self and self.distanceFromObject(entity) < self.dangerRange:
                    if self.interactions[self.__class__.__name__][entity.__class__.__name__] == "flee":
                        self.dangerObjects.append(entity)
        
            if self.dangerObjects:
                if self.action != "flee" or not self.target:
                    self.runAway(self.dangerObjects)
                self.action = "flee"
            elif self.targetObjects:
                self.runTowards(self.targetObjects)
                self.action = "chase"
            else:
                if self.action in ["flee", "chase"]:
                    self.action = "none"
                    self.target = []
        else:
            self.downTimer -= 1
        
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
            if distance < self.speed+10:
                self.movement = [0, 0]
                self.target.pop(0)
                if not self.target:
                    self.action = "none"
        
        super().tick()
        
    def render(self):
        super().render()
        
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
        r, c = self.dangerRange//self.game.tileMap.tileSize + 1, self.dangerRange//self.game.tileMap.tileSize + 1
        grid = [[0 for _ in range(r)] for _ in range(c)]
        pos = self.onBlock()
        gridPos = (r//2+1, c//2+1)
        
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
                        xPos, yPos = relx+r//2+1+i, rely+c//2+1+j
                        if 0 <= xPos < r and 0 <= yPos < c:
                            grid[xPos][yPos] += max(0, initial - math.ceil(dist*rateOfChange))
                            
        minimum = 10000
        low_threat_cells = []
        
        for y, line in enumerate(grid):
            for x, cell in enumerate(line):
                if type(cell) == int and not (x == r//2+1 and y == c//2+1):
                    if cell < minimum:
                        minimum = cell
                        low_threat_cells = [(x, y)]
                    elif cell == minimum:
                        low_threat_cells.append((x, y))
        
        if low_threat_cells:
            target = random.choice(low_threat_cells)
            
        path = self.aStar(grid, gridPos, target)
        if path:
            curPos = self.onBlock()
            self.target = [[(t[0]-r//2-1+curPos[0])* self.game.tileMap.tileSize, (t[1]-c//2-1+curPos[1]) * self.game.tileMap.tileSize] for t in path[1:]]
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