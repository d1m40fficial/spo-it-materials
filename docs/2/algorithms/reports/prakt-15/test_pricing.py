"""Практика 15. Тесты для pricing.py.

Запуск:
    python -m unittest test_pricing.py

Заполните тесты. Один тест проверяет одно поведение.
"""

import unittest

from pricing import discount, delivery, order_total


class TestDiscount(unittest.TestCase):
    def test_ten_percent(self):
        # TODO: проверьте discount(1000, 10) == 900.
        pass

    def test_zero_percent(self):
        # TODO: проверьте, что скидка 0 не меняет сумму.
        pass

    def test_full_discount(self):
        # TODO: проверьте, что скидка 100 даёт 0.
        pass

    def test_invalid_percent(self):
        # TODO: проверьте ValueError при скидке больше 100.
        pass


class TestDelivery(unittest.TestCase):
    def test_city(self):
        # TODO: доставка в город при сумме меньше 3000.
        pass

    def test_free_from_3000(self):
        # TODO: доставка бесплатна при сумме 3000.
        pass

    def test_region(self):
        # TODO: доставка в область.
        pass

    def test_unknown_zone(self):
        # TODO: неизвестная зона даёт ValueError.
        pass


class TestOrderTotal(unittest.TestCase):
    def test_usual_order(self):
        # TODO: заказ 640 x 3 со скидкой 10.
        pass

    def test_boundary_sum(self):
        # TODO: сумма ровно 3000 и доставка.
        pass

    def test_negative_price(self):
        # TODO: отрицательная цена даёт ValueError.
        pass


if __name__ == "__main__":
    unittest.main()
