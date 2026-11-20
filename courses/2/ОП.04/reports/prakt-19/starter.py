"""Практика 19. Таблица мест в аудитории.

Заполните блоки TODO. Программа запускается командой
    python starter.py
и работает со схемой мест 5 x 6.
"""

SEATS = [
    [1, 1, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 1],
]


def show(seats):
    for row in seats:
        # TODO: соберите строку из # и . и напечатайте её.
        print("")


def count_free(seats):
    # TODO: посчитайте нули.
    return 0


def row_occupied(seats):
    # TODO: верните список сумм по каждой строке.
    return []


def first_free(seats):
    # TODO: верните (row, col) первого нуля или None.
    return None


def take(seats, row, col):
    # TODO: проверьте границы и занятость, поставьте 1.
    return False


print("Практика 19. Таблица мест в аудитории")
print("=" * 44)

print("\nСхема")
show(SEATS)

free = count_free(SEATS)
print("\nСвободных мест:", free)
print("Всего мест:", len(SEATS) * len(SEATS[0]))
print("Занято по рядам:", row_occupied(SEATS))

place = first_free(SEATS)
print("Первое свободное:", place)

if place:
    ok = take(SEATS, place[0], place[1])
    print("Место занято:", ok)
    print("Свободных после:", count_free(SEATS))

print("\nСхема после")
show(SEATS)

print("\nПроверки")
print("Повторное занятие:", take(SEATS, place[0], place[1]) if place else "нет места")
print("Выход за границу:", take(SEATS, 10, 10))
