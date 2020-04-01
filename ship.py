from cell import Cell

class Ship:
    def __init__(self, size, x, y, orientation):
        self.size = size
        self.x = x
        self.y = y
        self.orientation = orientation
        self.alive = size

    def __repr__(self):
        return f'Ship({self.size}, {self.x}, {self.y}, {self.orientation}), alive = {self.alive}'

    @property
    def dead(self):
        return self.alive == 0

    def hit(self):
        if self.alive:
            self.alive -= 1
