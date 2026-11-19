"""Практика 11. Упорядочивание записей каталога.

Заполните блоки TODO. Программа запускается командой
    python starter.py
и печатает каталог в разных порядках.
"""

CATALOG = [
    {"name": "Кружка", "price": 640, "quantity": 3},
    {"name": "Блюдце", "price": 420, "quantity": 2},
    {"name": "Коробка", "price": 40, "quantity": 10},
    {"name": "Чайник", "price": 1250, "quantity": 1},
    {"name": "Ложка", "price": 90, "quantity": 6},
]


def show(title, records):
    print(f"\n{title}")
    for item in records:
        total = item["price"] * item["quantity"]
        print(f'{item["name"]:<10} {item["price"]:>6} x {item["quantity"]:<2} = {total:>7.2f}')


def binary_search(records, target):
    """Вернуть индекс записи по названию или -1."""
    # TODO: реализуйте бинарный поиск по полю name.
    return -1


print("Практика 11. Упорядочивание записей каталога")
print("=" * 44)

show("Исходный порядок", CATALOG)

# TODO: отсортируйте по цене.
by_price = []
show("По цене", by_price)

# TODO: отсортируйте по названию.
by_name = []
show("По названию", by_name)

# TODO: отсортируйте по стоимости по убыванию.
by_total = []
show("По стоимости", by_total)

for target in ("Ложка", "Кружка", "Ваза"):
    index = binary_search(by_name, target)
    if index >= 0:
        print(f'{target}: индекс {index}')
    else:
        print(f"{target}: не найдено")
