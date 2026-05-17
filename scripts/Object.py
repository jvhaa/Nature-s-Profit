import pygame
import math
from scripts.pygameExtend import cos, sin, collision

class Object():
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.game = game
        self.facingLeft = False
        self.movement = [0, 0]
        self.vel = [0, 0]
        self.speed = 0
        self.yoffset = 0
        self.angle = 90
        self.iframes = 0
        self.state = "idle"
        self.hitboxCorner = [(0, 0), (0, 0), (0, 0), (0, 0)]
        
    def tick(self):
        if self.movement[0] != 0:
            if self.movement[0] < 0:
                self.facingLeft = True
            else:
                self.facingLeft = False
        if self.movement != [0, 0]:
            angle = math.atan2(self.movement[1], self.movement[0])
            self.movement[0] = int(math.cos(angle) * self.speed)
            self.movement[1] = int(math.sin(angle) * self.speed)
        self.x += self.movement[0] + self.vel[0]
        self.y += self.movement[1] + self.vel[1]
        
    def render(self):
        self.image = self.animation.update()

        if self.facingLeft:
            self.image = pygame.transform.flip(self.image, False, True)
        
        
        self.image = pygame.transform.rotate(self.image, self.angle)
            
        x, y = self.centeredImage(self.image.get_width(), self.image.get_height())
            
        self.game.screen.blit(self.image, (x, y))
        
        self.hitboxCorner = self.hitbox()
        if self.iframes > 0:
            self.iframes -= 1
            self.shine()
        
    def centeredImage(self, imgWidth, imgHeight):
        center_x, center_y = self.centeredPos()
        draw_x = center_x - imgWidth / 2 
        draw_y = center_y - imgHeight / 2 
        
        return draw_x, draw_y
        
    def centeredPos(self):
        center_x = self.x + self.width / 2 - self.game.camera[0]
        center_y = self.y + self.height / 2 - self.game.camera[1] + self.yoffset
        return center_x, center_y
    
    def onBlock(self):
        return (self.x//self.game.tileMap.tileSize, self.y//self.game.tileMap.tileSize)
    
    def shine(self):
        mask = pygame.mask.from_surface(self.image)
        white = mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0))
        self.game.screen.blit(white.convert_alpha(), self.centeredImage(self.image.get_width(), self.image.get_height()))
    
    def showHitbox(self):
        pygame.draw.polygon(self.game.screen, (255, 0, 0), self.hitboxCorner, 1)
    
    def hitbox(self):
        x,y = self.centeredPos()
        y -= self.yoffset//2
        w, h = self.hbWidth/2, self.hbHeight/2
        cah, soh = cos(self.angle), sin(self.angle)
        
        localCorners = [(-w, -h),
                   (w, -h), 
                   (w, h), 
                   (-w, h)]
        
        corners = []
         
        for dx, dy in localCorners:
            rotated_x = dy * cah - dx * soh
            rotated_y = dy * soh + dx * cah
            corners.append((x + rotated_x, y + rotated_y))

        return corners
    
    def collision(self, other):
        return collision(self.hitboxCorner, other.hitboxCorner)