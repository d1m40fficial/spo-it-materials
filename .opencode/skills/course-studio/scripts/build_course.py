#!/usr/bin/env python3
"""Build course pages from course.json files.

Usage:
    python3 build_course.py courses/<slug>            # course page + every written chapter → courses/<slug>/dist/
    python3 build_course.py courses/ --catalog        # catalog of every course → courses/catalog.html

The course page shows the hero, outcomes and the syllabus (chapter status, minutes,
topics). Chapters with a chapter.md are built with build_chapter.py and linked.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _pages import accent_vars, code_class, esc, is_cards, lesson_slots, load_course, page, plural_lessons, plural_sections, rail, ASSETS  # noqa: E402
from availability import is_open, load_availability, summary  # noqa: E402
from plan_xlsx import plan_filename, write_plan_xlsx  # noqa: E402

HERE = Path(__file__).resolve().parent
SHADER_JS = (ASSETS / "shader.js").read_text(encoding="utf-8")


def chapter_dir(c: dict) -> str:
    return c.get("dir") or f'{int(c["n"]):02d}-{c["slug"]}'


def price(c: dict) -> str:
    if c.get("price") in (None, ""):
        return ""
    cur = c.get("currency") or ""
    sym = {"INR": "₹", "USD": "$", "EUR": "€", "GBP": "£"}.get(cur, f"{cur} " if cur else "")
    return f"{sym}{int(c['price']):,}"


def spec_line(c: dict, hours: int = None) -> str:
    h = hours if hours is not None else c.get("hours")
    bits = [c.get("level"), f'{h} ч' if h else None]
    if c.get("languages"):
        bits.append(" / ".join(c["languages"]))
    return " · ".join(b for b in bits if b)


def card_art(ch: dict) -> str:
    """A small thematic SVG illustration for a lesson card."""
    title = str(ch.get("title", "")).lower()
    text = " ".join([
        str(ch.get("title", "")),
        str(ch.get("summary", "")),
        " ".join(ch.get("topics", []) or []),
    ]).lower()

    def choose(source: str):
        def has(*words):
            return any(word in source for word in words)

        if has("база данных", "субд", "mysql", "sql", "er-", "нормализ", "таблиц", "запрос",
               "резервн", "копир", "backup"):
            return "db"
        if has("безопас", "защит", "парол", "доступ", "аудит"):
            return "shield"
        if has("сеть", "tcp", "ip", "dns", "маршрут", "коммутац", "vpn"):
            return "network"
        if has("тест", "дефект", "баг", "качеств"):
            return "test"
        if has("api", "интеграц", "postman", "обмен", "сервис"):
            return "api"
        if has("проект", "wbs", "риск", "бюджет", "agile", "scrum", "план", "внедрен",
               "обследован", "требован", "изменен"):
            return "project"
        if has("интерфейс", "дизайн", "макет", "ux", "экран"):
            return "design"
        if has("ос", "linux", "windows", "процесс", "память", "файлов", "командн"):
            return "os"
        if has("документ", "инструкц", "отчёт", "регламент", "руководств"):
            return "docs"
        if has("алгоритм", "цикл", "массив", "строк", "функц", "рекурс", "сортиров"):
            return "code"
        if has("процессор", "плата", "шина", "накопител", "чипсет", "bios", "uefi"):
            return "hardware"
        if has("матем", "модель", "график", "вероятн", "регресс", "статистик"):
            return "math"
        if has("сертификац", "стандарт"):
            return "cert"
        if has("поддержк", "сопровожд", "инцидент", "sla", "мониторинг", "диагност",
               "непрерывн", "сбой", "обращен"):
            return "support"
        if has("обучен", "занятие", "урок"):
            return "learn"
        if has("экзамен", "демо", "задание", "защита"):
            return "exam"
        return None

    icon = ch.get("icon")
    motif = icon if icon in CARD_ART else (choose(title) or choose(text) or "default")
    inner = CARD_ART[motif].replace("var(--accent)", "var(--course-accent, var(--accent))")
    return (f'<div class="card-art" aria-hidden="true"><svg viewBox="0 0 120 120" fill="none" '
            f'stroke="var(--course-accent, var(--accent))" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">'
            f'{inner}</svg></div>')


CARD_ART = {
    "db": '<ellipse cx="60" cy="34" rx="28" ry="10"/><path d="M32 34v22c0 5.5 12.5 10 28 10s28-4.5 28-10V34"/><path d="M32 56v22c0 5.5 12.5 10 28 10s28-4.5 28-10V56"/><path d="M32 45c0 5.5 12.5 10 28 10s28-4.5 28-10" opacity=".45"/>',
    "code": '<rect x="22" y="28" width="76" height="64" rx="10"/><path d="M22 44h76"/><path d="M40 64l-8 8 8 8"/><path d="M80 64l8 8-8 8"/><path d="M66 60l-12 24"/>',
    "network": '<circle cx="60" cy="30" r="10"/><circle cx="30" cy="84" r="10"/><circle cx="90" cy="84" r="10"/><path d="M60 40v14M52 52l-14 22M68 52l14 22"/><circle cx="60" cy="56" r="4" fill="var(--accent)" stroke="none"/>',
    "shield": '<path d="M60 20l30 12v22c0 20-13 34-30 42-17-8-30-22-30-42V32z"/><path d="M46 60l10 10 20-22"/>',
    "project": '<rect x="20" y="24" width="24" height="72" rx="5"/><rect x="48" y="24" width="24" height="48" rx="5"/><rect x="76" y="24" width="24" height="60" rx="5"/><path d="M28 40h8M28 52h8M56 40h8M84 40h8M84 52h8"/>',
    "test": '<circle cx="54" cy="52" r="24"/><path d="M72 70l18 18"/><path d="M44 52l7 7 13-15"/>',
    "design": '<rect x="20" y="24" width="80" height="72" rx="10"/><path d="M20 42h80"/><rect x="32" y="54" width="26" height="30" rx="4"/><path d="M68 58h20M68 68h20M68 78h14"/>',
    "api": '<circle cx="30" cy="60" r="10"/><circle cx="90" cy="60" r="10"/><path d="M40 60h14M66 60h14"/><path d="M54 48v24M66 48v24"/><path d="M54 60h12"/>',
    "os": '<rect x="18" y="26" width="84" height="68" rx="10"/><path d="M18 42h84"/><path d="M32 58l10 10-10 10M50 78h20"/><circle cx="30" cy="34" r="2" fill="var(--accent)" stroke="none"/><circle cx="38" cy="34" r="2" fill="var(--accent)" stroke="none"/>',
    "docs": '<path d="M34 20h40l16 16v64H34z"/><path d="M74 20v16h16"/><path d="M46 52h32M46 64h32M46 76h20"/>',
    "algorithm": '<rect x="20" y="22" width="36" height="24" rx="6"/><path d="M56 34h16v22H56"/><rect x="44" y="74" width="36" height="24" rx="6"/><path d="M62 56v18"/><path d="M78 34h16v40H78"/>',
    "hardware": '<rect x="30" y="30" width="60" height="60" rx="10"/><rect x="46" y="46" width="28" height="28" rx="5"/><path d="M40 18v12M60 18v12M80 18v12M40 90v12M60 90v12M80 90v12M18 40h12M18 60h12M18 80h12M90 40h12M90 60h12M90 80h12"/>',
    "math": '<path d="M24 90V30M24 90h72"/><path d="M34 78c12-4 18-28 30-28s18 16 30 8"/><path d="M34 70h8M34 50h8M34 30h8M44 82v8M64 82v8M84 82v8"/>',
    "cert": '<rect x="24" y="20" width="72" height="56" rx="8"/><path d="M40 40h40M40 52h28"/><circle cx="60" cy="76" r="12"/><path d="M54 86l-4 14 10-6 10 6-4-14"/>',
    "support": '<path d="M34 64v-8a26 26 0 0152 0v8"/><rect x="26" y="60" width="14" height="22" rx="7"/><rect x="80" y="60" width="14" height="22" rx="7"/><path d="M86 82c0 8-8 14-18 14h-8"/><circle cx="56" cy="96" r="4" fill="var(--accent)" stroke="none"/>',
    "learn": '<rect x="20" y="26" width="80" height="54" rx="8"/><path d="M32 42h36M32 54h28M32 66h20"/><circle cx="88" cy="74" r="12"/><path d="M82 74l4 4 8-9"/>',
    "exam": '<rect x="28" y="20" width="64" height="80" rx="8"/><path d="M44 42l6 6 12-12M44 64l6 6 12-12M44 86l6 6 12-12"/><path d="M70 48h10M70 70h10M70 92h10" opacity=".45"/>',
    "assemble": '<rect x="22" y="30" width="52" height="26" rx="7"/><path d="M32 43h20" opacity=".45"/><rect x="22" y="64" width="52" height="26" rx="7"/><path d="M32 77h12" opacity=".45"/><path d="M90 34v24M78 46h24"/>',
    "strategy": '<circle cx="28" cy="60" r="9"/><path d="M37 60h13"/><path d="M50 60c14 0 12-26 32-26"/><path d="M50 60h32"/><path d="M50 60c14 0 12 26 32 26"/><circle cx="94" cy="34" r="7"/><circle cx="94" cy="60" r="7"/><circle cx="94" cy="86" r="7"/>',
    "survey": '<rect x="18" y="34" width="42" height="60" rx="6"/><path d="M28 50h10M42 50h8M28 64h10M42 64h8M28 78h10M42 78h8" opacity=".45"/><circle cx="76" cy="56" r="17"/><path d="M88 68l14 14"/>',
    "processmap": '<rect x="14" y="30" width="30" height="20" rx="5"/><rect x="14" y="76" width="30" height="20" rx="5"/><rect x="62" y="76" width="30" height="20" rx="5"/><path d="M44 40h10v48h8M44 86h18"/><path d="M58 18h32a6 6 0 016 6v14a6 6 0 01-6 6H78l-9 9v-9h-11a6 6 0 01-6-6V24a6 6 0 016-6z" opacity=".45"/>',
    "gap": '<path d="M40 26H24v68h16"/><path d="M80 26h16v68H80"/><path d="M48 60h24"/><path d="M56 52l-8 8 8 8M64 52l8 8-8 8"/>',
    "priorities": '<rect x="18" y="26" width="58" height="18" rx="5"/><circle cx="66" cy="35" r="4" fill="var(--accent)" stroke="none"/><rect x="18" y="52" width="44" height="18" rx="5" opacity=".45"/><rect x="18" y="78" width="30" height="18" rx="5" opacity=".45"/><path d="M94 92V58M86 66l8-8 8 8"/>',
    "plan": '<rect x="18" y="26" width="84" height="72" rx="8"/><path d="M18 46h84"/><path d="M38 16v16M82 16v16"/><path d="M32 60h12M54 60h12M76 60h12M32 78h12M54 78h12" opacity=".45"/>',
    "sliders": '<path d="M22 36h76M22 60h76M22 84h76" opacity=".35"/><circle cx="46" cy="36" r="9"/><circle cx="78" cy="60" r="9"/><circle cx="38" cy="84" r="9"/>',
    "roadmap": '<path d="M22 92c16 0 12-24 28-24s10 18 26 18 16-18 16-32" stroke-dasharray="6 7"/><circle cx="22" cy="92" r="6"/><path d="M86 54V20"/><path d="M86 20h18l-5 8 5 8H86"/>',
    "migrate": '<ellipse cx="32" cy="36" rx="15" ry="6"/><path d="M17 36v30c0 3.5 6.7 6 15 6s15-2.5 15-6V36"/><path d="M17 51c0 3.5 6.7 6 15 6s15-2.5 15-6" opacity=".45"/><ellipse cx="88" cy="36" rx="15" ry="6"/><path d="M73 36v30c0 3.5 6.7 6 15 6s15-2.5 15-6V36"/><path d="M73 51c0 3.5 6.7 6 15 6s15-2.5 15-6" opacity=".45"/><path d="M50 62h20M62 54l8 8-8 8"/>',
    "import": '<path d="M34 18h40l14 14v54H34z"/><path d="M74 18v14h14"/><path d="M62 46v20M54 58l8 8 8-8"/><path d="M26 96h68" opacity=".45"/>',
    "compare": '<rect x="14" y="28" width="30" height="64" rx="6"/><rect x="76" y="28" width="30" height="64" rx="6"/><path d="M22 44h14M22 56h14M22 68h9M84 44h14M84 56h14M84 68h9" opacity=".45"/><path d="M50 62l6 6 12-14"/>',
    "link": '<rect x="10" y="40" width="32" height="40" rx="6"/><rect x="78" y="40" width="32" height="40" rx="6"/><path d="M42 60h36M50 52l-8 8 8 8M70 52l8 8-8 8"/>',
    "browsersync": '<rect x="16" y="20" width="88" height="72" rx="8"/><path d="M16 36h88"/><circle cx="27" cy="28" r="2.5" fill="var(--accent)" stroke="none"/><circle cx="36" cy="28" r="2.5" fill="var(--accent)" stroke="none"/><path d="M34 54h30M56 46l8 8-8 8"/><path d="M86 78H56M64 70l-8 8 8 8"/>',
    "lessonplan": '<rect x="16" y="24" width="88" height="62" rx="8"/><path d="M28 42h30M28 54h22M28 66h14" opacity=".45"/><circle cx="82" cy="58" r="12"/><path d="M78 51l10 7-10 7z"/>',
    "memo": '<path d="M30 16h44l12 12v58H30z"/><path d="M74 16v12h12"/><path d="M42 42h26M42 54h20" opacity=".45"/><circle cx="72" cy="74" r="13"/><path d="M66 74l5 5 9-10"/>',
    "orgchange": '<rect x="46" y="16" width="28" height="20" rx="5"/><path d="M60 36v10M60 46H32v20M60 46h28v20"/><rect x="18" y="66" width="28" height="18" rx="5"/><rect x="74" y="66" width="28" height="18" rx="5"/><path d="M40 98h40M48 90l-8 8 8 8M72 90l8 8-8 8"/>',
    "branch": '<path d="M34 96V26"/><path d="M34 68c0-14 30-8 30-24"/><circle cx="34" cy="26" r="7"/><circle cx="34" cy="68" r="7"/><circle cx="34" cy="96" r="7"/><circle cx="64" cy="44" r="7"/>',
    "risk": '<path d="M60 22l38 66H22z"/><path d="M60 46v22"/><circle cx="60" cy="78" r="3" fill="var(--accent)" stroke="none"/>',
    "stamp": '<path d="M44 22h32l-4 32H48z"/><rect x="34" y="58" width="52" height="12" rx="4"/><rect x="24" y="74" width="72" height="18" rx="5"/><path d="M55 83l5 5 9-9"/>',
    "pilot": '<circle cx="60" cy="60" r="34" stroke-dasharray="6 8" opacity=".45"/><circle cx="60" cy="60" r="21"/><path d="M55 50l16 10-16 10z"/>',
    "testplan": '<rect x="14" y="18" width="50" height="84" rx="8"/><path d="M24 36l5 5 9-10M24 56l5 5 9-10M24 76l5 5 9-10"/><path d="M46 40h8M46 60h8M46 80h8" opacity=".45"/><path d="M84 96V34"/><path d="M84 34h22l-6 9 6 9H84"/>',
    "gear": '<circle cx="60" cy="60" r="17"/><circle cx="60" cy="60" r="6" opacity=".45"/><path d="M60 43V34M60 77v9M77 60h9M43 60h-9M72 48l6-6M48 48l-6-6M72 72l6 6M48 72l-6 6"/>',
    "effect": '<path d="M20 98h78" opacity=".45"/><rect x="28" y="62" width="14" height="34" rx="3"/><rect x="52" y="46" width="14" height="50" rx="3"/><rect x="76" y="30" width="14" height="66" rx="3"/><path d="M26 40l22-12 14 6 22-16"/><path d="M76 24h10v10"/>',
    "queue": '<rect x="18" y="30" width="48" height="16" rx="4" opacity=".45"/><rect x="18" y="54" width="48" height="16" rx="4" opacity=".45"/><rect x="18" y="78" width="48" height="16" rx="4"/><path d="M88 96V48M78 58l10-10 10 10"/>',
    "shieldkey": '<path d="M60 20l30 12v22c0 20-13 34-30 42-17-8-30-22-30-42V32z"/><circle cx="60" cy="54" r="7"/><path d="M60 61v13"/>',
    "keylist": '<circle cx="32" cy="48" r="14"/><path d="M42 58l20 20M54 70l6-6M62 78l6-6"/><rect x="74" y="24" width="28" height="40" rx="5" opacity=".45"/><path d="M81 34h14M81 44h14M81 54h9" opacity=".3"/>',
    "backup": '<ellipse cx="44" cy="32" rx="18" ry="7"/><path d="M26 32v34c0 4 8 7 18 7s18-3 18-7V32"/><path d="M26 49c0 4 8 7 18 7s18-3 18-7" opacity=".45"/><rect x="66" y="50" width="30" height="40" rx="6" opacity=".55"/><path d="M74 62h14M74 72h14M74 82h8" opacity=".35"/>',
    "restore": '<circle cx="44" cy="44" r="24"/><path d="M44 30v15l10 6"/><ellipse cx="80" cy="78" rx="18" ry="7"/><path d="M62 78v14c0 4 8 7 18 7s18-3 18-7V78"/><path d="M62 85c0 4 8 7 18 7s18-3 18-7" opacity=".45"/>',
    "inbox": '<path d="M18 48h20l6 10h32l6-10h20"/><path d="M18 48v42h84V48"/><path d="M44 18v18M36 28l8 8 8-8"/><path d="M76 18v18M68 28l8 8 8-8"/>',
    "dashboard": '<rect x="14" y="26" width="92" height="68" rx="8"/><rect x="28" y="66" width="14" height="18" rx="3"/><rect x="53" y="52" width="14" height="32" rx="3"/><rect x="78" y="40" width="14" height="44" rx="3"/>',
    "metricsdoc": '<rect x="8" y="26" width="52" height="44" rx="6"/><path d="M16 62V50M26 62V42M36 62V54"/><path d="M68 22h24l8 8v56H68z"/><path d="M92 22v8h8"/><path d="M75 48h14M75 58h14M75 68h9" opacity=".45"/>',
    "finish": '<path d="M16 98c14 0 20-8 32-8s14 8 26 8 16-6 24-6" opacity=".45"/><path d="M66 94V36"/><path d="M66 36h30l-8 11 8 11H66"/><path d="M32 64l8 8 16-18"/>',
    "defense": '<rect x="12" y="24" width="52" height="38" rx="6"/><path d="M22 38h28M22 48h20" opacity=".45"/><path d="M38 62v8M28 86l10-16 10 16"/><path d="M88 50l16 6v12c0 11-7 18-16 22-9-4-16-11-16-16V56z"/>',
    "sla": '<path d="M28 16h40l14 14v58H28z"/><path d="M68 16v14h14"/><path d="M38 40h20M38 50h16" opacity=".45"/><circle cx="60" cy="70" r="13"/><path d="M60 62v8l6 4"/>',
    "incident": '<path d="M78 46a18 18 0 00-36 0c0 16-8 20-8 20h52s-8-4-8-20z"/><path d="M52 78a8 8 0 0016 0"/><path d="M60 18v-6" opacity=".45"/>',
    "tree": '<circle cx="60" cy="24" r="8"/><path d="M60 32v18M60 50H34v14M60 50h26v14"/><rect x="22" y="64" width="24" height="18" rx="4"/><rect x="48" y="64" width="24" height="18" rx="4"/><rect x="74" y="64" width="24" height="18" rx="4"/>',
    "timeline": '<path d="M16 60h88"/><circle cx="30" cy="60" r="6"/><circle cx="60" cy="60" r="6"/><circle cx="90" cy="60" r="6"/><path d="M30 54V38h18" opacity=".45"/><path d="M60 66v16h16" opacity=".45"/>',
    "request": '<rect x="22" y="18" width="56" height="84" rx="8"/><path d="M34 38h24M34 52h24M34 66h14" opacity=".45"/><path d="M90 62v24M78 74h24"/>',
    "monitor": '<rect x="14" y="24" width="92" height="60" rx="8"/><path d="M26 58h12l7-14 9 28 8-20 6 6h22"/><path d="M60 84v10M44 100h32"/>',
    "logs": '<rect x="16" y="22" width="88" height="76" rx="8"/><path d="M16 40h88"/><circle cx="27" cy="31" r="2.5" fill="var(--accent)" stroke="none"/><circle cx="36" cy="31" r="2.5" fill="var(--accent)" stroke="none"/><path d="M30 56h44M30 68h34M30 80h48" opacity=".45"/>',
    "server": '<rect x="26" y="16" width="68" height="26" rx="5"/><rect x="26" y="48" width="68" height="26" rx="5"/><rect x="26" y="80" width="68" height="26" rx="5"/><circle cx="40" cy="29" r="2.5" fill="var(--accent)" stroke="none"/><circle cx="40" cy="61" r="2.5" fill="var(--accent)" stroke="none"/><circle cx="40" cy="93" r="2.5" fill="var(--accent)" stroke="none"/><path d="M58 29h24M58 61h24M58 93h24" opacity=".45"/>',
    "update": '<rect x="22" y="56" width="76" height="42" rx="7"/><path d="M60 46V22M46 34l14-12 14 12"/><path d="M34 70h24M34 82h16" opacity=".45"/>',
    "rollback": '<rect x="30" y="20" width="60" height="76" rx="7"/><path d="M74 58H46M58 44L44 58l14 14"/>',
    "access": '<circle cx="44" cy="34" r="13"/><path d="M44 47c-13 0-22 9-22 21v22h44V68"/><circle cx="84" cy="66" r="16"/><path d="M76 66l6 6 12-13"/>',
    "roles": '<rect x="18" y="24" width="84" height="72" rx="6"/><path d="M18 46h84M18 70h84M46 24v72M74 24v72"/><rect x="46" y="46" width="28" height="24" fill="var(--accent)" stroke="none" opacity=".35"/>',
    "knowledge": '<path d="M18 32c12-6 24-6 32 0v60c-8-6-20-6-32 0z"/><path d="M82 32c-12-6-24-6-32 0v60c8-6 20-6 32 0z"/><path d="M60 16v-8M78 20l5-6M42 20l-5-6" opacity=".45"/>',
    "comms": '<path d="M14 30a8 8 0 018-8h36a8 8 0 018 8v16a8 8 0 01-8 8H44l-12 10V54H22a8 8 0 01-8-8z"/><path d="M62 60h24a8 8 0 018 8v10a8 8 0 01-8 8H84v8l-9-8H62a8 8 0 01-8-8V68a8 8 0 018-8z" opacity=".45"/>',
    "report": '<rect x="26" y="20" width="68" height="80" rx="6"/><rect x="46" y="12" width="28" height="14" rx="4"/><path d="M40 78V64M54 78V50M68 78V58"/><path d="M36 92h48" opacity=".45"/>',
    "continuity": '<path d="M34 46a30 30 0 0142-14"/><path d="M70 24l10 8-8 10"/><path d="M86 74a30 30 0 01-42 14"/><path d="M50 96l-10-8 8-10"/><circle cx="60" cy="60" r="7" opacity=".45"/>',
    "data": '<rect x="20" y="22" width="80" height="20" rx="4"/><rect x="20" y="50" width="80" height="20" rx="4"/><rect x="20" y="78" width="80" height="20" rx="4"/><circle cx="32" cy="32" r="2.5" fill="var(--accent)" stroke="none"/><circle cx="32" cy="60" r="2.5" fill="var(--accent)" stroke="none"/><circle cx="32" cy="88" r="2.5" fill="var(--accent)" stroke="none"/><path d="M46 32h38M46 60h38M46 88h26" opacity=".45"/>',
    "layers": '<path d="M60 18l38 18-38 18-38-18z"/><path d="M22 60l38 18 38-18"/><path d="M22 78l38 18 38-18"/>',
    "hierarchy": '<rect x="42" y="14" width="36" height="20" rx="5"/><path d="M60 34v12M24 46h72"/><path d="M24 46v10M60 46v10M96 46v10"/><rect x="10" y="56" width="28" height="18" rx="5"/><rect x="46" y="56" width="28" height="18" rx="5"/><rect x="82" y="56" width="28" height="18" rx="5"/><rect x="36" y="86" width="48" height="18" rx="5" opacity=".45"/><path d="M60 74v12" opacity=".45"/>',
    "flow": '<path d="M18 34h50M56 26l10 8-10 8"/><path d="M18 60h72M80 52l10 8-10 8"/><path d="M18 86h34M42 78l10 8-10 8"/>',
    "architecture": '<rect x="12" y="30" width="34" height="26" rx="5"/><rect x="74" y="30" width="34" height="26" rx="5"/><path d="M46 43h28"/><path d="M58 37l6 6-6 6"/><rect x="42" y="74" width="36" height="26" rx="5" opacity=".45"/><path d="M60 56v18" opacity=".45"/>',
    "lifecycle": '<circle cx="60" cy="60" r="30"/><circle cx="60" cy="30" r="5"/><circle cx="90" cy="60" r="5"/><circle cx="60" cy="90" r="5"/><circle cx="30" cy="60" r="5"/><path d="M80 38l6-6M82 82l6 6M40 82l-6 6M38 38l-6-6" opacity=".45"/>',
    "er": '<rect x="10" y="18" width="36" height="24" rx="4"/><rect x="74" y="18" width="36" height="24" rx="4"/><rect x="42" y="76" width="36" height="24" rx="4"/><path d="M46 30h28M28 42v32h14M92 42v32H78"/>',
    "schema": '<rect x="14" y="24" width="92" height="72" rx="6"/><path d="M14 44h92M14 62h92M14 80h92M40 24v72"/><circle cx="27" cy="34" r="3" fill="var(--accent)" stroke="none"/><path d="M50 34h40M50 54h40M50 72h40M50 90h24" opacity=".45"/>',
    "services": '<circle cx="60" cy="60" r="14"/><circle cx="26" cy="26" r="8"/><circle cx="94" cy="26" r="8"/><circle cx="60" cy="98" r="8"/><path d="M33 32l17 17M87 32L70 49M60 74v16"/>',
    "grid": '<rect x="16" y="16" width="30" height="30" rx="5"/><rect x="16" y="56" width="30" height="30" rx="5"/><rect x="56" y="16" width="30" height="30" rx="5"/><rect x="56" y="56" width="30" height="30" rx="5" opacity=".45"/>',
    "replica": '<ellipse cx="32" cy="52" rx="16" ry="6"/><path d="M16 52v26c0 3 7 6 16 6s16-3 16-6V52"/><path d="M16 65c0 3 7 6 16 6s16-3 16-6" opacity=".45"/><ellipse cx="88" cy="52" rx="16" ry="6"/><path d="M72 52v26c0 3 7 6 16 6s16-3 16-6V52"/><path d="M72 65c0 3 7 6 16 6s16-3 16-6" opacity=".45"/><path d="M48 44h24M62 38l6 6-6 6M72 60H48M58 54l-6 6 6 6"/>',
    "index": '<rect x="14" y="26" width="80" height="64" rx="6"/><path d="M14 46h80M14 66h80M48 26v64"/><rect x="48" y="26" width="24" height="64" fill="var(--accent)" stroke="none" opacity=".18"/><path d="M100 34h8M100 58h8M100 82h8" opacity=".45"/>',
    "lock": '<rect x="30" y="54" width="60" height="44" rx="8"/><path d="M44 54V42a16 16 0 0132 0v12"/><circle cx="60" cy="72" r="6"/><path d="M60 78v8"/>',
    "export": '<path d="M16 20h44l14 14v66H16z"/><path d="M60 20v14h14"/><path d="M28 50h22M42 42l8 8-8 8"/><path d="M28 68h16" opacity=".45"/>',
    "standard": '<path d="M22 16h44l14 14v66H22z"/><path d="M66 16v14h14"/><path d="M34 42h26M34 54h18" opacity=".45"/><circle cx="88" cy="72" r="12"/><path d="M84 80l-2 12 6-4 6 4-2-12"/>',
    "medal": '<circle cx="60" cy="46" r="22"/><path d="M50 46l7 7 14-15"/><path d="M48 66l-6 30 18-9 18 9-6-30" opacity=".55"/>',
    "function": '<rect x="34" y="28" width="52" height="64" rx="8"/><path d="M18 44h16M18 76h16"/><path d="M86 60h16M98 54l4 6-4 6"/><path d="M52 52h16M52 68h10" opacity=".45"/>',
    "oop": '<rect x="20" y="16" width="80" height="88" rx="8"/><path d="M20 38h80M20 70h80"/><path d="M30 28h20"/><circle cx="30" cy="52" r="2.5" fill="var(--accent)" stroke="none"/><path d="M40 52h22M40 60h16" opacity=".45"/><circle cx="30" cy="84" r="2.5" fill="var(--accent)" stroke="none"/><path d="M40 84h24" opacity=".45"/>',
    "json": '<path d="M44 26c-8 0-8 10-8 10s0 8-8 8c8 0 8 8 8 8s0 10 8 10"/><path d="M76 26c8 0 8 10 8 10s0 8 8 8c-8 0-8 8-8 8s0 10-8 10"/><path d="M46 52h28M46 64h18" opacity=".45"/>',
    "bug": '<ellipse cx="60" cy="66" rx="16" ry="20"/><circle cx="60" cy="42" r="8"/><path d="M52 34l-6-6M68 34l6-6"/><path d="M44 58l-14-6M44 72H28M44 84l-14 8M76 58l14-6M76 72h16M76 84l14 8"/><path d="M60 50v32" opacity=".45"/>',
    "usecase": '<circle cx="24" cy="34" r="8"/><path d="M24 42v20M16 50h16M24 62l-8 14M24 62l8 14"/><ellipse cx="82" cy="58" rx="24" ry="14"/><path d="M34 52h24" opacity=".45"/>',
    "sequence": '<rect x="14" y="18" width="24" height="14" rx="3"/><rect x="48" y="18" width="24" height="14" rx="3"/><rect x="82" y="18" width="24" height="14" rx="3"/><path d="M26 32v72M60 32v72M94 32v72" opacity=".45"/><path d="M38 50h24M56 46l6 4-6 4M94 66H70M76 62l-6 4 6 4"/>',
    "state": '<rect x="18" y="22" width="42" height="22" rx="11"/><rect x="60" y="76" width="42" height="22" rx="11"/><path d="M60 40c16 0 4 38 20 38"/><path d="M72 72l8 6-8 6"/>',
    "c4": '<rect x="12" y="14" width="96" height="92" rx="8"/><rect x="26" y="28" width="38" height="26" rx="4"/><rect x="26" y="64" width="38" height="26" rx="4" opacity=".45"/><rect x="72" y="64" width="24" height="26" rx="4"/>',
    "micro": '<circle cx="60" cy="60" r="12"/><rect x="14" y="14" width="20" height="20" rx="4"/><rect x="86" y="14" width="20" height="20" rx="4"/><rect x="14" y="86" width="20" height="20" rx="4"/><rect x="86" y="86" width="20" height="20" rx="4"/><path d="M34 34l16 16M86 34L70 50M34 86l16-16M86 86L70 70"/>',
    "cache": '<path d="M66 18L42 62h16l-6 40 28-48H62z"/>',
    "prototype": '<rect x="36" y="10" width="48" height="100" rx="10"/><path d="M54 20h12" opacity=".45"/><rect x="44" y="32" width="32" height="12" rx="3"/><rect x="44" y="50" width="32" height="22" rx="3" opacity=".45"/><rect x="44" y="78" width="20" height="10" rx="3"/>',
    "boundary": '<path d="M14 60h92"/><path d="M34 46v28M70 46v28"/><circle cx="34" cy="60" r="4" fill="var(--accent)" stroke="none"/><circle cx="70" cy="60" r="4" fill="var(--accent)" stroke="none"/><path d="M22 78h16M62 78h16" opacity=".45"/>',
    "load": '<path d="M24 78a36 36 0 1172 0"/><path d="M60 78l16-22"/><circle cx="60" cy="78" r="4" fill="var(--accent)" stroke="none"/><path d="M36 92h48" opacity=".45"/>',
    "people": '<circle cx="60" cy="38" r="11"/><path d="M40 78c0-11 9-18 20-18s20 7 20 18"/><circle cx="30" cy="48" r="8" opacity=".45"/><path d="M14 78c0-9 7-14 16-14" opacity=".45"/><circle cx="90" cy="48" r="8" opacity=".45"/><path d="M106 78c0-9-7-14-16-14" opacity=".45"/>',
    "budget": '<rect x="14" y="36" width="92" height="48" rx="6"/><circle cx="60" cy="60" r="13"/><path d="M24 48v24M96 48v24" opacity=".45"/>',
    "board": '<rect x="12" y="18" width="96" height="84" rx="7"/><path d="M44 18v84M76 18v84"/><rect x="20" y="30" width="16" height="10" rx="3"/><rect x="20" y="46" width="16" height="10" rx="3" opacity=".45"/><rect x="52" y="30" width="16" height="10" rx="3" opacity=".45"/><rect x="52" y="46" width="16" height="10" rx="3"/><rect x="84" y="30" width="16" height="10" rx="3" opacity=".45"/>',
    "string": '<path d="M28 32l-7 14M40 32l-7 14"/><path d="M58 38h34M58 52h28M58 66h34M58 80h20" opacity=".45"/>',
    "sort": '<path d="M18 96h84" opacity=".35"/><rect x="26" y="70" width="14" height="26" rx="3"/><rect x="48" y="54" width="14" height="42" rx="3"/><rect x="70" y="38" width="14" height="58" rx="3"/><path d="M26 28h60M76 20l10 8-10 8"/>',
    "recursion": '<rect x="14" y="14" width="92" height="92" rx="8"/><rect x="32" y="32" width="56" height="56" rx="6"/><rect x="48" y="48" width="24" height="24" rx="4"/><circle cx="60" cy="60" r="4" fill="var(--accent)" stroke="none"/>',
    "graph": '<circle cx="24" cy="32" r="9"/><circle cx="24" cy="88" r="9"/><circle cx="76" cy="24" r="9"/><circle cx="96" cy="72" r="9"/><circle cx="56" cy="72" r="9"/><path d="M32 37l18 29M32 83l16-8M32 28l35-3M72 32l-12 31M65 76l22-3"/>',
    "steps": '<path d="M14 100h24V76h26V52h26V28h16"/><path d="M92 20l14 8-14 8" opacity=".45"/>',
    "bits": '<rect x="18" y="28" width="34" height="34" rx="6"/><rect x="68" y="28" width="34" height="34" rx="6"/><rect x="18" y="66" width="34" height="34" rx="6"/><rect x="68" y="66" width="34" height="34" rx="6" opacity=".45"/><circle cx="35" cy="45" r="4" fill="var(--accent)" stroke="none"/><circle cx="85" cy="45" r="4" fill="var(--accent)" stroke="none" opacity=".45"/><circle cx="35" cy="83" r="4" fill="var(--accent)" stroke="none" opacity=".45"/>',
    "regex": '<path d="M34 28H22v64h12M86 28h12v64H86"/><path d="M60 44v32M48 52l24 16M72 52L48 68"/>',
    "logic": '<path d="M32 34h18a26 26 0 010 52H32z"/><path d="M14 48h18M14 72h18M76 60h16M88 54l8 6-8 6"/>',
    "ram": '<rect x="12" y="40" width="96" height="40" rx="5"/><path d="M24 80v10M38 80v10M52 80v10M66 80v10M80 80v10M94 80v10"/><rect x="24" y="56" width="14" height="12" rx="2"/><rect x="46" y="56" width="14" height="12" rx="2"/><rect x="68" y="56" width="14" height="12" rx="2"/><rect x="90" y="56" width="10" height="12" rx="2" opacity=".45"/>',
    "boardpc": '<rect x="14" y="14" width="92" height="92" rx="6"/><rect x="26" y="26" width="26" height="26" rx="4"/><rect x="62" y="26" width="32" height="14" rx="3"/><rect x="62" y="46" width="32" height="10" rx="3" opacity=".45"/><rect x="26" y="62" width="16" height="32" rx="3" opacity=".45"/><rect x="50" y="62" width="44" height="12" rx="3"/>',
    "disk": '<circle cx="60" cy="60" r="34"/><circle cx="60" cy="60" r="9"/><path d="M60 60l24-16"/><path d="M84 44l8-5" opacity=".45"/>',
    "gpu": '<rect x="12" y="34" width="96" height="52" rx="6"/><circle cx="46" cy="60" r="15"/><circle cx="78" cy="60" r="15" opacity=".45"/><path d="M46 51c5 5 5 13 0 18M78 51c5 5 5 13 0 18" opacity=".45"/>',
    "keyboard": '<rect x="10" y="40" width="100" height="42" rx="6"/><path d="M22 52h8M38 52h8M54 52h8M70 52h8M86 52h12M22 66h8M38 66h8M54 66h44" opacity=".45"/>',
    "fan": '<circle cx="60" cy="60" r="34"/><circle cx="60" cy="60" r="7"/><path d="M60 53c-2-11 5-17 11-13 5 3 4 10-2 13"/><path d="M67 60c11-2 17 5 13 11-3 5-10 4-13-2"/><path d="M60 67c2 11-5 17-11 13-5-3-4-10 2-13"/><path d="M53 60c-11 2-17-5-13-11 3-5 10-4 13 2"/>',
    "package": '<path d="M60 18l36 18v44L60 100 24 80V36z"/><path d="M24 36l36 18 36-18M60 54v46"/>',
    "scan": '<circle cx="64" cy="52" r="18"/><path d="M77 65l18 18"/><path d="M40 34L28 52l12 18M54 34l-6 36" opacity=".45"/>',
    "pipeline": '<rect x="6" y="46" width="24" height="28" rx="5"/><rect x="48" y="46" width="24" height="28" rx="5" opacity=".45"/><rect x="84" y="46" width="24" height="28" rx="5"/><path d="M30 60h16M40 54l6 6-6 6M72 60h10M78 54l6 6-6 6"/>',
    "target": '<circle cx="54" cy="62" r="32"/><circle cx="54" cy="62" r="18" opacity=".45"/><circle cx="54" cy="62" r="5" fill="var(--accent)" stroke="none"/><path d="M92 24L68 48"/><path d="M78 22h16v16"/>',
    "area": '<path d="M16 90h88"/><path d="M16 90c28 0 38-56 88-56"/><path d="M34 90V70M54 90V54M74 90V44M94 90V38" opacity=".45"/>',
    "dice": '<rect x="26" y="26" width="68" height="68" rx="12"/><circle cx="42" cy="42" r="4" fill="var(--accent)" stroke="none"/><circle cx="60" cy="60" r="4" fill="var(--accent)" stroke="none"/><circle cx="78" cy="78" r="4" fill="var(--accent)" stroke="none"/>',
    "curve": '<path d="M12 90h96"/><path d="M12 90c22 0 24-54 48-54s26 54 48 54"/>',
    "trend": '<path d="M14 96h92" opacity=".35"/><circle cx="28" cy="76" r="4"/><circle cx="44" cy="70" r="4"/><circle cx="62" cy="52" r="4"/><circle cx="78" cy="46" r="4"/><circle cx="94" cy="30" r="4"/><path d="M20 84l80-60"/>',
    "cable": '<rect x="16" y="40" width="56" height="40" rx="5"/><path d="M72 50h18M72 70h18"/><path d="M28 46v8M40 46v8M52 46v8M64 46v8" opacity=".45"/><path d="M90 60h16"/>',
    "frame": '<rect x="8" y="44" width="104" height="32" rx="4"/><path d="M28 44v32M52 44v32M76 44v32M96 44v32" opacity=".45"/><circle cx="18" cy="60" r="2.5" fill="var(--accent)" stroke="none"/>',
    "switch": '<rect x="30" y="44" width="60" height="32" rx="6"/><path d="M42 76v10M54 76v10M66 76v10M78 76v10" opacity=".45"/><path d="M18 60h10M24 54l-6 6 6 6M102 60H90M90 54l6 6-6 6"/>',
    "packet": '<rect x="14" y="34" width="92" height="52" rx="6"/><path d="M14 40l46 32 46-32"/><path d="M22 82l22-22M98 82L76 60" opacity=".35"/>',
    "ip": '<rect x="8" y="46" width="20" height="18" rx="4"/><rect x="36" y="46" width="20" height="18" rx="4"/><rect x="64" y="46" width="20" height="18" rx="4"/><rect x="92" y="46" width="20" height="18" rx="4"/><path d="M28 55h8M56 55h8M84 55h8"/>',
    "mask": '<rect x="14" y="30" width="92" height="60" rx="6"/><path d="M60 30v60" stroke-dasharray="5 6"/><path d="M14 60h92" opacity=".35"/><circle cx="36" cy="45" r="3" fill="var(--accent)" stroke="none"/><circle cx="36" cy="75" r="3" fill="var(--accent)" stroke="none"/><circle cx="84" cy="45" r="3" fill="var(--accent)" stroke="none"/><circle cx="84" cy="75" r="3" fill="var(--accent)" stroke="none"/>',
    "tcp": '<rect x="14" y="28" width="30" height="22" rx="5"/><rect x="76" y="70" width="30" height="22" rx="5"/><path d="M29 50v18h40M62 62l8 6-8 6M91 70V52H51M59 46l-8 6 8 6"/>',
    "socket": '<rect x="14" y="40" width="34" height="40" rx="6"/><path d="M48 52h16M48 68h16"/><rect x="72" y="40" width="34" height="40" rx="6"/><circle cx="64" cy="60" r="4" fill="var(--accent)" stroke="none"/>',
    "dns": '<circle cx="60" cy="60" r="30"/><path d="M30 60h60M60 30c12 12 12 48 0 60M60 30c-12 12-12 48 0 60" opacity=".45"/><circle cx="86" cy="34" r="7"/>',
    "dhcp": '<rect x="34" y="14" width="52" height="24" rx="5"/><path d="M52 38v14M44 46l8 8 8-8M60 52v16M52 62l8 8 8-8M76 38v14M68 46l8 8 8-8"/>',
    "vpn": '<path d="M20 78c20-42 60-42 80 0" stroke-dasharray="6 7"/><rect x="8" y="76" width="24" height="18" rx="4"/><rect x="88" y="76" width="24" height="18" rx="4"/><rect x="46" y="30" width="28" height="22" rx="4"/><path d="M53 30v-6a7 7 0 0114 0v6"/>',
    "wifi": '<path d="M26 52a48 48 0 0168 0"/><path d="M40 66a30 30 0 0140 0"/><path d="M52 80a14 14 0 0116 0"/><circle cx="60" cy="92" r="4" fill="var(--accent)" stroke="none"/>',
    "process": '<circle cx="24" cy="60" r="9"/><path d="M33 60h12"/><path d="M45 60c12 0 10-26 28-26M45 60h28M45 60c12 0 10 26 28 26"/><circle cx="81" cy="34" r="8"/><circle cx="81" cy="60" r="8"/><circle cx="81" cy="86" r="8"/>',
    "folder": '<path d="M14 32h34l8 10h50v50H14z"/><path d="M14 50h92" opacity=".45"/>',
    "normalize": '<rect x="12" y="24" width="48" height="18" rx="4"/><rect x="12" y="56" width="48" height="18" rx="4"/><path d="M60 33c10 0 8 27 18 27M60 65c10 0 8-5 18-5"/><rect x="78" y="46" width="30" height="20" rx="4"/>',
    "matrix": '<path d="M30 26H18v68h12M90 26h12v68H90"/><circle cx="38" cy="42" r="3" fill="var(--accent)" stroke="none"/><circle cx="60" cy="42" r="3" fill="var(--accent)" stroke="none"/><circle cx="82" cy="42" r="3" fill="var(--accent)" stroke="none"/><circle cx="38" cy="60" r="3" fill="var(--accent)" stroke="none"/><circle cx="60" cy="60" r="3" fill="var(--accent)" stroke="none"/><circle cx="82" cy="60" r="3" fill="var(--accent)" stroke="none"/><circle cx="38" cy="78" r="3" fill="var(--accent)" stroke="none"/><circle cx="60" cy="78" r="3" fill="var(--accent)" stroke="none"/><circle cx="82" cy="78" r="3" fill="var(--accent)" stroke="none"/>',
    "default": '<circle cx="42" cy="48" r="18"/><circle cx="78" cy="72" r="22" opacity=".45"/><path d="M24 96h72" opacity=".4"/>',
}


def build_course(root: Path) -> Path:
    c = load_course(root / "course.json")
    dist = root / "dist"
    dist.mkdir(exist_ok=True)
    availability = load_availability(root)
    cards = is_cards(c)
    items, written = [], 0
    slot = 1
    for ch in c.get("chapters", []):
        dirname = chapter_dir(ch)
        if cards:
            lesson = f'{int(ch.get("n") or len(items) + 1):02d}'
        else:
            pairs = max(1, round(int(ch.get("minutes") or 90) / 90))
            lesson = f"{slot}" if pairs == 1 else f"{slot}<br>-<br>{slot + pairs - 1}"
            slot += pairs
        d = root / "chapters" / dirname
        md = d / "chapter.md"
        open_ = is_open(c, dirname, availability)
        locked = md.exists() and not open_
        link = None
        if md.exists() and open_:
            r = subprocess.run([sys.executable, str(HERE / "build_chapter.py"), str(md)], capture_output=True, text=True)
            print(r.stdout.strip() or r.stderr.strip())
            if r.returncode == 0:
                link = f"{dirname}.html"
                written += 1
        elif locked:
            stale = dist / f"{dirname}.html"
            if stale.exists():
                stale.unlink()
        ST = {"planned": "план", "drafted": "черновик", "figures-pending": "фигуры готовятся", "published": "готово"}
        if locked:
            status = " · закрыто"
        else:
            status = "" if link else f' · {esc(ST.get(ch.get("status", "planned"), ch.get("status", "план")))}'
        title = esc(ch["title"])
        classes = []
        if locked:
            classes.append("locked")
        if ch.get("pinned"):
            classes.append("pinned")
        cls = f' class="{" ".join(classes)}"' if classes else ""
        if cards:
            label = ch.get("label") or (
                "Справочник" if ch.get("role") == "info"
                else "Варианты" if ch.get("role") == "variants"
                else "Методичка")
            mins = esc(label) + status
        else:
            mins = status.strip(" · ")
        mins_html = f'<div class="mins">{mins}</div>' if mins else ""
        inner = (f'<div class="n">{lesson}</div><h3>{title}</h3>'
                 f'{mins_html}'
                 f'<p>{esc(ch.get("summary", ""))}</p>{card_art(ch)}')
        card = (f'<a class="lesson-card" href="{link}">{inner}</a>' if link
                else f'<div class="lesson-card lesson-card-static">{inner}</div>')
        items.append(f'<li{cls}>{card}</li>')

    n_ch = len(c.get("chapters", []))
    slots = lesson_slots(c.get("chapters", []))
    if cards:
        meta = " · ".join(x for x in [
            f"{n_ch} {plural_sections(n_ch)}" if n_ch else None,
            esc(c.get("assessment", "")),
            summary(c, availability),
        ] if x)
    else:
        meta = " · ".join(x for x in [
            f"{slots} {plural_lessons(slots)}" if slots else None,
            esc(c.get("assessment", "")),
            summary(c, availability),
        ] if x)
    outcomes = ""
    if c.get("outcomes"):
        outcomes_title = "Что вы освоите" if cards else "В результате обучения вы сможете"
        outcomes = f'<section class="outcomes"><b>{outcomes_title}</b><ul>' + "".join(
            f"<li>{esc(o)}</li>" for o in c["outcomes"]) + "</ul></section>"
    prereq = ""
    if c.get("prerequisites"):
        prereq_title = "Что нужно знать заранее" if cards else "Требуется предварительно"
        prereq = f'<section class="outcomes"><b>{prereq_title}</b><ul>' + "".join(
            f"<li>{esc(o)}</li>" for o in c["prerequisites"]) + "</ul></section>"
    price_pill = f'<span class="pill">{esc(price(c))}</span>' if price(c) else ""
    code = c.get("code", "")
    glyph_class = "glyph" + (f" {code_class(code)}" if code_class(code) else "")
    accent = c.get("accent", "#D04A28")
    seed = (sum(ord(ch) for ch in c.get("slug", "")) % 97) / 97.0
    for stale in dist.glob("Учебный_план_*.xlsx"):
        stale.unlink()
    plan_name = plan_filename(c)
    write_plan_xlsx(c, dist / plan_name)
    if cards:
        plan_heading = "Разделы подготовки"
        plan_intro = ('<article class="prose"><p>Материалы собраны в разделы: предварительная '
                      'подготовка с разбором первых трёх заданий, общая информация об экзамене, '
                      'методички по шести заданиям и варианты для практики. В каждом разделе '
                      'указано, что открыть, какие файлы создать и какие команды выполнить.</p></article>')
    else:
        plan_heading = "Учебный план"
        plan_intro = ""
    body = f"""<main class="page">{rail(back="#year", excel=plan_name)}
