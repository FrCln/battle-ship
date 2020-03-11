from tkinter import *

from field import SetField


SIZE = 40
job = None


def on_close():
    window.after_cancel(job)
    window.destroy()


def update_labels():
    global job
    ships = field.ships
    for i in range(1, 5):
        labels[i].configure(text=f'{i}-палубных: {ships[i]}')
    if ships != field.available:
        job = window.after(50, update_labels)


def start_game():
    ships = field.ships
    if ships == field.available:
        on_close()
    else:
        window.bell()


window = Tk()
window.title('Battle Ship')

canvas = Canvas(window, width=SIZE * 15, height=SIZE * 15, bg='white')
canvas.grid(row=0, column=0, rowspan=4, columnspan=4)

field = SetField(canvas, SIZE * 5 // 2, SIZE * 5 // 2, SIZE)

labels = {}
for i in range(1, 5):
    labels[i] = Label(window)
    labels[i].grid(row=4, column=i - 1)

button_ok = Button(window, text='Начать игру', command=start_game)
button_ok.grid(row=5, column=0, columnspan=4)

job = window.after(50, update_labels)
window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()
