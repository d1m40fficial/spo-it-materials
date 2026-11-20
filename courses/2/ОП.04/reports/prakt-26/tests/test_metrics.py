"""Тесты показателей. Чтение файла здесь не используется."""

import unittest

from app.metrics import total, by_region, average


class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.records = [
            {"date": "2026-11-01", "region": "север", "amount": 1200.0},
            {"date": "2026-11-01", "region": "юг", "amount": 800.0},
            {"date": "2026-11-02", "region": "север", "amount": 1500.0},
        ]

    def test_total(self):
        self.assertEqual(total(self.records), 3500.0)

    def test_total_empty(self):
        self.assertEqual(total([]), 0.0)

    def test_by_region(self):
        self.assertEqual(by_region(self.records), {"север": 2700.0, "юг": 800.0})

    def test_average(self):
        self.assertAlmostEqual(average(self.records), 3500.0 / 3)

    def test_average_empty(self):
        self.assertEqual(average([]), 0.0)


if __name__ == "__main__":
    unittest.main()
