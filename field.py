from tkinter import *

from cell import Cell
from ship import Ship


class Field:
    def __init__(self, canvas, x, y, cell_size, draw=True, shape=(10, 10)):
        self.cells = [
            [Cell(x, y) for x in range(shape[0])]
            for y in range(shape[1])
        ]
        self._ships = []
        self.shape = shape
        self.canvas = canvas
        self.x = x
        self.y = y
        self.cell_size = cell_size
        if draw:
            self.draw_field()

    def __str__(self):
        lines = [
            [chr(65 + i)] + [str(cell) for cell in line]
            for i, line in enumerate(self.cells)
        ]
        lines = [[' '] + [chr(49 + i) for i in range(9)] + ['10']] + lines
        return '\n'.join(' '.join(x for x in line) for line in lines)

    def empty(self, x, y):
        return self.cells[x][y].empty()

    def draw_field(self):
        self.rect = self.canvas.create_rectangle(
            self.x,
            self.y,
            self.x + self.cell_size * 10,
            self.y + self.cell_size * 10,
            fill='cyan'
        )

        for i in range(1, 10):
            self.canvas.create_line(
                self.x + i * self.cell_size,
                self.y,
                self.x + i * self.cell_size,
                self.y + self.cell_size * 10
            )

        for i in range(1, 10):
            self.canvas.create_line(
                self.x,
                self.y + i * self.cell_size,
                self.x + self.cell_size * 10,
                self.y + i * self.cell_size
            )

        for i in range(10):
            self.canvas.create_text(
                self.x - self.cell_size / 2,
                self.y + self.cell_size / 2 + i * self.cell_size,
                text=chr(65 + i)
            )

        for i in range(10):
            self.canvas.create_text(
                self.x + self.cell_size / 2 + i * self.cell_size,
                self.y - self.cell_size / 2,
                text=str(i + 1)
            )

    def click_field(self, event):
        x, y = event.x, event.y
        if self.rect in self.canvas.find_overlapping(x, y, x, y):
            x = (x - self.cell_size * 25 // 10) // self.cell_size
            y = (y - self.cell_size * 25 // 10) // self.cell_size
            if self.empty(x, y):
                self.choose_ship(x, y)

    def choose_ship(self, x, y):
        def click():
            if self.check_cell(ship_size.get(), x, y, orientation.get()):
                self.create_ship(ship_size.get(), x, y, orientation.get())
                window.destroy()
            else:
                window.bell()
        window = Tk()
        window.title('Выбор корабля')
        ship_size = IntVar(window)
        ship_size.set(1)
        sizes = []
        for i in range(1, 5):
            r = Radiobutton(window, text=f'{i}-палубный', variable=ship_size, value=i)
            sizes.append(r)
            r.grid(row=i - 1, column=0)
        orientation = IntVar(window)
        orientation.set(0)
        hor = Radiobutton(window, text=f'горизонтально', variable=orientation, value=0)
        hor.grid(row=0, column=1)
        vert = Radiobutton(window, text=f'вертикально', variable=orientation, value=1)
        vert.grid(row=1, column=1)
        b = Button(window, text='OK')
        b.config(command=click)
        b.grid(row=2, column=1, rowspan=2)

    def _get_neibourhood(self, size, x, y, orientation):
        if orientation == 0:
            ship_coord = {(i, y) for i in range(x, x + size)}
        else:
            ship_coord = {(x, i) for i in range(y, y + size)}
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

    def check_cell(self, size, x, y, orientation):
        if not 0 <= x < self.shape[0]:
            return False
        if not 0 <= y < self.shape[1]:
            return False
        if orientation == 0 and x >= self.shape[0] - size:
            return False
        if orientation == 1 and y >= self.shape[1] - size:
            return False
        for point in self._get_neibourhood(size, x, y, orientation):
            if not self.empty(*point):
                return False
        return True

    def create_ship(self, size, x, y, orientation):
        ship = Ship(size, x, y, orientation)
        if ship.orientation == 0:
            for i in range(ship.x, ship.x + ship.size):
                self.cells[i][ship.y].set_ship()
        else:
            for i in range(ship.y, ship.y + ship.size):
                self.cells[ship.x][i].set_ship()

        self._ships.append(ship)
        self.draw_ship(ship)

    @property
    def ships(self):
        result = [0] * 5
        for ship in self._ships:
            result[ship.size] += 1
        return result

    def draw_ship(self, ship):
        self.canvas.create_rectangle(
            self.x + self.cell_size * ship.x,
            self.y + self.cell_size * ship.y,
            self.x + self.cell_size * (ship.x + (ship.size if ship.orientation == 0 else 1)),
            self.y + self.cell_size * (ship.y + (ship.size if ship.orientation == 1 else 1)),
            fill='red'
        )
        print(
            self.x, self.y, self.cell_size, ship.x, ship.y, ship.size, ship.orientation, '\n',
            self.x + self.cell_size * ship.x,
            self.y + self.cell_size * ship.y,
            self.x + self.cell_size * (ship.x + (ship.size if ship.orientation == 0 else 1)),
            self.y + self.cell_size * (ship.y + (ship.size if ship.orientation == 1 else 1)),
        )
