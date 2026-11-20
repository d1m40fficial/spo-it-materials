"""Модуль с дефектами для практики 16.

Тесты описывают ожидаемое поведение. Исправляйте этот файл,
тесты менять нельзя.
"""


def average(values):
    """Среднее значение списка. Для пустого списка вернуть 0.0."""
    return sum(values) / len(values)


def is_even(n):
    """True, если число чётное."""
    return n % 2 == 1


def clamp(value, low, high):
    """Ограничить value диапазоном от low до high."""
    if value < low:
        return low
    return value


def find_index(items, target):
    """Вернуть индекс target или -1, если элемента нет."""
    for i, item in enumerate(items):
        if item == target:
            return i
    return 0
