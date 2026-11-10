"""Rebuild the 30 variant workbooks as readable structured forms.

The source data lives in courses/4/ДЭ-2027/reports/variants.json. Each variant
gets four workbooks: order, production order, specification and prices. The
layout follows the paper forms: a merged title, labelled header blocks, tables
with visible borders and formatted dates and money.
"""

from __future__ import annotations

import json
import zipfile
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
VARIANTS = ROOT / "courses" / "4" / "ДЭ-2027" / "reports" / "variants.json"
OUT = ROOT / "courses" / "4" / "ДЭ-2027" / "reports" / "variants"

ORDER_DATE = date(2027, 3, 15)
DUE_DATE = date(2027, 3, 22)
LAUNCH_DATE = date(2027, 3, 16)
PRICE_DATE = date(2027, 3, 1)

TITLE_FILL = PatternFill("solid", fgColor="FFFFFF")
SUBTITLE_FILL = PatternFill("solid", fgColor="FFFFFF")
SECTION_FILL = PatternFill("solid", fgColor="FFFFFF")
HEADER_FILL = PatternFill("solid", fgColor="FFFFFF")
LABEL_FILL = PatternFill("solid", fgColor="FFFFFF")
INPUT_FILL = PatternFill("solid", fgColor="FFFFFF")
WHITE = "000000"
thin = Side(style="thin", color="404040")
medium = Side(style="medium", color="000000")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
OUTER = Border(left=medium, right=medium, top=medium, bottom=medium)

TITLE_FONT = Font(name="Arial", size=14, bold=True, color="000000")
SUBTITLE_FONT = Font(name="Arial", size=9, italic=True, color="404040")
SECTION_FONT = Font(name="Arial", size=9, bold=True, color="000000")
HEADER_FONT = Font(name="Arial", size=9, bold=True, color="000000")
BODY_FONT = Font(name="Arial", size=8)
VALUE_FONT = Font(name="Arial", size=9, bold=True)
LABEL_FONT = Font(name="Arial", size=9)


def merge_title(ws, row: int, last_col: int, text: str) -> None:
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=last_col)
    cell = ws.cell(row=row, column=1, value=text)
    cell.fill = TITLE_FILL
    cell.font = TITLE_FONT
    cell.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[row].height = 44


def merge_subtitle(ws, row: int, last_col: int, text: str) -> None:
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=last_col)
    cell = ws.cell(row=row, column=1, value=text)
    cell.fill = SUBTITLE_FILL
    cell.font = SUBTITLE_FONT
    cell.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[row].height = 13


def section(ws, row: int, last_col: int, text: str) -> None:
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=last_col)
    cell = ws.cell(row=row, column=1, value=text)
    cell.fill = SECTION_FILL
    cell.font = SECTION_FONT
    cell.alignment = Alignment(horizontal="left", vertical="center")
    cell.border = Border(bottom=Side(style="medium", color="000000"))
    ws.row_dimensions[row].height = 16


def label_value(ws, row: int, pairs: list[tuple[str, object]], last_col: int) -> None:
    """Write label/value pairs across the row, two columns per pair."""
    col = 1
    for label, value in pairs:
        c = ws.cell(row=row, column=col, value=label)
        c.font = LABEL_FONT
        c.fill = LABEL_FILL
        c.border = BORDER
        c.alignment = Alignment(vertical="center", wrap_text=True)
        col += 1
        if col > last_col:
            break
        v = ws.cell(row=row, column=col, value=value)
        v.font = VALUE_FONT
        v.border = BORDER
        v.alignment = Alignment(vertical="center", wrap_text=True)
        col += 1
    for c in range(col, last_col + 1):
        cell = ws.cell(row=row, column=c)
        cell.border = BORDER
    ws.row_dimensions[row].height = 36


