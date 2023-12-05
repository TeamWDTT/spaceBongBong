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
        self.has_rotated_recently = False
        self.rotate = angle

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
                    if self.y > 50: # interface height
                        self.y -= self.move
                    elif self.y <= 50:
                        self.y = 50
                elif self.down_go:
                    if self.y < self.size[1] - self.sy - 10:
                        self.y += self.move
                    elif self.y >= self.size[1]:
                        self.y = self.size[1] - self.sy - 10
            else:  
                if self.right_go:
                    if self.x < self.size[0] - self.sx - 70:
                        self.x += self.move
                elif self.left_go:
                    if self.x > self.sx:
                        self.x -= self.move

            # if airplane meet left bottom
            if (self.y >= self.size[1] - self.sy - 10) and (self.x <= self.sx):
                if not self.has_rotated_recently:
                    self.check_touched = not self.check_touched
                    if self.rotate == 270:
                        self.change_rotate(90)
                        self.rotate = 0
                        self.has_rotated_recently = True
                    else:
                        self.change_rotate(270)
                        self.rotate = 270
                        self.has_rotated_recently = True
            else:
                self.has_rotated_recently = False

        else:  # right_player
            if not self.check_touched:  
                if self.up_go:
                    self.y -= self.move
                    if self.y <= 40: # interface height
                        self.y = 40
                elif self.down_go: 
                    self.y += self.move
                    if self.y >= self.size[1] - self.sy + 20: # 아래쪽 벽 보정값 20
                        self.y = self.size[1] - self.sy + 20
            else:  
                if self.right_go:
                    if self.x < self.size[0] - self.sx - 70: # 오른쪽 벽 보정값 70
                        self.x += self.move
                elif self.left_go:
                    if self.x > self.sx + 20: # 왼쪽 벽 보정값 20
                        self.x -= self.move

            # if airplane meet right top
            if (self.y == 40) and (self.x >= self.size[0]-self.sx- 70):
                if not self.has_rotated_recently:
                    self.check_touched = not self.check_touched
                    if self.rotate == 90:
                        self.change_rotate(90)
                        self.rotate = 180
                        self.has_rotated_recently = True
                    else :
                        self.change_rotate(270)
                        self.rotate = 90
                        self.has_rotated_recently = True
            else:
                self.has_rotated_recently = False
