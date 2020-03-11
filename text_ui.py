from ship import Ship
from field import Field
from cell import Cell

field = Field()


def get_neibourhood(field, size, x, y, orientation):
    if orientation == 'x':
        ship_coord = {(i, y) for i in range(x, x + size)}
    else:
        ship_coord = {(x, i) for i in range(y, y + size)}
    near_coord = set()
    for point in ship_coord:
        near_point = {
            (i, j) for i in range(point[0] - 1, point[0] + 2)
            for j in range(point[1] - 1, point[1] + 2)
            if 0 <= i < field.size[0] and
            0 <= j < field.size[1]
        }
        near_coord |= near_point
    return near_coord | ship_coord


def check_cell(field, size, x, y, orientation):
    if not 0 <= x < field.size[0]:
        return False
    if not 0 <= y < field.size[1]:
        return False
    if orientation == 'x' and x >= field.size[0] - size:
        return False
    if orientation == 'y' and y >= field.size[1] - size:
        return False
    for point in get_neibourhood(field, size, x, y, orientation):
        if not field.empty(*point):
            return False
    return True


def create_ship(field, size, x, y, orientation):
    ship = Ship(size, x, y, orientation)
    field.set_ship(ship)


def player_place():
    ship_count = 10
    ships = [0, 4, 3, 2, 1]
    while ship_count > 0:
        print("У вас есть:", ships[4], "четырёхпалубных,", ships[3], "трёхпалубных,", ships[2], "двухпалубных,", ships[1], "однопалубных.")
        size = int(input("Введите размер коробля: "))
        if size > 4 or size < 1 or ships[size] == 0:
            print("Ваш размер не должен превышать 4 и 1, а также кол-во кораблей не может уйти в минус.")
            continue
        x = int(input("Введите первую точку постановки коробля: "))
        y = int(input("Введите вторкю точку постановки коробля: "))
        orientation = input("Введите сторону,в которую будет смотреть корабль(x или y): ")
        if not check_cell(field, size, x, y, orientation):
            print('Занято')
            continue
        create_ship(field, size, x, y, orientation)
        ships[size] -= 1
        ship_count -= 1
        print(field)
        print()

player_place()

