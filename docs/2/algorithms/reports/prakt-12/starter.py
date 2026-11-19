"""Практика 12. Рекурсивный обход.

Заполните блоки TODO. Программа запускается командой
    python starter.py
и обходит вложенный каталог.
"""

TREE = {
    "name": "catalog",
    "type": "folder",
    "children": [
        {
            "name": "python",
            "type": "folder",
            "children": [
                {
                    "name": "basics",
                    "type": "folder",
                    "children": [
                        {"name": "intro.md", "type": "file", "size": 12},
                        {"name": "types.md", "type": "file", "size": 18},
                    ],
                },
                {"name": "oop.md", "type": "file", "size": 30},
            ],
        },
        {
            "name": "images",
            "type": "folder",
            "children": [
                {"name": "logo.png", "type": "file", "size": 120},
            ],
        },
        {"name": "readme.md", "type": "file", "size": 8},
    ],
}


def print_tree(node, level=0):
    """Напечатать дерево с отступом."""
    # TODO: напечатайте имя и вызовите функцию для детей.
    pass


def count_files(node):
    """Вернуть число файлов в узле."""
    # TODO: файл считается за 1, папка суммирует детей.
    return 0


def total_size(node):
    """Вернуть общий размер файлов."""
    # TODO: для файла вернуть size, для папки сумму по детям.
    return 0


def max_depth(node):
    """Вернуть максимальную глубину, корень имеет глубину 0."""
    # TODO: для файла вернуть 0, для папки 1 + максимум по детям.
    return 0


def find_path(node, target, path):
    """Вернуть список имён от корня до target или None."""
    # TODO: добавьте имя в path и проверьте детей.
    return None


print("Практика 12. Рекурсивный обход")
print("=" * 44)

print("\nДерево")
print_tree(TREE)

print("\nЧисло файлов:", count_files(TREE))
print("Общий размер:", total_size(TREE))
print("Максимальная глубина:", max_depth(TREE))

for name in ("logo.png", "missing.txt"):
    print(f"Путь к {name}:", find_path(TREE, name, []))
