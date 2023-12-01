from entity import Entity

class Bullet(Entity):
    def __init__(self, screen, size, address, angle, airplane):
        super().__init__(screen, size, address, angle, 0)
        self.move = 5
        self.x = airplane.x + airplane.sx/2
        self.y = airplane.y + airplane.sy/4
        self.change_size(15, 5)
        self.rotate = angle

    def update_position(self):
        if self.rotate == 270:
            self.x += self.move
        elif self.rotate == 90:
            self.x -= self.move

    def off_screen(self):
        return self.x <= self.sx or self.x >= self.size[0]-self.sx
