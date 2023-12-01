import pygame

from entity import Entity

class Airplane(Entity):
    def __init__(self, screen, size, address, angle, player):
        super().__init__(screen, size, address, angle, player)
        if self.player == 0:
            self.x = self.sx
            self.y = round(self.size[1]/2 - self.sy/2)
        else:
            self.x = self.size[0]-self.sx- 70
            self.y = round(self.size[1]/2 - self.sy/2)
        self.up_go = False
        self.down_go = False
        self.shooting = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.player == 0:
                if event.key == pygame.K_w:
                    self.up_go = True
                if event.key == pygame.K_s:
                    self.down_go = True
                if event.key == pygame.K_LSHIFT:
                    self.shooting = True
            else:
                if event.key == pygame.K_UP:
                    self.up_go = True
                if event.key == pygame.K_DOWN:
                    self.down_go = True
                if event.key == pygame.K_RSHIFT:
                    self.shooting = True
        elif event.type == pygame.KEYUP:
            if self.player == 0:
                if event.key == pygame.K_w:
                    self.up_go = False
                if event.key == pygame.K_s:
                    self.down_go = False
                if event.key == pygame.K_LSHIFT:
                    self.shooting = False
            else:
                if event.key == pygame.K_UP:
                    self.up_go = False
                if event.key == pygame.K_DOWN:
                    self.down_go = False
                if event.key == pygame.K_RSHIFT:
                    self.shooting = False

    def update_position(self):
        if self.up_go:
            self.y -= self.move
            if self.y <= 0:
                self.y = 0
        elif self.down_go:
            self.y += self.move
            if self.y >= self.size[1] - self.sy + 30:
                self.y = self.size[1] - self.sy + 30
