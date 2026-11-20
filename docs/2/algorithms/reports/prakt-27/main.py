"""Точка входа мини-проекта с меню.

Запуск из корня проекта:
    python main.py
"""

from app.interface import MENU, read_choice, read_amount, read_date
from app.metrics import total, by_region, average
from app.readers import load_sales
from app.report import build_report

DATA = "data/sales.csv"


def show_report(records):
    lines = build_report(records, total(records), by_region(records), average(records))
    for line in lines:
        print(line)


def add_record(records):
    date = read_date("Дата (ГГГГ-ММ-ДД): ")
    region = input("Регион: ").strip() or "неизвестно"
    amount = read_amount("Сумма: ")
    records.append({"date": date, "region": region, "amount": amount})
    print("Запись добавлена.")


def find_region(records):
    region = input("Регион: ").strip()
    found = [record for record in records if record["region"] == region]
    if not found:
        print("Записей нет.")
        return
    print("Записей:", len(found))
    print(f"Сумма: {total(found):.2f}")


def main():
    records = load_sales(DATA)
    while True:
        print("\n" + MENU)
        choice = read_choice({0, 1, 2, 3})
        if choice == 0:
            break
        if choice == 1:
            show_report(records)
        elif choice == 2:
            add_record(records)
        elif choice == 3:
            find_region(records)


if __name__ == "__main__":
    main()
