from cell import Cell
from ship import Ship


class Field():
    def __init__(self, shape=(10, 10)):
        self.cells = [
            [Cell(x, y) for x in range(shape[0])]
            for y in range(shape[1])
        ]
        self.cells_dict = {}
        self._ships = []
        self.shape = shape

    def __str__(self):
        lines = [
            [chr(65 + i)] + [str(cell) for cell in line]
            for i, line in enumerate(self.cells)
        ]
        lines = [[' '] + [chr(49 + i) for i in range(9)] + ['10']] + lines
        return '\n'.join(' '.join(x for x in line) for line in lines)

    def empty(self, x, y):
        return self.cells[x][y].empty()

    @property
    def num_ships(self):
        result = [0] * 5
        for ship in self._ships:
            result[ship.size] += 1
        return result

    @property
    def ships(self):
        return self._ships

    def create_ship(self, ship):
        if ship.orientation == 0:
            for i in range(ship.x, ship.x + ship.size):
                self.cells[i][ship.y].set_ship()
                self.cells_dict[(i, ship.y)] = ship
        else:
            for i in range(ship.y, ship.y + ship.size):
                self.cells[ship.x][i].set_ship()
                self.cells_dict[(ship.x, i)] = ship
        self._ships.append(ship)

    def miss(self, x, y):
        self.cells[x][y].miss()

    def hit(self, x, y):
        self.cells[x][y].hit()
        ship = self.cells_dict[(x, y)]
        ship.hit()
        if ship.dead:
            self.kill(ship)

    def kill(self, ship):
        for x, y in self.neighborhood(ship):
            if self.cells[x][y].empty:
                self.miss(x, y)

    def alive(self):
        return any(ship.alive for ship in self._ships)

    def neighborhood(self, ship):
        if ship.orientation == 0:
            ship_coord = {(i, ship.y) for i in range(ship.x, ship.x + ship.size)}
        else:
            ship_coord = {(ship.x, i) for i in range(ship.y, ship.y + ship.size)}
        near_coord = set()
        for point in ship_coord:
            near_point = {
                (i, j) for i in range(point[0] - 1, point[0] + 2)
                for j in range(point[1] - 1, point[1] + 2)
                if 0 <= i < self.shape[0] and
                0 <= j < self.shape[1]
            }
            near_coord |= near_point
        return near_coord | ship_coord

    def check_cell(self, ship):
        if not 0 <= ship.x < self.shape[0]:
            return False
        if not 0 <= ship.y < self.shape[1]:
            return False
        if ship.orientation == 0 and ship.x > self.shape[0] - ship.size:
            return False
        if ship.orientation == 1 and ship.y > self.shape[1] - ship.size:
            return False
        for point in self.neighborhood(ship):
            if not self.empty(*point):
                return False
        return True
