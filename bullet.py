from entity import Entity

class Bullet(Entity):
    def __init__(self, screen, size, address, angle, airplane):
        super().__init__(screen, size, address, angle, 0)
        self.move = 5
        self.x = airplane.x + airplane.sx/2
        self.y = airplane.y + airplane.sy/4
        self.change_size(15, 5)
        self.rotate = angle
        self.airplane = airplane
        self.direction = None  

    def update_direction(self):
        if not self.airplane.check_touched: 
            if self.direction is None:
                if self.rotate == 270:  # left_player
                    self.direction = "RIGHTWARD"
                elif self.rotate == 90:  # right_player
                    self.direction = "LEFTWARD"
        else:
            if self.direction is None:
                if self.rotate == 270:
                    self.direction = "UPWARD"
                    self.change_rotate(90)
                elif self.rotate == 90:
                    self.direction = "DOWNWARD"
                    self.change_rotate(90)
    
    def update_position(self):
        self.update_direction()
        if self.direction == "RIGHTWARD":
            self.x += self.move
        elif self.direction == "LEFTWARD":
            self.x -= self.move
        elif self.direction == "UPWARD":
            self.y -= self.move
        elif self.direction == "DOWNWARD":
            self.y += self.move

    def off_screen(self):
        return self.x <= self.sx or self.x >= self.size[0] - self.sx
