"""Консольный интерфейс проекта."""

import re

MENU = """1. Показать отчёт
2. Добавить запись
3. Найти по региону
0. Выход"""

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_choice(raw, allowed):
    """Вернуть номер пункта или None."""
    # TODO: уберите пробелы, преобразуйте в int с обработкой ValueError
    # и проверьте, что номер входит в allowed.
    return None


def parse_amount(raw):
    """Вернуть неотрицательную сумму или None."""
    # TODO: уберите пробелы, преобразуйте в float,
    # отклоните пустую строку, запятую и отрицательные числа.
    return None


def read_choice(allowed):
    """Читать пункт меню, пока не получится корректный."""
    while True:
        raw = input("Пункт: ")
        value = parse_choice(raw, allowed)
        if value is not None:
            return value
        print("Неверный пункт. Повторите.")


def read_amount(prompt):
    """Читать сумму, пока не получится корректная."""
    while True:
        raw = input(prompt)
        value = parse_amount(raw)
        if value is not None:
            return value
        print("Нужна неотрицательная сумма с точкой.")


def read_date(prompt):
    """Читать дату в формате ГГГГ-ММ-ДД."""
    while True:
        raw = input(prompt).strip()
        if DATE.fullmatch(raw):
            return raw
        print("Дата должна быть в формате ГГГГ-ММ-ДД.")
