from cell import Cell

class Ship:
    def __init__(self, size, x, y, orientation):
        self.size = size
        self.x = x
        self.y = y
        self.orientation = orientation
        self.alive = True

    def kill(self):
        self.alive = False
