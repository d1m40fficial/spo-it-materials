"""Практика 6. Разбиение расчёта на части.

Заполните блоки TODO. Программа запускается командой
    python starter.py
и печатает чеки для четырёх заказов.
"""

from pricing import order_total, delivery_cost

ORDERS = [
    {"number": 1, "name": "Кружка", "price": 640, "quantity": 3, "discount": 10, "zone": "город"},
    {"number": 2, "name": "Блюдце", "price": 420, "quantity": 2, "discount": 0, "zone": "город"},
    {"number": 3, "name": "Коробка", "price": 40, "quantity": 10, "discount": 5, "zone": "область"},
    {"number": 4, "name": "Стол", "price": 4500, "quantity": 1, "discount": 0, "zone": "город"},
]

print("Практика 6. Разбиение расчёта на части")
print("=" * 44)


def format_receipt(number, name, total, delivery):
    """Собрать строку чека."""
    # TODO: верните строку вида
    # "Заказ 1. Кружка: 1728.00 + доставка 300.00 = 2028.00"
    return ""


def main():
    grand_total = 0.0
    for order in ORDERS:
        # TODO: вызовите order_total и delivery_cost,
        # затем напечатайте чек через format_receipt.
        total = 0.0
        delivery = 0.0
        print(format_receipt(order["number"], order["name"], total, delivery))
        grand_total += total + delivery
    print(f"Итого по всем заказам: {grand_total:.2f}")


if __name__ == "__main__":
    main()
