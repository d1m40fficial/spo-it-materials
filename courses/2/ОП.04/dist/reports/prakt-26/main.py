"""Точка входа мини-проекта.

Запуск из корня проекта:
    python main.py
"""

from app.readers import load_sales
from app.metrics import total, by_region, average
from app.report import build_report

DATA = "data/sales.csv"


def main():
    records = load_sales(DATA)
    lines = build_report(records, total(records), by_region(records), average(records))
    for line in lines:
        print(line)


if __name__ == "__main__":
    main()
