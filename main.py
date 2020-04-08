from random import choice
from tkinter import *
import tkinter.messagebox as mb

from ai import AI
from field import Field
from gui import SetField, PlayerField, EnemyField
from ship import Ship

SIZE = 40
job = None
in_game = False


def set_field():
    global job

    def on_close():
        window.after_cancel(job)
        window.destroy()

    def update_labels():
        global job
        ships = field.num_ships
        for i in range(1, 5):
            labels[i].configure(text=f'{i}-палубных: {ships[i]}')
        if ships != sf.available:
            job = window.after(100, update_labels)

    def start_game():
        global in_game
        ships = field.num_ships
        if ships == sf.available:
            in_game = True
            on_close()
        else:
            window.bell()

    window = Tk()
    window.title('Battle Ship')

    canvas = Canvas(window, width=SIZE * 15, height=SIZE * 15, bg='white')
    canvas.grid(row=0, column=0, rowspan=4, columnspan=4)

    field = Field()
    sf = SetField(field, canvas, SIZE * 5 // 2, SIZE * 5 // 2, SIZE)

    labels = {}
    for i in range(1, 5):
        labels[i] = Label(window)
        labels[i].grid(row=4, column=i - 1)

    button_ok = Button(window, text='Начать игру', command=start_game)
    button_ok.grid(row=5, column=0, columnspan=4)

    job = window.after(50, update_labels)
    window.protocol("WM_DELETE_WINDOW", on_close)
    window.mainloop()
    if in_game:
        return field


def game(player_field, comp_field):
    global job
    def on_close():
        global in_game
        in_game = False
        window.after_cancel(job)
        window.destroy()

    def check_player_field(x, y):
        if player_field.cells[x][y].ship():
            player_field.hit(x, y)
            pf.hit(x, y)
            if player_field.cells_dict[(x, y)].dead:
                return 2
            return 1
        else:
            player_field.miss(x, y)
            pf.miss(x, y)
            return 0

    def check_turn():
        global job
        if ef.blocked:
            if not player_field.alive():
                ai.kill(x, y)
                mb.showinfo('Ура!', 'Я победил!')
                return
            if not comp_field.alive():
                mb.showinfo('Поздравляю!', 'Ты победил!')
                return

            x, y = ai.make_turn()
            result = check_player_field(x, y)
            if result == 1:
                ai.hit(x, y)
            elif result == 2:
                ai.kill(x, y)
            else:
                ai.miss(x, y)
                ef.unblock()

        job = window.after(50, check_turn)

    def restart_game():
        window.after_cancel(job)
        window.destroy()

    window = Tk()
    window.title('Battle Ship')

    canvas = Canvas(window, width=SIZE * 30, height=SIZE * 15, bg='white')
    canvas.grid(row=0, column=0, rowspan=4, columnspan=4)

    restart_button = Button(window, text='Начать заново', command=restart_game)
    quit_button = Button(window, text='Выйти', command=on_close)
    restart_button.grid(row=4, column=0, columnspan=2)
    quit_button.grid(row=4, column=2, columnspan=2)

    pf = PlayerField(player_field, canvas, SIZE * 5 // 2, SIZE * 5 // 2, SIZE)
    pf.draw_ships()
    ef = EnemyField(comp_field, canvas, SIZE * 15, SIZE * 5 // 2, SIZE)

    ai = AI()

    job = window.after(50, check_turn)
    window.protocol("WM_DELETE_WINDOW", on_close)
    window.mainloop()


def generate_test_field():
    comp_field = Field()
    comp_ships = [
        Ship(4, 0, 0, 0),
        Ship(3, 0, 2, 0),
        Ship(3, 0, 4, 0),
        Ship(2, 0, 6, 0),
        Ship(2, 0, 8, 0),
        Ship(2, 6, 0, 0),
        Ship(2, 6, 2, 0),
        Ship(1, 4, 4, 0),
        Ship(1, 6, 6, 0),
        Ship(1, 6, 4, 0),
        Ship(1, 6, 8, 0)
    ]
    for ship in comp_ships:
        comp_field.create_ship(ship)

    return comp_field


def generate_random_field():
    cells = [(x, y) for x in range(10) for y in range(10)]
    f = Field()
    sizes = [4] + [3] * 2 + [2] * 3 + [1] * 4
    for size in sizes:
        while True:
            ship = Ship(size, *choice(cells), choice((0, 1)))
            if f.check_cell(ship):
                f.create_ship(ship)
                break
    return f


def main():
    while True:
        # player_field = set_field()
        player_field = generate_test_field()
        if player_field:
            comp_field = generate_test_field()
            game(player_field, comp_field)
        if not in_game:
            break


if __name__ == '__main__':
    main()
