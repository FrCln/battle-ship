from abc import ABC, abstractmethod
from tkinter import *

from cell import Cell
from ship import Ship
from field import Field

class AbstractUI(ABC):
    def __init__(self, field: Field, canvas: Canvas, x, y, cell_size):
        self.field = field
        self.canvas = canvas
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.draw_field()
        self.bind()

    def bind(self):
        self.canvas.bind('<Button-1>', self.click_field)

    def draw_field(self):
        self.rect = self.canvas.create_rectangle(
            self.x,
            self.y,
            self.x + self.cell_size * self.field.shape[0],
            self.y + self.cell_size * self.field.shape[1],
            fill='cyan'
        )

        for i in range(1, self.field.shape[0]):
            self.canvas.create_line(
                self.x + i * self.cell_size,
                self.y,
                self.x + i * self.cell_size,
                self.y + self.cell_size * self.field.shape[1]
            )

        for i in range(1, self.field.shape[1]):
            self.canvas.create_line(
                self.x,
                self.y + i * self.cell_size,
                self.x + self.cell_size * self.field.shape[0],
                self.y + i * self.cell_size
            )

        for i in range(self.field.shape[1]):
            self.canvas.create_text(
                self.x - self.cell_size / 2,
                self.y + self.cell_size / 2 + i * self.cell_size,
                text=chr(65 + i)
            )

        for i in range(self.field.shape[0]):
            self.canvas.create_text(
                self.x + self.cell_size / 2 + i * self.cell_size,
                self.y - self.cell_size / 2,
                text=str(i + 1)
            )

    @abstractmethod
    def click_action(self, x, y):
        pass

    def click_field(self, event):
        x, y = event.x, event.y
        if self.rect in self.canvas.find_overlapping(x, y, x, y):
            x = (x - self.x) // self.cell_size
            y = (y - self.y) // self.cell_size
            self.click_action(x, y)

    def draw_ship(self, ship: Ship, fill='red'):
        self.canvas.create_rectangle(
            self.x + self.cell_size * ship.x,
            self.y + self.cell_size * ship.y,
            self.x + self.cell_size * (ship.x + (ship.size if ship.orientation == 0 else 1)),
            self.y + self.cell_size * (ship.y + (ship.size if ship.orientation == 1 else 1)),
            fill=fill
        )

    def draw_ships(self):
        for ship in self.field.ships:
            self.draw_ship(ship)

    def miss(self, x, y):
        self.canvas.create_line(
            self.x + x * self.cell_size,
            self.y + y * self.cell_size,
            self.x + (x + 1) * self.cell_size,
            self.y + (y + 1) * self.cell_size
        )
        self.canvas.create_line(
            self.x + (x + 1) * self.cell_size,
            self.y + y * self.cell_size,
            self.x + x * self.cell_size,
            self.y + (y + 1) * self.cell_size
        )

    def hit(self, x, y):
        ship = self.field.cells_dict[(x, y)]
        if ship.dead:
            self.kill(ship)
        else:
            self.canvas.create_rectangle(
                self.x + self.cell_size * x,
                self.y + self.cell_size * y,
                self.x + self.cell_size * (x + 1),
                self.y + self.cell_size * (y + 1),
                fill='#770000'
            )

    def kill(self, ship):
        self.draw_ship(ship, 'black')
        for x, y in self.field.neighborhood(ship):
            if self.field.cells[x][y].empty:
                self.field.miss(x, y)
                self.miss(x, y)


class SetField(AbstractUI):
    available = [0, 4, 3, 2, 1]

    def click_action(self, x, y):
        if self.field.num_ships == self.available:
            return
        if not self.field.empty(x, y):
            return

        def on_close():
            self.bind()
            window.destroy()
        def click():
            size = ship_size.get()
            ship = Ship(size, x, y, orientation.get())
            if self.field.num_ships[size] < self.available[size] and \
            self.check_cell(ship):
                self.field.create_ship(ship)
                self.draw_ship(ship)
                window.destroy()
                self.canvas.bind('<Button-1>', self.click_field)
            else:
                window.bell()
        window = Tk()
        window.title('Выбор корабля')
        window.protocol("WM_DELETE_WINDOW", on_close)
        # FIXIT
        window.focus_set()
        self.canvas.unbind('<Button-1>')
        _, root_x, root_y = self.canvas.winfo_toplevel().wm_geometry().split('+')
        win_x = int(root_x) + self.x + (x + 1) * self.cell_size
        win_y = int(root_y) + self.y + (y + 1) * self.cell_size
        window.geometry("+{}+{}".format(win_x, win_y))
        ship_size = IntVar(window)
        ship_size.set(1)
        for i in range(1, 5):
            r = Radiobutton(window, text=f'{i}-палубный', variable=ship_size, value=i)
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

    def check_cell(self, ship):
        if not 0 <= ship.x < self.field.shape[0]:
            return False
        if not 0 <= ship.y < self.field.shape[1]:
            return False
        if ship.orientation == 0 and ship.x > self.field.shape[0] - ship.size:
            return False
        if ship.orientation == 1 and ship.y > self.field.shape[1] - ship.size:
            return False
        for point in self.field.neighborhood(ship):
            if not self.field.empty(*point):
                return False
        return True


class PlayerField(AbstractUI):
    def click_action(self, event):
        pass


class EnemyField(AbstractUI):
    blocked = False
    def click_action(self, x, y):
        if self.field.empty(x, y):
            self.field.miss(x, y)
            self.miss(x, y)
            self.block()
        elif self.field.cells[x][y].ship():
            self.field.hit(x, y)
            self.hit(x, y)
            if not self.field.alive():
                self.block()

    def block(self):
        self.blocked = True
        self.canvas.unbind('<Button-1>')

    def unblock(self):
        self.blocked = False
        self.bind()

