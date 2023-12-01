import pygame

class Entity:
    def __init__(self, screen, size, address, angle, player):
        self.screen = screen
        self.size = size
        self.x, self.y, self.move = 0, 0, 8
        if address[-3:] == "png":
            self.image = pygame.image.load(address).convert_alpha()
        else:
            self.image = pygame.image.load(address)
        self.sx, self.sy = self.image.get_size()
        self.change_size(50, 80)
        self.change_rotate(angle)
        self.player = player

    def change_size(self, sx, sy):
        self.image = pygame.transform.scale(self.image, (sx, sy))
        self.sx, self.sy = self.image.get_size()
        
    def change_rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        self.rotate = angle        
        
    def show(self):
        self.screen.blit(self.image, (self.x, self.y))

    def crash(self, other):
        if (self.x-other.sx <= other.x) and (other.x <= self.x+self.sx):
            if (self.y-other.sy <= other.y) and (other.y <= self.y+self.sy):
                return True
            else:
                return False
        else : 
            return False
