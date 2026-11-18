"""Практика 1. Первая программа и расчёты.

Заполните блоки TODO. Программа должна запускаться командой
    python starter.py
и печатать результаты пяти задач.
"""

print("Практика 1. Первая программа и расчёты")
print("=" * 40)

# Задача 1. Площадь и периметр прямоугольника.
print("\nЗадача 1. Прямоугольник")
a = float(input("Сторона a: "))
b = float(input("Сторона b: "))
# TODO: посчитайте area и perimeter.
area = 0.0
perimeter = 0.0
print(f"Площадь: {area:.2f}")
print(f"Периметр: {perimeter:.2f}")

# Задача 2. Перевод температуры.
print("\nЗадача 2. Температура")
c = float(input("Температура в Цельсиях: "))
# TODO: посчитайте fahrenheit и kelvin.
fahrenheit = 0.0
kelvin = 0.0
print(f"Фаренгейт: {fahrenheit:.2f}")
print(f"Кельвин: {kelvin:.2f}")

# Задача 3. Кассовый чек.
print("\nЗадача 3. Кассовый чек")
name = input("Товар: ")
price = float(input("Цена: "))
quantity = int(input("Количество: "))
discount = float(input("Скидка, %: "))
# TODO: посчитайте subtotal, discount_value и total.
subtotal = 0.0
discount_value = 0.0
total = 0.0
print(f"Товар: {name}")
print(f"Сумма: {subtotal:.2f}")
print(f"Скидка: {discount_value:.2f}")
print(f"Итого: {total:.2f}")

# Задача 4. Три покупки.
print("\nЗадача 4. Три покупки")
# Введите данные из data.md. Для каждой покупки посчитайте итог.
name1 = input("Товар 1: ")
price1 = float(input("Цена 1: "))
qty1 = int(input("Количество 1: "))
disc1 = float(input("Скидка 1, %: "))

name2 = input("Товар 2: ")
price2 = float(input("Цена 2: "))
qty2 = int(input("Количество 2: "))
disc2 = float(input("Скидка 2, %: "))

name3 = input("Товар 3: ")
price3 = float(input("Цена 3: "))
qty3 = int(input("Количество 3: "))
disc3 = float(input("Скидка 3, %: "))

# TODO: посчитайте total1, total2, total3, grand_total и average.
total1 = 0.0
total2 = 0.0
total3 = 0.0
grand_total = 0.0
average = 0.0
print(f"{name1}: {total1:.2f}")
print(f"{name2}: {total2:.2f}")
print(f"{name3}: {total3:.2f}")
print(f"Общая сумма: {grand_total:.2f}")
print(f"Средний чек: {average:.2f}")

# Задача 5. Сравнение упаковок.
print("\nЗадача 5. Сравнение упаковок")
grams_a = 1200
price_a = 540.0
grams_b = 900
price_b = 432.0
# TODO: посчитайте price_per_kg_a и price_per_kg_b.
price_per_kg_a = 0.0
price_per_kg_b = 0.0
print(f"Упаковка A: {price_per_kg_a:.2f} за кг")
print(f"Упаковка B: {price_per_kg_b:.2f} за кг")
print(f"Меньшая цена за кг: {min(price_per_kg_a, price_per_kg_b):.2f}")
