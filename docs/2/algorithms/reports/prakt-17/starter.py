"""Практика 17. Импорт каталога из JSON.

Заполните блоки TODO. Программа запускается командой
    python starter.py
и читает файл catalog.json из текущей папки.
"""

import json

FILE = "catalog.json"


def is_valid(item):
    """Проверить обязательные поля и значения."""
    # TODO: проверьте name, price, quantity, category.
    return True


def load_catalog(path):
    """Прочитать JSON и вернуть два списка: принятые и отброшенные."""
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)

    accepted = []
    rejected = []

    # TODO: проверьте, что raw это список.
    # TODO: пройдите по записям и разделите их на accepted и rejected.
    for item in raw:
        if is_valid(item):
            accepted.append(item)
        else:
            rejected.append(item)

    return accepted, rejected


print("Практика 17. Импорт каталога из JSON")
print("=" * 44)

accepted, rejected = load_catalog(FILE)

print("Принято:", len(accepted))
print("Отброшено:", len(rejected))

# TODO: посчитайте общую стоимость, самую дорогую позицию и среднюю цену.
total = 0.0
most_expensive = None
average_price = 0.0

print(f"Общая стоимость: {total:.2f}")
print("Самая дорогая:", most_expensive)
print(f"Средняя цена: {average_price:.2f}")

# TODO: соберите записи категории "посуда".
dishes = []
print("Посуда:", len(dishes))

print("\nОтброшенные записи")
for item in rejected:
    print(" -", item)
