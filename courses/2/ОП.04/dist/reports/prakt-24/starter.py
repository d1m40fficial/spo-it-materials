"""Практика 24. Проверка ввода регулярным выражением.

Заполните блоки TODO. Программа запускается командой
    python starter.py
и проверяет строки шаблонами.
"""

import re

PHONES = [
    "+7-912-345-67-89",
    "8-912-345-67-89",
    "+7-91-345-67-89",
    "+7-912-345-67-8X",
]

DATES = ["18.11.2026", "32.11.2026", "1.1.2026", "18/11/2026"]

CODES = ["AB-1234", "ab-1234", "AB-123", "CD-0007"]

TEXT = "12 яблок, 7 груш и 105 слив"

print("Практика 24. Проверка ввода")
print("=" * 44)

# TODO: задайте шаблоны.
PHONE = r""
DATE = r""
CODE = r""

print("\nТелефоны")
for value in PHONES:
    ok = bool(re.fullmatch(PHONE, value))
    print(f"{value:<20} {'подходит' if ok else 'не подходит'}")

print("\nДаты")
for value in DATES:
    match = re.fullmatch(DATE, value)
    if match:
        day, month, year = match.group(1), match.group(2), match.group(3)
        print(f"{value}: день {day}, месяц {month}, год {year}")
    else:
        print(f"{value}: не подходит")

print("\nАртикулы")
for value in CODES:
    ok = bool(re.fullmatch(CODE, value))
    print(f"{value:<10} {'подходит' if ok else 'не подходит'}")

print("\nЧисла в тексте")
numbers = re.findall(r"\d+", TEXT)
print(numbers)
print("Сумма:", sum(int(n) for n in numbers))
