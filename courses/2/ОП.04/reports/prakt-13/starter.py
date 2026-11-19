"""Практика 13. Модель предметной области в классах.

Заполните блоки TODO. Программа запускается командой
    python starter.py
и показывает состояние товаров, заказа и склада.
"""


class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def total(self):
        # TODO: верните стоимость позиции.
        return 0.0

    def __str__(self):
        # TODO: верните строку с названием и стоимостью.
        return self.name


class Order:
    def __init__(self, number):
        self.number = number
        # TODO: создайте пустой список позиций.
        self.items = []

    def add(self, product):
        # TODO: добавьте позицию в заказ.
        pass

    def total(self):
        # TODO: сложите стоимости позиций.
        return 0.0

    def count(self):
        # TODO: верните число позиций.
        return 0


class Warehouse:
    def __init__(self):
        self.stock = {}

    def receive(self, name, quantity):
        # TODO: увеличьте остаток.
        pass

    def issue(self, name, quantity):
        # TODO: уменьшите остаток, если товара хватает.
        # Верните True при успехе и False при отказе.
        return False

    def report(self):
        for name in sorted(self.stock):
            print(f"{name}: {self.stock[name]}")


print("Практика 13. Модель предметной области в классах")
print("=" * 44)

cup = Product("Кружка", 640, 3)
plate = Product("Блюдце", 420, 2)
box = Product("Коробка", 40, 10)

print(cup)
print(plate)
print(box)

order = Order(1)
order.add(Product("Кружка", 640, 2))
order.add(Product("Блюдце", 420, 1))

print("\nЗаказ", order.number)
print("Позиций:", order.count())
print(f"Итого: {order.total():.2f}")

warehouse = Warehouse()
warehouse.receive("Кружка", 10)
warehouse.receive("Блюдце", 5)

print("\nСклад")
warehouse.report()

print("\nВыдача 4 кружек:", warehouse.issue("Кружка", 4))
print("Выдача 20 кружек:", warehouse.issue("Кружка", 20))
print("Остаток кружек:", warehouse.stock.get("Кружка"))

print("\nПроверки")
print("Количество не отрицательно:", cup.quantity >= 0)
print("Итог заказа сходится:", abs(order.total() - sum(p.total() for p in order.items)) < 0.01)
print("Остаток не отрицателен:", all(v >= 0 for v in warehouse.stock.values()))
