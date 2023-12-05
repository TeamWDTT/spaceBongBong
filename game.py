import random
import pygame
from datetime import datetime
from airplane import Airplane
from bullet import Bullet
from heart import Heart
from item import Item


class Game:
    def __init__(self):
        pygame.init()
        self.size = [1000, 750]
        self.screen = pygame.display.set_mode(self.size)
        self.title = "spaceBongBong" 
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
        player_one = Airplane(self.screen, self.size, "./images/airplane1.png", 270, 0) # left_player
        player_two = Airplane(self.screen, self.size, "./images/airplane2.png", 90, 1) # right_player
        self.airplanes = [player_one, player_two]
        self.bullets = [[], []]
        heart_p1 = []
        heart_p2 = []
        for i in range(5):
            heart_p1.append(Heart(self.screen, self.size, "./images/heart1.png", 0, 0, 40*i))
            heart_p2.append(Heart(self.screen, self.size, "./images/heart1.png", 0, 1, 840 + 40*(i-1)))
        self.hearts = [heart_p1, heart_p2]
        self.heart_index = [4, 4]
        self.spawn_index = 0
        self.delta_time = 0
        self.items = [Item(self.screen, self.size, ["./item_speed.png", "./item_bullet.png"], i % 2)]
        self.item_respawn_rate = 500
        self.item_respawn_index = 0
        self.run_game()

    def run_game(self):
        SB = 0

        #game start image
        start_image = pygame.image.load('./images/start.png')  

        while SB == 0:
            self.clock.tick(120)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        SB = 1
            
            self.screen.blit(start_image, (0, 0)) 
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

        self.airplanes[0].update_stealth()
        self.airplanes[1].update_stealth()

        if self.airplanes[0].shooting: # 총알 생성 - 1P
            if self.spawn_index % self.airplanes[0].bullet_spawn_rate == 0:
                bullet = Bullet(self.screen, self.size, "./images/bullet1.png", 270, self.airplanes[0])
                self.bullets[0].append(bullet)
    
        if self.airplanes[1].shooting: # 총알 생성 - 2P
            if self.spawn_index % self.airplanes[1].bullet_spawn_rate == 0:

                bullet = Bullet(self.screen, self.size, "./images/bullet2.png", 90, self.airplanes[1])
                self.bullets[1].append(bullet)
    
        delete_bullet_list = []
        delete_heart_list = []

        for i in range(len(self.bullets[0])): # 총알이 벽에 맞았을 때 - 1P

            self.bullets[0][i].update_position()
            if self.bullets[0][i].off_screen():
                delete_bullet_list.append(self.bullets[0][i])
            
        for i in range(len(self.bullets[1])): # 총알이 벽에 맞았을 때 - 2P
            self.bullets[1][i].update_position()
            if self.bullets[1][i].off_screen():
                delete_bullet_list.append(self.bullets[1][i])
        
        for i in range(len(self.bullets[0])): # 1P 총알이 2P 비행기에 맞았을 때
            a = self.bullets[0][i]
            if self.airplanes[1].crash(a):
                delete_bullet_list.append(self.bullets[0][i]) 
                self.score[1] += 1
                if self.heart_index[1] >= 0:
                    delete_heart_list.append(self.hearts[1][self.heart_index[1]])
                self.heart_index[1] -= 1
                if self.heart_index[1] == -1:
                    self.game_over("PLAYER 1") # winner
                
        for i in range(len(self.bullets[1])): # 2P 총알이 1P 비행기에 맞았을 때
            a = self.bullets[1][i]
            if self.airplanes[0].crash(a):
                delete_bullet_list.append(self.bullets[1][i])
                self.score[0] += 1
                if self.heart_index[0] >= 0:
                    delete_heart_list.append(self.hearts[0][self.heart_index[0]])
                self.heart_index[0] -= 1
                if self.heart_index[0] == -1:
                    self.game_over("PLAYER 2") # winner
            

        for i in range(len(self.bullets[0])):  # 아이템 적중 시 파괴 - 1P
            for item in self.items:
                if item.crash(self.bullets[0][i]):
                    item.apply_buff(self.airplanes[0])
                    self.items.remove(item)

        for i in range(len(self.bullets[1])): # 아이템 적중 시 파괴 - 2P
            for item in self.items:
                if item.crash(self.bullets[1][i]):
                    item.apply_buff(self.airplanes[1])
                    self.items.remove(item) 

        for i in range(len(self.bullets[0])):
            for item in self.items:
                if item.crash(self.bullets[0][i]):
                    delete_bullet_list.append(self.bullets[0][i])
                    item.apply_buff(self.airplanes[0])

        for i in range(len(self.bullets[1])):
            for item in self.items:
                if item.crash(self.bullets[1][i]):
                    item.apply_buff(self.airplanes[1])

        delete_bullet_list.reverse()
    
        for d in delete_bullet_list:
            if d in self.bullets[0]:
                self.bullets[0].remove(d)
            elif d in self.bullets[1]:
                self.bullets[1].remove(d)   
                
        for d in delete_heart_list:
            if d in self.hearts[0]:
                self.hearts[0].remove(d)
            elif d in self.hearts[1]:
                self.hearts[1].remove(d)   
             
        if self.item_respawn_index % self.item_respawn_rate == 0 and len(self.items) == 0:
            self.items.append(Item(self.screen, self.size, ["./item_speed.png", "./item_bullet.png"], random.randint(0, 1)))

        self.item_respawn_index += 1
        self.airplanes[0].image.set_alpha(255)
        self.airplanes[1].image.set_alpha(255)

        self.spawn_index += 1

    def draw_game_state(self):
        font_path = 'PressStart2P.ttf' # font

        # game main image
        main_background = pygame.image.load('./images/background.png')  
        self.screen.blit(main_background, (0, 0))  
    
        self.airplanes[0].show()
        self.airplanes[1].show()
    
        for bullet in self.bullets[0]:
            bullet.show()
        
        for bullet in self.bullets[1]:
            bullet.show()

        for item in self.items:
            item.show()

        font = pygame.font.Font(font_path, 20)  
        text_time = font.render("TIME : {0}".format(self.delta_time), True, self.colors['WHITE'])
        self.screen.blit(text_time, (430, 5))
        
        for heart in self.hearts[0]:
            heart.show()
            
        for heart in self.hearts[1]:
            heart.show()

        pygame.display.flip()
        
    def game_over(self, winner):
        SB = 0
        # game result image
        winner_player1 = pygame.image.load('./images/winPlayer1.png')
        winner_player2 = pygame.image.load('./images/winPlayer2.png')

        while SB == 0:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        SB = 1
            
            winner_image = winner_player1 if winner == "PLAYER 1" else winner_player2
            self.screen.blit(winner_image, (0,0))
            pygame.display.flip()
        pygame.quit()