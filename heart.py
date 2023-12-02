import pygame
from entity import Entity

class Heart(Entity):
    
    def __init__(self, screen, size, address, angle, player, x):
        super().__init__(screen, size, address, angle, player)
        self.address = address
        self.x, self.y = x, 0
        self.change_size(40, 40)