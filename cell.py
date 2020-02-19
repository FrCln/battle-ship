EMPTY = 0
SHIP = 1
DESTOIED_SHIP = 2
MISSED = 3


class Cell:
    def __init__(self, x, y, color=None, size=None):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.state = EMPTY

    def __str__(self):
        return str(self.state)

    def set_ship(self):
        self.state = SHIP

    def hit(self):
        if self.state == SHIP:
            self.state = DESTOIED_SHIP
        else:
            self.state = MISSED

    def draw(self):
        pass

    def empty(self):
        return self.state == EMPTY
