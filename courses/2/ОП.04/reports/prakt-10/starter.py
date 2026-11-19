"""Практика 10. Устойчивый ввод и исключения.

Заполните блоки TODO. Программа запускается командой
    python starter.py
и не должна завершаться на неверном вводе.
"""

errors = []


def read_int(prompt, attempts=3):
    """Прочитать целое число, повторить запрос при ошибке."""
    # TODO: цикл, try/except ValueError, счётчик попыток.
    raw = input(prompt)
    try:
        return int(raw)
    except ValueError:
        errors.append(f'read_int: введено "{raw}"')
        return None


def read_choice():
    """Прочитать пункт меню: 0, 1, 2 или 3."""
    # TODO: повторяйте запрос, пока пункт неверный.
    raw = input("Пункт: ").strip()
    if raw in ("0", "1", "2", "3"):
        return raw
    errors.append(f"read_choice: пункт {raw}")
    return None


def safe_divide(a, b):
    """Вернуть частное или None при делении на ноль."""
    # TODO: перехватите ZeroDivisionError и запишите причину в errors.
    return a / b


print("Практика 10. Устойчивый ввод и исключения")
print("=" * 44)

a = read_int("Первое число: ")
b = read_int("Второе число: ")

print("\nМеню")
print("1. Сложить")
print("2. Вычесть")
print("3. Разделить")
print("0. Выход")

choice = read_choice()
result = None

# TODO: выполните выбранную операцию и обработайте result.

print("\nСводка")
print("Ошибок:", len(errors))
for record in errors:
    print(" -", record)
