from tkinter import *

from ai import AI
from field import Field
from gui import SetField, PlayerField, EnemyField
from ship import Ship

SIZE = 40
job = None


def set_field():
    def on_close():
        window.after_cancel(job)
        window.destroy()

    def update_labels():
        global job
        ships = field.ships
        for i in range(1, 5):
            labels[i].configure(text=f'{i}-палубных: {ships[i]}')
        if ships != sf.available:
            job = window.after(50, update_labels)

    def start_game():
        ships = field.ships
        if ships == sf.available:
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
    return field


def game(player_field, comp_field):
    def on_close():
        window.after_cancel(job)
        window.destroy()

    def check_player_field(x, y):
        if player_field.cells[x][y].ship():
            player_field.hit(x, y)
            pf.hit(x, y)
            return True
        else:
            player_field.miss(x, y)
            pf.miss(x, y)
            return False

    def check_turn():
        global job
        if ef.blocked:
            if not comp_field.alive():
                print('Ты победил!')
                return
            x, y = ai.comp_turn()
            while check_player_field(x, y):
                x, y = ai.comp_turn()
            if not player_field.alive():
                print('Я победил!')
                return
            ef.unblock()
        job = window.after(50, check_turn)

    window = Tk()
    window.title('Battle Ship')

    canvas = Canvas(window, width=SIZE * 30, height=SIZE * 15, bg='white')
    canvas.grid(row=0, column=0, rowspan=4, columnspan=4)

    pf = PlayerField(player_field, canvas, SIZE * 5 // 2, SIZE * 5 // 2, SIZE)
    pf.draw_ships()
    ef = EnemyField(comp_field, canvas, SIZE * 15, SIZE * 5 // 2, SIZE)

    ai = AI(player_field)

    job = window.after(50, check_turn)
    window.protocol("WM_DELETE_WINDOW", on_close)
    window.mainloop()


def generate_field():
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


def main():
    player_field = generate_field()
    comp_field = generate_field()
    game(player_field, comp_field)


if __name__ == '__main__':
    main()
