from tkinter import *

from ai import AI
from field import PlayerField, EnemyField
from ship import Ship

player_ships = [
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

SIZE = 40
job = None


def on_close():
    window.after_cancel(job)
    window.destroy()


def check_turn():
    global job
    if comp_field.blocked:
        if not comp_field.alive():
            print('Ты победил!')
            return
        ai.comp_turn()
        if not player_field.alive():
            print('Я победил!')
            return
        comp_field.unblock()
    job = window.after(50, check_turn)


window = Tk()
window.title('Battle Ship')

canvas = Canvas(window, width=SIZE * 30, height=SIZE * 15, bg='white')
canvas.grid(row=0, column=0, rowspan=4, columnspan=4)

player_field = PlayerField(canvas, SIZE * 5 // 2, SIZE * 5 // 2, SIZE)
comp_field = EnemyField(canvas, SIZE * 15, SIZE * 5 // 2, SIZE)

ai = AI(player_field)

for ship in player_ships:
    player_field.create_ship(ship)

for ship in comp_ships:
    comp_field.create_ship(ship, False)

job = window.after(50, check_turn)
window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()
