#!/usr/bin/env python3
"""Print VK Video playlist titles for a course: "N. Название занятия".

Usage:
    python tools/ks/scripts/vk_titles.py courses/2/МДК.02.01
"""
import json
import re
import sys
from pathlib import Path

PREFIX = re.compile(r"^(?:Лекция|Практика|Занятие)\s*\d+\.\s*", re.I)


def clean(title: str) -> str:
    return PREFIX.sub("", str(title)).strip()


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    course_dir = Path(sys.argv[1])
    data = json.loads((course_dir / "course.json").read_text(encoding="utf-8"))
    for chapter in data.get("chapters", []):
        print(f'{chapter.get("n", "?")}. {clean(chapter.get("title", ""))}')


if __name__ == "__main__":
    main()
