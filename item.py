import math
import pygame
from entity import Entity
import random

class Item(Entity):
    def __init__(self, screen, size, address_list, buff_type):
        super().__init__(screen, size, address_list[buff_type], 0, 0)
        self.change_size(70, 50)  # (은비) 크기 수정
        self.buff_type = buff_type  # 0: 비행기 속도+2 , 1: 총알속도 2배
        self.address_list = address_list
        self.setPosition()

    def setPosition(self): # 자꾸 위치가 주변부에 생겨서 만듦
        center_x, center_y = self.size[0] // 2, self.size[1] // 2
        radius = min(center_x, center_y) * 0.7

        # 각도와 반지름 생성
        angle = 2 * math.pi * random.random()
        r = random.uniform(0.5, 1) * radius

        # # 극좌표계 -> 직교좌표계
        self.x = int(center_x + r * math.cos(angle) - self.sx // 2)
        self.y = int(center_y + r * math.sin(angle) - self.sy // 2)


    def apply_buff(self, airplane):
        if self.buff_type == 0:
            airplane.move += 2
        elif self.buff_type == 1:
            airplane.bullet_spawn_rate /= 2