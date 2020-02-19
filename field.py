from tkinter import *

from cell import Cell
from ship import Ship


class Field:
    def __init__(self, canvas, x, y, cell_size, draw=True, shape=(10, 10)):
        self.cells = [
            [Cell(x, y) for x in range(shape[0])]
            for y in range(shape[1])
        ]
        self.ships = []
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

    def set_ship(self, ship):
        if ship.orientation == 'x':
            for i in range(ship.x, ship.x + ship.shape):
                self.cells[i][ship.y].set_ship()
        else:
            for i in range(ship.y, ship.y + ship.shape):
                self.cells[ship.x][i].set_ship()

        self.ships.append(ship)

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
            print(x, y)
