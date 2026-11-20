"""Практика 20. Маршрут по графу.

Заполните блоки TODO. Программа запускается командой
    python starter.py
и ищет пути в неориентированном графе.
"""

from collections import deque

GRAPH = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "D", "E"],
    "D": ["B", "C", "F"],
    "E": ["C", "F"],
    "F": ["D", "E"],
    "G": [],
    "H": ["I"],
    "I": ["H"],
}


def bfs(graph, start):
    """Вернуть порядок обхода в ширину."""
    # TODO: очередь, посещённые, список порядка.
    return []


def shortest_path(graph, start, target):
    """Вернуть список вершин кратчайшего пути или None."""
    # TODO: BFS с словарём parent и восстановление пути.
    return None


def component_count(graph):
    """Вернуть число компонент связности."""
    # TODO: обойдите все вершины и посчитайте новые обходы.
    return 0


print("Практика 20. Маршрут по графу")
print("=" * 44)

print("Вершины:", sorted(GRAPH))
print("Порядок BFS из A:", bfs(GRAPH, "A"))

for start, target in [("A", "F"), ("A", "G"), ("H", "I"), ("A", "A")]:
    path = shortest_path(GRAPH, start, target)
    if path:
        print(f"{start} -> {target}: {path}, шагов {len(path) - 1}")
    else:
        print(f"{start} -> {target}: пути нет")

print("Компонент связности:", component_count(GRAPH))