def merged_label(ws, row: int, c1: int, c2: int, text: str,
                 bold: bool = False, align: str = "left") -> None:
    font = VALUE_FONT if bold else LABEL_FONT
    if c2 > c1:
        ws.merge_cells(start_row=row, start_column=c1, end_row=row, end_column=c2)
    cell = ws.cell(row=row, column=c1, value=text)
    cell.font = font
    cell.alignment = Alignment(horizontal=align, vertical="center", wrap_text=True)
    for c in range(c1, c2 + 1):
        ws.cell(row=row, column=c).border = BORDER
        ws.cell(row=row, column=c).font = font
    ws.row_dimensions[row].height = 30


def data_rows(ws, start_row: int, rows: list[list[object]],
              formats: list[str | None], widths: list[float]) -> None:
    for i, width in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = width
    for r, values in enumerate(rows, start_row):
        for i, value in enumerate(values, 1):
            cell = ws.cell(row=r, column=i, value=value)
            cell.font = BODY_FONT
            cell.border = BORDER
            cell.alignment = Alignment(vertical="top", wrap_text=i == 1)
            fmt = formats[i - 1]
            if fmt:
                cell.number_format = fmt
        ws.row_dimensions[r].height = 15


def table(ws, start_row: int, headers: list[str], rows: list[list[object]],
          formats: list[str | None], widths: list[float]) -> int:
    for i, header in enumerate(headers, 1):
        cell = ws.cell(row=start_row, column=i, value=header)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
        ws.column_dimensions[get_column_letter(i)].width = widths[i - 1]
    ws.row_dimensions[start_row].height = 30

    for r, values in enumerate(rows, start_row + 1):
        for i, value in enumerate(values, 1):
            cell = ws.cell(row=r, column=i, value=value)
            cell.font = BODY_FONT
            cell.border = BORDER
            cell.alignment = Alignment(vertical="top", wrap_text=i == 1)
            fmt = formats[i - 1]
            if fmt:
                cell.number_format = fmt
        ws.row_dimensions[r].height = 15

    last_row = start_row + len(rows)
    for c in range(1, len(headers) + 1):
        ws.cell(row=last_row, column=c).border = Border(
            left=BORDER.left, right=BORDER.right,
            top=BORDER.top, bottom=medium,
        )
    return last_row


def base_sheet(title: str, subtitle: str, last_col: int):
    wb = Workbook()
    ws = wb.active
    ws.title = "Документ"
    ws.sheet_view.showGridLines = False
    merge_title(ws, 1, last_col, title)
    merge_subtitle(ws, 2, last_col, subtitle)
    ws.row_dimensions[3].height = 8
    return wb, ws


def variant_subtitle(v: dict) -> str:
    return f"Учебный вариант {v['id']} · {v['domain']} · {v['brand']}"


def save(wb: Workbook, path: Path) -> None:
    wb.save(path)


def build_order(v: dict, path: Path) -> None:
    wb, ws = base_sheet("Заказ покупателя", variant_subtitle(v), 8)
    customer = v["customers"][0]
    merged_label(ws, 4, 1, 2, "Номер заказа")
    merged_label(ws, 4, 3, 3, v["id"] + "-01", bold=True)
    merged_label(ws, 4, 4, 5, "Дата")
    merged_label(ws, 4, 6, 8, ORDER_DATE, bold=True)
    merged_label(ws, 5, 1, 2, "Срок")
    merged_label(ws, 5, 3, 3, DUE_DATE, bold=True)
    merged_label(ws, 5, 4, 5, "Код заказчика")
    merged_label(ws, 5, 6, 8, customer["id"], bold=True)
    merged_label(ws, 7, 1, 2, "Изготовитель")
    merged_label(ws, 7, 3, 5, v["brand"], bold=True)
    merged_label(ws, 7, 6, 6, "Заказчик")
    merged_label(ws, 7, 7, 8, customer["name"], bold=True)
    ws.cell(row=4, column=6).number_format = "DD.MM.YYYY"
    ws.cell(row=5, column=3).number_format = "DD.MM.YYYY"

    section(ws, 9, 8, "Продукция")
    table(ws, 10, ["№", "Товары (работы, услуги)", "Код", "Кол-во", "Ед.", "Цена", "Скидка", "Сумма"],
          [[1, v["product"], "P-01", v["qty"], "ед.", 700.00, 0.00, v["qty"] * 700.00]],
          [None, None, None, "0.###", None, "#,##0.00", "#,##0.00", "#,##0.00"],
          [4, 30, 14, 14, 9, 14, 12, 14])
    ws.cell(row=12, column=7, value="Итого:").font = VALUE_FONT
    ws.cell(row=12, column=7).alignment = Alignment(horizontal="right")
    ws.cell(row=12, column=8, value=v["qty"] * 700.00).number_format = "#,##0.00"
    ws.cell(row=12, column=8).font = VALUE_FONT
    ws.cell(row=12, column=8).border = BORDER
    ws.freeze_panes = "A4"
    save(wb, path)


