"""Практика 18. Выгрузка отчёта в CSV.

Заполните блоки TODO. Программа запускается командой
    python starter.py
и создаёт report.csv в текущей папке.
"""

import csv

ITEMS = [
    {"name": "Кружка", "price": 640, "quantity": 3},
    {"name": "Блюдце", "price": 420, "quantity": 2},
    {"name": "Коробка", "price": 40, "quantity": 10},
    {"name": "Чайник", "price": 1250, "quantity": 1},
]

FILE = "report.csv"

print("Практика 18. Выгрузка отчёта в CSV")
print("=" * 44)


def total_of(item):
    # TODO: верните стоимость позиции.
    return 0.0


with open(FILE, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=";")

    # TODO: запишите заголовок name;price;quantity;total.
    pass

    # TODO: запишите строку для каждого товара.
    grand_total = 0.0

    # TODO: запишите итоговую строку.

print("Файл записан:", FILE)
print(f"Итог: {grand_total:.2f}")
