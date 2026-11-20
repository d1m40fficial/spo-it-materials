"""Чтение выгрузки продаж."""

import csv


def load_sales(path="data/sales.csv"):
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        return [
            {
                "date": row["date"],
                "region": row["region"],
                "amount": float(row["amount"]),
            }
            for row in reader
        ]
