from random import choice


class AI:
    def __init__(self, player_field):
        n, m = player_field.shape
        self.empty_cells = [(i, j) for i in range(n) for j in range(m)]
        self.player_field = player_field


    def check_player_field(self, x, y):
        if self.player_field.cells[x][y].ship():
            self.player_field.hit(x, y)
            return True
        else:
            self.player_field.miss(x, y)
            return False


    def comp_turn(self):
        x, y = choice(self.empty_cells)
        self.empty_cells.remove((x, y))
        if self.check_player_field(x, y):
            ship = self.player_field.cells_dict[(x, y)]
            if ship.dead:
                for x, y in self.player_field.neighborhood(ship.size, ship.x, ship.y, ship.orientation):
                    if (x, y) in self.empty_cells:
                        self.empty_cells.remove((x, y))
            self.comp_turn()
