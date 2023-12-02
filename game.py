import pygame
from datetime import datetime
from airplane import Airplane
from bullet import Bullet

class Game:
    def __init__(self):
        pygame.init()
        self.size = [1000, 750]
        self.screen = pygame.display.set_mode(self.size)
        self.title = "My Game"
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.colors = {
            'RED': (255, 0, 0), 'ORANGE': (255, 153, 51), 'YELLOW': (255, 255, 0),
            'GREEN': (0, 255, 0), 'SEAGREEN': (60, 179, 113), 'BLUE': (0, 0, 255),
            'BLACK': (0, 0, 0), 'WHITE': (255, 255, 255), 'VIOLET': (204, 153, 255),
            'PINK': (255, 153, 153)
        }
        self.start_time = datetime.now()
        self.score = [0, 0]
        player_one = Airplane(self.screen, self.size, "./airplane.png", 270, 0) # left_player
        player_two = Airplane(self.screen, self.size, "./airplane.png", 90, 1) # right_player
        self.airplanes = [player_one, player_two]
        self.bullets = [[], []]
        self.bullet_spawn_rate = 10
        self.spawn_index = 0
        self.delta_time = 0
        self.run_game()

    def run_game(self):
        SB = 0
        while SB == 0:
            self.clock.tick(120)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        SB = 1
            self.screen.fill(self.colors['BLACK'])
            font = pygame.font.Font(None, 60)
            text = font.render("PRESS SPACE KEY TO START THE GAME", True, self.colors['WHITE'])
            self.screen.blit(text, (70, round(self.size[1]/2-50)))    
            pygame.display.flip()

        SB = 0
        while SB == 0:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    SB = 1
                else:
                    self.airplanes[0].handle_event(event)
                    self.airplanes[1].handle_event(event)

            self.update_game_state()
            self.draw_game_state()

        pygame.quit()    

    def update_game_state(self):
        now_time = datetime.now()
        self.delta_time = round((now_time - self.start_time).total_seconds())
    
        self.airplanes[0].update_position()
        self.airplanes[1].update_position()
    
        if self.airplanes[0].shooting:
            if self.spawn_index % self.bullet_spawn_rate == 0:
                bullet = Bullet(self.screen, self.size, "./bullet.png", 270, self.airplanes[0])
                self.bullets[0].append(bullet)
    
        if self.airplanes[1].shooting:
            if self.spawn_index % self.bullet_spawn_rate == 0:
                bullet = Bullet(self.screen, self.size, "./bullet.png", 90, self.airplanes[1])
                self.bullets[1].append(bullet)
    
        delete_bullet_list = []
        for i in range(len(self.bullets[0])):
            self.bullets[0][i].update_position()
            if self.bullets[0][i].off_screen():
                delete_bullet_list.append(self.bullets[0][i])
            
        for i in range(len(self.bullets[1])):
            self.bullets[1][i].update_position()
            if self.bullets[1][i].off_screen():
                delete_bullet_list.append(self.bullets[1][i])
        
        for i in range(len(self.bullets[1])):
            a = self.bullets[1][i]
            if self.airplanes[0].crash(a):
                delete_bullet_list.append(self.bullets[1][i])
                self.airplanes[0].image.set_alpha(128)
                self.score[0] += 1
            
        for i in range(len(self.bullets[0])):
            a = self.bullets[0][i]
            if self.airplanes[1].crash(a):
                delete_bullet_list.append(self.bullets[0][i]) 
                self.airplanes[1].image.set_alpha(128)
                self.score[1] += 1
            
        delete_bullet_list.reverse()
    
        for d in delete_bullet_list:
            if d in self.bullets[0]:
                self.bullets[0].remove(d)
            elif d in self.bullets[1]:
                self.bullets[1].remove(d)      
             
        self.spawn_index += 1
        self.airplanes[0].image.set_alpha(255)
        self.airplanes[1].image.set_alpha(255)

    def draw_game_state(self):
        self.screen.fill(self.colors['BLACK'])
    
        self.airplanes[0].show()
        self.airplanes[1].show()
    
        for bullet in self.bullets[0]:
            bullet.show()
        
        for bullet in self.bullets[1]:
            bullet.show()
        
        font = pygame.font.Font(None, 40)
        score_p1 = font.render("SCORE : {0}".format(self.score[0]), True, self.colors['YELLOW'])
        self.screen.blit(score_p1, (820, 0))
    
        score_p2 = font.render("SCORE : {0}".format(self.score[1]), True, self.colors['YELLOW'])
        self.screen.blit(score_p2, (0, 0))
    
        text_time = font.render("TIME : {0}".format(self.delta_time), True, self.colors['WHITE'])
        self.screen.blit(text_time, (430, 5))

        pygame.display.flip()
