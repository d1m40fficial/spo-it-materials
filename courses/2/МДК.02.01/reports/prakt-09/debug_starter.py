"""Учебный продукт: расчёт просрочки заявки.

При запуске на данных из app_log.md возникает ошибка.
Воспроизведите её, найдите причину и исправьте.
"""
from datetime import date, datetime


def parse_due(value):
    return datetime.strptime(value, "%d.%m.%Y").date()


def days_overdue(due, today=None):
    today = today or date.today()
    return (today - parse_due(due)).days


if __name__ == "__main__":
    rows = [
        {"id": 101, "due": "2026-11-20"},
        {"id": 102, "due": "2026-11-22"},
        {"id": 103, "due": "2026-11-24"},
    ]
    for row in rows:
        try:
            print(row["id"], days_overdue(row["due"]))
        except Exception as exc:
            print(row["id"], "ошибка:", exc)
