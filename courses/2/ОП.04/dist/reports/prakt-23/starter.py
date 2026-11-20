"""Практика 23. Флаги и маски.

Заполните блоки TODO. Программа запускается командой
    python starter.py
и показывает набор прав в одном числе.
"""

READ = 1 << 0
WRITE = 1 << 1
EXEC = 1 << 2
DELETE = 1 << 3
ADMIN = 1 << 4

FLAGS = {
    "READ": READ,
    "WRITE": WRITE,
    "EXEC": EXEC,
    "DELETE": DELETE,
    "ADMIN": ADMIN,
}

print("Практика 23. Флаги и маски")
print("=" * 44)

rights = READ | WRITE | EXEC

print("Начальные права:", rights)
print("Двоичный вид:", bin(rights))


def has(value, flag):
    # TODO: проверьте флаг через &.
    return False


print("\nПроверка прав")
for name, flag in FLAGS.items():
    print(f"{name}: {has(rights, flag)}")

# TODO: включите DELETE.
print("\nПосле включения DELETE:", rights, bin(rights))

# TODO: снимите WRITE.
print("После снятия WRITE:", rights, bin(rights))

# TODO: переключите ADMIN.
print("После переключения ADMIN:", rights, bin(rights))


def decode(value):
    # TODO: верните список имён установленных прав.
    return []


print("\nИтоговый набор:", decode(rights))

print("\nВсе права:", 31)
print("Двоичный вид всех прав:", bin(31))
