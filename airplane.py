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

        self.bullet_spawn_rate = 20

        self.up_go = False
        self.down_go = False
        self.left_go = False
        self.right_go = False
        self.shooting = False
        self.check_touched = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN: #left_player
            if self.player == 0:
                if event.key == pygame.K_w:
                    self.up_go = True
                if event.key == pygame.K_s:
                    self.down_go = True
                if event.key == pygame.K_a:
                    self.left_go = True
                if event.key == pygame.K_d:
                    self.right_go = True    
                if event.key == pygame.K_LSHIFT:
                    self.shooting = True
            else: #right_player
                if event.key == pygame.K_UP:
                    self.up_go = True
                if event.key == pygame.K_DOWN:
                    self.down_go = True
                if event.key == pygame.K_LEFT:
                    self.left_go = True
                if event.key == pygame.K_RIGHT:
                    self.right_go = True
                if event.key == pygame.K_RSHIFT:
                    self.shooting = True
        elif event.type == pygame.KEYUP:
            if self.player == 0:
                if event.key == pygame.K_w:
                    self.up_go = False
                if event.key == pygame.K_s:
                    self.down_go = False
                if event.key == pygame.K_a:
                    self.left_go = False
                if event.key == pygame.K_d:
                    self.right_go = False
                if event.key == pygame.K_LSHIFT:
                    self.shooting = False
            else:
                if event.key == pygame.K_UP:
                    self.up_go = False
                if event.key == pygame.K_DOWN:
                    self.down_go = False
                if event.key == pygame.K_LEFT:
                    self.left_go = False
                if event.key == pygame.K_RIGHT:
                    self.right_go = False
                if event.key == pygame.K_RSHIFT:
                    self.shooting = False

    def update_position(self):
        if self.player == 0:  # left_player
            if not self.check_touched: 
                if self.up_go:
                    if self.y > 40: # interface height
                        self.y -= self.move
                elif self.down_go:
                    if self.y < self.size[1] - self.sy - 10:
                        self.y += self.move
            else:  
                if self.right_go:
                    if self.x < self.size[0] - self.sx - 70:
                        self.x += self.move
                elif self.left_go:
                    if self.x > self.sx:
                        self.x -= self.move

            # if airplane meet left bottom
            if (self.y >= self.size[1] - self.sy - 10) and (self.x == self.sx):
                self.check_touched = not self.check_touched
                if self.rotate == 270:
                    self.change_rotate(90)
                    self.rotate = 0
                else:
                    self.change_rotate(270)
                    self.rotate = 270

        else:  # right_player
            if not self.check_touched:  
                if self.up_go:
                    self.y -= self.move
                    if self.y <= 40: # interface height
                        self.y = 40
                elif self.down_go:
                    self.y += self.move
                    if self.y >= self.size[1] - self.sy + 30:
                        self.y = self.size[1] - self.sy + 30
            else:  
                if self.right_go:
                    if self.x < self.size[0] - self.sx - 70:
                        self.x += self.move
                elif self.left_go:
                    if self.x > self.sx:
                        self.x -= self.move

            # if airplane meet right top
            if (self.y == 40) and (self.x == self.size[0]-self.sx- 70):
                self.check_touched = not self.check_touched
                if self.rotate == 90:
                    self.change_rotate(90)
                    self.rotate = 180
                else :
                    self.change_rotate(270)
                    self.rotate = 90
