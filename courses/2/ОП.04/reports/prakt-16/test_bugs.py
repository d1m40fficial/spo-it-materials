"""Практика 16. Тесты, которые находят дефекты.

Запуск:
    python -m unittest test_bugs.py

Тесты менять нельзя. Исправляйте bugs.py.
"""

import unittest

from bugs import average, is_even, clamp, find_index


class TestAverage(unittest.TestCase):
    def test_usual(self):
        self.assertEqual(average([10, 20, 30]), 20)

    def test_empty(self):
        self.assertEqual(average([]), 0.0)

    def test_one_value(self):
        self.assertEqual(average([7]), 7)


class TestEven(unittest.TestCase):
    def test_even(self):
        self.assertTrue(is_even(4))

    def test_odd(self):
        self.assertFalse(is_even(7))

    def test_zero(self):
        self.assertTrue(is_even(0))


class TestClamp(unittest.TestCase):
    def test_inside(self):
        self.assertEqual(clamp(50, 0, 100), 50)

    def test_above(self):
        self.assertEqual(clamp(150, 0, 100), 100)

    def test_below(self):
        self.assertEqual(clamp(-10, 0, 100), 0)


class TestFindIndex(unittest.TestCase):
    def test_found(self):
        self.assertEqual(find_index([1, 2, 3], 2), 1)

    def test_first(self):
        self.assertEqual(find_index([5, 6], 5), 0)

    def test_missing(self):
        self.assertEqual(find_index([1, 2], 5), -1)


if __name__ == "__main__":
    unittest.main()
