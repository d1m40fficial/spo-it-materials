"""Тесты интерфейса. Чтение ввода здесь не используется.

Запуск:
    python -m unittest discover tests
"""

import unittest

from app.interface import parse_choice, parse_amount


class TestParseChoice(unittest.TestCase):
    def test_valid(self):
        # TODO: parse_choice("2", {0, 1, 2, 3}) == 2
        pass

    def test_spaces(self):
        # TODO: пробелы по краям не мешают.
        pass

    def test_out_of_range(self):
        # TODO: номер вне набора даёт None.
        pass

    def test_not_a_number(self):
        # TODO: текст даёт None.
        pass

    def test_empty(self):
        # TODO: пустая строка даёт None.
        pass


class TestParseAmount(unittest.TestCase):
    def test_integer(self):
        # TODO: "800" даёт 800.0
        pass

    def test_decimal_point(self):
        # TODO: "1200.50" даёт 1200.5
        pass

    def test_spaces(self):
        # TODO: пробелы по краям убираются.
        pass

    def test_negative(self):
        # TODO: отрицательная сумма даёт None.
        pass

    def test_comma(self):
        # TODO: "12,50" даёт None.
        pass

    def test_zero(self):
        # TODO: ноль допускается.
        pass


if __name__ == "__main__":
    unittest.main()
