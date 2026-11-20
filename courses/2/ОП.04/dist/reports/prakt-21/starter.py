"""Практика 21. Оптимальная стоимость по шагам.

Заполните блоки TODO. Программа запускается командой
    python starter.py
и ищет минимальный путь по сетке.
"""

GRID = [
    [1, 3, 1, 2],
    [1, 5, 1, 3],
    [4, 2, 1, 1],
]

print("Практика 21. Оптимальная стоимость по шагам")
print("=" * 44)


def show(grid):
    for row in grid:
        print(" ".join(f"{value:>3}" for value in row))


def build_dp(grid):
    """Вернуть таблицу минимальных стоимостей."""
    rows = len(grid)
    cols = len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    # TODO: заполните базу, первую строку, первый столбец и остальные клетки.
    return dp


def build_path(dp):
    """Вернуть маршрут от начала к концу в виде списка (r, c)."""
    # TODO: идите от конца к началу и разверните список.
    return []


def greedy_path(grid):
    """Жадный проход: всегда идём в меньшую соседнюю клетку."""
    # TODO: реализуйте жадный выбор.
    return []


print("\nСетка")
show(GRID)

dp = build_dp(GRID)
print("\nТаблица dp")
show(dp)

print("\nМинимальная стоимость:", dp[-1][-1] if dp else None)

path = build_path(dp)
print("Маршрут:", path)

greedy = greedy_path(GRID)
print("Жадный маршрут:", greedy)
