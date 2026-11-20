"""Практика 25. Конвейер обработки данных.

Заполните блоки TODO. Программа запускается командой
    python starter.py
и проводит заказы через цепочку генераторов.
"""

ORDERS = [
    {"id": 1, "status": "оплачен", "amount": 1200},
    {"id": 2, "status": "отменён", "amount": 800},
    {"id": 3, "status": "оплачен", "amount": 2500},
    {"id": 4, "status": "оплачен", "amount": 400},
    {"id": 5, "status": "ожидает", "amount": 900},
    {"id": 6, "status": "оплачен", "amount": 1700},
]

print("Практика 25. Конвейер обработки данных")
print("=" * 44)


def paid(orders):
    # TODO: пропускайте только оплаченные заказы.
    for order in orders:
        yield order


def above(orders, limit):
    # TODO: пропускайте заказы с суммой не меньше limit.
    for order in orders:
        yield order


def with_vat(orders):
    # TODO: добавьте поле vat.
    for order in orders:
        yield order


def first_n(items, n):
    # TODO: выдайте не больше n элементов.
    for item in items:
        yield item


stream = first_n(above(paid(ORDERS), 500), 3)
print("\nПервые три записи")
for order in stream:
    print(order)

# TODO: соберите конвейер заново и посчитайте количество и сумму.
count = 0
total = 0.0
print("\nКоличество:", count)
print(f"Сумма: {total:.2f}")

print("\nПовторный проход по тому же генератору")
print(list(stream))
