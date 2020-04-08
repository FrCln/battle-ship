from random import choice
from time import sleep


class AI:
    def __init__(self, shape=(10, 10)):
        n, m = shape
        self.empty_cells = [(i, j) for i in range(n) for j in range(m)]
        self.ship_to_kill = []

    def make_turn(self):
        sleep(0.5)
        if not self.ship_to_kill:
            x, y = choice(self.empty_cells)
            self.empty_cells.remove((x, y))
            return x, y
        else:
            for x, y in self.neighborhood():
                if (x, y) in self.empty_cells:
                    self.empty_cells.remove((x, y))
                    return x, y

    def neighborhood(self):
        x_coords = {coord[0] for coord in self.ship_to_kill}
        y_coords = {coord[1] for coord in self.ship_to_kill}
        if len(self.ship_to_kill) == 1:
            x, y = self.ship_to_kill[0]
            return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        else:
            if len(x_coords) == 1:
                x = x_coords.pop()
                return (x, min(y_coords) - 1), (x, max(y_coords) + 1)
            elif len(y_coords) == 1:
                y = y_coords.pop()
                return (min(x_coords) - 1, y), (max(x_coords) + 1, y)
            else:
                assert False, f'Ошибка в расстановке кораблей: {self.ship_to_kill[0]} ({x}, {y})'

    def get_empty_cells(self):
        res = set()
        for x, y in self.ship_to_kill:
            res.update({
                (x + i, y + j)
                for i in range(-1, 2)
                for j in range(-1, 2)
            })
        return res

    def miss(self, x, y):
        pass

    def hit(self, x, y):
        self.ship_to_kill.append((x, y))

    def kill(self, x, y):
        self.ship_to_kill.append((x, y))
        for x, y in self.get_empty_cells():
            if (x, y) in self.empty_cells:
                self.empty_cells.remove((x, y))
        self.ship_to_kill = []

