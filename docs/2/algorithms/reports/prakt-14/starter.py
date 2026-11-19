"""Практика 14. Иерархия фигур.

Заполните блоки TODO. Программа запускается командой
    python starter.py
и обходит список фигур.
"""

import math


class Shape:
    def __init__(self, name):
        self.name = name

    def area(self):
        raise NotImplementedError("наследник должен реализовать area")

    def perimeter(self):
        raise NotImplementedError("наследник должен реализовать perimeter")

    def __str__(self):
        return f"{self.name}: {self.area():.2f}"


class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Круг")
        self.radius = radius

    def area(self):
        # TODO: площадь круга.
        return 0.0

    def perimeter(self):
        # TODO: длина окружности.
        return 0.0


class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("Прямоугольник")
        self.width = width
        self.height = height

    def area(self):
        # TODO: площадь прямоугольника.
        return 0.0

    def perimeter(self):
        # TODO: периметр прямоугольника.
        return 0.0


class Triangle(Shape):
    def __init__(self, a, b, c):
        super().__init__("Треугольник")
        self.a = a
        self.b = b
        self.c = c

    def area(self):
        # TODO: проверьте стороны и посчитайте площадь по формуле Герона.
        return 0.0

    def perimeter(self):
        # TODO: периметр треугольника.
        return 0.0


print("Практика 14. Иерархия фигур")
print("=" * 44)

shapes = [Circle(3), Rectangle(4, 5), Triangle(3, 4, 5)]

print("Фигуры")
for shape in shapes:
    print(shape)

# TODO: посчитайте общую площадь.
total = 0.0
print(f"\nОбщая площадь: {total:.2f}")

# TODO: отсортируйте по площади и найдите максимум.
by_area = []
largest = None

print("\nПо возрастанию площади")
for shape in by_area:
    print(shape)

print("\nСамая большая:", largest)

print("\nПроверки")
print("Круг является Shape:", isinstance(shapes[0], Shape))
print("Площадь треугольника 3-4-5:", shapes[2].area())
