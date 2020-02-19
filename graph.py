from tkinter import *

from field import Field


SIZE = 40


def update_labels(labels, ships):
    for i in range(1, 5):
        labels[i].configure(text=f'{i}-палубных: {ships[i]}')


window = Tk()
window.title('Battle Ship')

canvas = Canvas(window, width=SIZE * 15, height=SIZE * 15, bg='white')
canvas.grid(row=0, column=0, rowspan=4, columnspan=4)

field = Field(canvas, SIZE * 2.5, SIZE * 2.5, SIZE)

ships = [0, 4, 3, 2, 1]
labels = {}
for i in range(1, 5):
    labels[i] = Label(window, text=f'{i}-палубных: {ships[i]}')
    labels[i].grid(row=4, column=i - 1)

canvas.bind('<Button-1>', field.click_field)

window.mainloop()
