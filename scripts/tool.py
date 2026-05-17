from scripts.Object import Object
from scripts.pygameExtend import cos, sin
import pygame
import math

class tool(Object):
    tool_width = None
    tool_height = None
    hitbox_width = None
    hitbox_height = None

    def __init__(self, x, y, game, angle):
        super().__init__(x, y, game)
        self.image = None
        self.rotated_image = None
        self.angle = angle
        self.timer = 16
        self.image = game.assets['tools/' + self.__class__.__name__]
        self.animation = self.image.copy()
        self.touched = set([self.owner, self])
        self.width, self.height = self.get_tool_size()
        self.hbWidth, self.hbHeight = self.get_hitbox_size()
        self.sync_to_owner()

    def get_tool_size(self):
        if self.tool_width is not None and self.tool_height is not None:
            return self.tool_width, self.tool_height
        return self.animation.images[0].get_size()

    def get_hitbox_size(self):
        if self.hitbox_width is not None and self.hitbox_height is not None:
            return self.hitbox_width, self.hitbox_height
        return self.width, self.height

    def sync_to_owner(self):
        self.x = self.owner.x + self.owner.width // 2 - self.width // 2 + cos(self.angle) * self.height // 2
        self.y = self.owner.y + self.owner.height // 2 - self.height // 2 + sin(self.angle) * self.height // 2
        
    def tick(self):
        super().tick()
        self.sync_to_owner()
        self.timer -= 1 
        if self.timer <= 0:
            self.game.tools.remove(self)
        
    def render(self):
        super().render()