<header class="hero hero-course" data-shader data-accent="{esc(accent)}" data-seed="{seed:.3f}">
<canvas class="shader-bg" width="820" height="300" aria-hidden="true" style="background:linear-gradient(135deg,#08090D,{esc(accent)} 58%,#08090D)"></canvas>
<div class="badges">{price_pill}</div><div class="meta">{esc(meta)}</div>
<h1>{esc(c['title'])}</h1><p class="dek">{esc(c.get('tagline', ''))}</p>
<div class="{glyph_class}" aria-hidden="true">{esc(code)}</div></header>
    {outcomes}{prereq}
<article class="prose"><h2 class="nonum" style="margin-top:36px">{plan_heading}</h2></article>
{plan_intro}
<ol class="syllabus">{''.join(items)}</ol></main>"""
    out = dist / "index.html"
    out.write_text(page(c["title"], body, accent_vars(c), "", SHADER_JS), encoding="utf-8")
    print(f"wrote {out}: {n_ch} chapters, {written} written")
    return out


def build_catalog(root: Path) -> Path:
    courses = [load_course(p) for p in sorted(root.glob("*/course.json"))]
    courses.sort(key=lambda c: (c.get("status") != "available", c.get("order", 99)))
    cards = []
    for c in courses:
        slots = lesson_slots(c.get("chapters", []))
        ch_label = f"{slots} {plural_lessons(slots)}" if slots else ""
        avail = c.get("status") == "available"
        style = (f"--cl-accent:{c['accent']};--cl-tint:{c['tint']};"
                 f"--cd-accent:{c.get('accentDark', c['accent'])};--cd-tint:{c.get('tintDark', c['tint'])}")
        code = c.get("code", "")
        glyph_class = "glyph" + (f" {code_class(code)}" if code_class(code) else "")
        cards.append(f"""<a class="course-card" data-status="{'available' if avail else 'soon'}" href="{esc(c['slug'])}/index.html" style="{style}">