def build_production(v: dict, path: Path) -> None:
    wb, ws = base_sheet("Заказ на производство", variant_subtitle(v), 6)
    merged_label(ws, 4, 1, 2, "Производственный заказ")
    merged_label(ws, 4, 3, 3, v["id"] + "-P01", bold=True)
    merged_label(ws, 4, 4, 5, "Заказ покупателя")
    merged_label(ws, 4, 6, 6, v["id"] + "-01", bold=True)
    merged_label(ws, 5, 1, 2, "Дата запуска")
    merged_label(ws, 5, 3, 3, LAUNCH_DATE, bold=True)
    merged_label(ws, 5, 4, 4, "Подразделение")
    merged_label(ws, 5, 5, 6, "Основное производство", bold=True)
    ws.cell(row=5, column=3).number_format = "DD.MM.YYYY"

    row = 7
    section(ws, row, 6, "Продукция к выпуску")
    row += 1
    table(ws, row, ["№", "Наименование", "Код", "Кол-во", "Ед."],
          [[1, v["product"], "P-01", v["qty"], "ед."]],
          [None, None, None, "0.###", None], [4, 32, 14, 10, 9])
    row += 3

    section(ws, row, 6, "Потребность в материалах")
    row += 1
    materials = [r for r in v["resources"] if r["kind"] == "material"]
    rows = []
    for i, r in enumerate(materials, 1):
        rows.append([i, r["name"], f"M-{i:02d}", v["qty"] * r["norm"], r["unit"]])
    table(ws, row, ["№", "Наименование", "Код", "Кол-во", "Ед."],
          rows, [None, None, None, "0.###", None], [4, 32, 14, 10, 9])
    row += len(rows) + 2

    section(ws, row, 6, "Технологические операции")
    row += 1
    operations = [r for r in v["resources"] if r["kind"] == "operation"]
    rows = []
    for i, r in enumerate(operations, 1):
        rows.append([i, r["name"], f"O-{i:02d}", v["qty"] * r["time"], r["unit"]])
    table(ws, row, ["№", "Наименование", "Код", "Кол-во", "Ед."],
          rows, [None, None, None, "0.###", None], [4, 32, 14, 10, 9])
    ws.freeze_panes = "A4"
    save(wb, path)


def build_spec(v: dict, path: Path) -> None:
    wb, ws = base_sheet(f'Спецификация "{v["product"]}"', variant_subtitle(v), 4)
    ws.column_dimensions["D"].width = 12
    merged_label(ws, 4, 1, 2, "Изделие")
    merged_label(ws, 4, 3, 4, v["product"], bold=True)
    merged_label(ws, 6, 1, 2, "Изготовитель")
    merged_label(ws, 6, 3, 4, v["brand"], bold=True)
    section(ws, 8, 4, "Состав")
    materials = [r for r in v["resources"] if r["kind"] == "material"]
    rows = [[r["name"], r["unit"], r["norm"]] for r in materials]
    table(ws, 9, ["Ресурс", "Ед. изм.", "Норма расхода"],
          rows, [None, None, "0.###"], [28, 10, 14])
    row = 9 + len(rows) + 2
    section(ws, row, 4, "Технологические операции")
    row += 1
    operations = [r for r in v["resources"] if r["kind"] == "operation"]
    rows = [[r["name"], r["unit"], r["time"]] for r in operations]
    table(ws, row, ["Операция", "Ед. изм.", "Норма времени"],
          rows, [None, None, "0.###"], [28, 10, 14])
    ws.freeze_panes = "A4"
    save(wb, path)


