"""Практика 22. Расписание задач жадным методом.

Заполните блоки TODO. Программа запускается командой
    python starter.py
и выбирает максимальное число непересекающихся задач.
"""

TASKS = [
    ("A", 9, 11),
    ("B", 10, 12),
    ("C", 11, 13),
    ("D", 12, 14),
    ("E", 13, 15),
    ("F", 14, 16),
    ("G", 15, 17),
]

print("Практика 22. Расписание задач")
print("=" * 44)


def show(title, tasks):
    print(f"\n{title}")
    for name, start, end in tasks:
        print(f"{name}: {start:>2} - {end:>2}")


def select(tasks):
    """Вернуть список выбранных задач (name, start, end)."""
    # TODO: отсортируйте по окончанию и выберите совместимые.
    return []


def load(tasks):
    # TODO: сумма длительностей.
    return 0


def no_overlaps(tasks):
    # TODO: проверьте, что соседние задачи не пересекаются.
    return False


show("Все задачи", TASKS)

chosen = select(TASKS)
show("Выбрано", chosen)

print("\nЗадач:", len(chosen))
print("Загрузка:", load(chosen))
print("Без пересечений:", no_overlaps(chosen))

# TODO: постройте расписание с сортировкой по началу и сравните число задач.
by_start = []
print("По началу выбрано:", len(by_start))
