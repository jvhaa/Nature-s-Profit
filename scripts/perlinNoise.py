import math
import random

def lerp(a, b, t):
    return a + fade(t)* (b-a)

def fade(x):
    return 6 * x**5 - 15 * x ** 4 + 10 * x ** 3 

def generateGradients(width, height):
    gradients = {}
    for x in range(-width, width+1):
        for y in range(-height, height+1):
            angle = random.uniform(0, 2*math.pi)
            gradients[(x, y)] = (math.cos(angle), math.sin(angle))
    return gradients

def dotProduct(cx, cy, x, y, gradients):
    dx = x - cx
    dy = y - cy
    gx, gy = gradients[(cx, cy)]
    return dx*gx + dy*gy
    
class PerlinNoise():
    def __init__(self, width, height):
        self.gradients = generateGradients(width, height)
        
    def value(self, x, y):
        x = x/30
        y = y/30
        
        x0 = math.floor(x)
        x1 = x0+1
        y0 = math.floor(y)
        y1 = y0+1
        
        n0 = dotProduct(x0, y0, x, y, self.gradients)
        n1 = dotProduct(x1, y0, x, y, self.gradients)
        top = lerp(n0, n1, x-x0)
        
        n0 = dotProduct(x0, y1, x, y, self.gradients)
        n1 = dotProduct(x1, y1, x, y, self.gradients)
        bottom = lerp(n0, n1, x-x0)
        
        center = lerp(top, bottom, y-y0)
        return center
    
"""
p = PerlinNoise(20, 20)

width, height = 200, 200
noise = [[0] *width for _ in range(height)]

for y in range(height):
    for x in range(width):
        noise[y][x] = p.value(x, y)
        
import matplotlib.pyplot as plt
plt.imshow(noise, cmap="terrain")
plt.colorbar()
plt.show()
"""