<div class="art"><span class="pill{' dark' if avail else ''}">{'Доступно' if avail else 'Готовится'}</span><span class="ch">{ch_label}</span>
<div class="{glyph_class}" aria-hidden="true">{esc(code)}</div></div>
<div class="body"><h3>{esc(c['title'])}</h3><p>{esc(c.get('tagline', ''))}</p><div class="spec">{esc(spec_line(c))}</div>
<div class="foot"><span class="price">{esc(price(c))}</span><span class="btn{' primary' if avail else ''}">{'Открыть' if avail else 'Готовится'}</span></div></div></a>""")
    body = f"""<main class="catalog"><div class="catalog-head"><div class="filters" role="group" aria-label="Фильтр курсов">
<button aria-pressed="true" data-f="all">Все</button><button aria-pressed="false" data-f="available">Доступные</button><button aria-pressed="false" data-f="soon">Готовятся</button></div>
<span class="count">{len(courses)} курсов</span></div><div class="grid">{''.join(cards)}</div></main>"""
    css = """.course-card{--c-accent:var(--cl-accent);--c-tint:var(--cl-tint)}
@media (prefers-color-scheme: dark){:root:not([data-theme=light]) .course-card{--c-accent:var(--cd-accent);--c-tint:var(--cd-tint)}}
:root[data-theme=dark] .course-card{--c-accent:var(--cd-accent);--c-tint:var(--cd-tint)}"""
    js = """document.querySelectorAll('.filters button').forEach(function(b){b.onclick=function(){
document.querySelectorAll('.filters button').forEach(function(x){x.setAttribute('aria-pressed', x===b)});
var f=b.dataset.f, n=0; document.querySelectorAll('.course-card').forEach(function(c){var on=f==='all'||c.dataset.status===f; c.style.display=on?'':'none'; n+=on});
document.querySelector('.count').textContent=n+' курсов';}});"""
    out = root / "catalog.html"
    out.write_text(page("Courses", body, "", css, js), encoding="utf-8")
    print(f"wrote {out}: {len(courses)} courses")
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = Path(sys.argv[1]).resolve()
    if "--catalog" in sys.argv:
        for cj in sorted(root.glob("*/course.json")):
            build_course(cj.parent)
        build_catalog(root)
    else:
        build_course(root)


if __name__ == "__main__":
    main()