def build_prices(v: dict, path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Документ"
    ws.sheet_view.showGridLines = False
    rows = [[r["name"], r["unit"], r["price"], PRICE_DATE] for r in v["resources"]]
    table(ws, 1, ["Номенклатура", "Ед.", "Цена", "Действует с"],
          rows, [None, None, "#,##0.00", "DD.MM.YYYY"], [30, 10, 14, 14])
    ws.freeze_panes = "A2"
    save(wb, path)


def build_calc(v: dict, path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Документ"
    ws.sheet_view.showGridLines = False
    for col, width in zip("ABCD", [54, 16, 14, 12]):
        ws.column_dimensions[col].width = width

    table(ws, 1, ["Номенклатура", "Количество", "Норма/часы", "Сумма"],
          [[v["product"], v["qty"], None, None]],
          [None, "0.###", "0.###", "#,##0.00"], [54, 16, 14, 12])

    row = 3
    section(ws, row, 4, "Материальные затраты")
    row += 1
    materials = [r for r in v["resources"] if r["kind"] == "material"]
    rows = [[r["name"], v["qty"] * r["norm"], r["norm"], None] for r in materials]
    data_rows(ws, row, rows, [None, "0.###", "0.###", "#,##0.00"], [54, 16, 14, 12])
    row += len(rows) + 1

    section(ws, row, 4, "Технологические операции")
    row += 1
    operations = [r for r in v["resources"] if r["kind"] == "operation"]
    rows = [[r["name"], v["qty"] * r["time"], r["time"], None] for r in operations]
    data_rows(ws, row, rows, [None, "0.###", "0.###", "#,##0.00"], [54, 16, 14, 12])
    row += len(rows) + 1

    ws.cell(row=row, column=1, value="Итого").font = VALUE_FONT
    ws.cell(row=row, column=4).number_format = "#,##0.00"
    for c in range(1, 5):
        ws.cell(row=row, column=c).border = BORDER
    save(wb, path)


def build_archive(folder: Path, variant_id: str) -> None:
    names = [
        "Заказ покупателя.xlsx",
        "Заказ на производство.xlsx",
        "Спецификация.xlsx",
        "Цены.xlsx",
        "Расчет стоимости.xlsx",
        "Заказчики.json",
    ]
    archive = folder / f"{variant_id}_исходные_данные.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for name in names:
            path = folder / name
            if path.exists():
                z.write(path, name)


def main() -> None:
    data = json.loads(VARIANTS.read_text(encoding="utf-8"))
    for v in data:
        # V01 is supplied by the teacher as a ready set; do not overwrite it.
        if v["id"] == "V01":
            continue
        folder = OUT / v["id"]
        folder.mkdir(parents=True, exist_ok=True)
        build_order(v, folder / "Заказ покупателя.xlsx")
        build_production(v, folder / "Заказ на производство.xlsx")
        build_spec(v, folder / "Спецификация.xlsx")
        build_prices(v, folder / "Цены.xlsx")
        build_calc(v, folder / "Расчет стоимости.xlsx")
        for csv_name in ("customers.csv", "notes.csv", "resources.csv"):
            csv_path = folder / csv_name
            if csv_path.exists():
                csv_path.unlink()
        build_archive(folder, v["id"])
    print(f"formatted {len(data) - 1} variants, V01 kept as supplied")


if __name__ == "__main__":
    main()
