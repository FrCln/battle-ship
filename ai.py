from random import choice


class AI:
    def __init__(self, player_field):
        n, m = player_field.shape
        self.empty_cells = [(i, j) for i in range(n) for j in range(m)]
        self.player_field = player_field
        self.ship_to_kill = []
        self.dir = -1

    def check_player_field(self, x, y):
        if self.player_field.cells[x][y].ship():
            if self.ship_to_kill:
                if x == self.ship_to_kill[0][0]:
                    self.dir = 1
                elif y == self.ship_to_kill[0][1]:
                    self.dir = 0
                else:
                    raise ValueError(f'Ошибка в расстановке кораблей: {self.ship_to_kill[0]} ({x}, {y})')
            return True
        else:
            return False

    def choice(self):
        if not self.ship_to_kill:
            return choice(self.empty_cells)
        else:
            for x, y in self.neighborhood():
                if (x, y) in self.empty_cells:
                    return x, y

    def neighborhood(self):
        x_coords = [coord[0] for coord in self.ship_to_kill]
        y_coords = [coord[1] for coord in self.ship_to_kill]
        result = set()
        if self.dir == 1:
            for y in range(min(y_coords) - 1, max(y_coords) + 2):
                result.add((x_coords[0], y))
        elif self.dir == 0:
            for x in range(min(x_coords) - 1, max(x_coords) + 2):
                result.add((x, y_coords[0]))
        else:
            x = x_coords[0]
            y = y_coords[0]
            result = {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}
        return result

    def comp_turn(self):
        x, y = self.choice()
        self.empty_cells.remove((x, y))
        if self.check_player_field(x, y):
            ship = self.player_field.cells_dict[(x, y)]
            if ship.alive == 1:
                self.ship_to_kill = []
                self.dir = -1
                for x, y in self.player_field.neighborhood(ship):
                    if (x, y) in self.empty_cells:
                        self.empty_cells.remove((x, y))
            else:
                self.ship_to_kill.append((x, y))
        return x, y
