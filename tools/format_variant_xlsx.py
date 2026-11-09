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

TITLE_FILL = PatternFill("solid", fgColor="1F3864")
SUBTITLE_FILL = PatternFill("solid", fgColor="D9E2F3")
SECTION_FILL = PatternFill("solid", fgColor="DDEBF7")
HEADER_FILL = PatternFill("solid", fgColor="2F5597")
LABEL_FILL = PatternFill("solid", fgColor="F2F2F2")
INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")
WHITE = "FFFFFF"
thin = Side(style="thin", color="7F7F7F")
medium = Side(style="medium", color="1F3864")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
OUTER = Border(left=medium, right=medium, top=medium, bottom=medium)

TITLE_FONT = Font(name="Arial", size=14, bold=True, color=WHITE)
SUBTITLE_FONT = Font(name="Arial", size=10, italic=True, color="1F3864")
SECTION_FONT = Font(name="Arial", size=11, bold=True, color="1F3864")
HEADER_FONT = Font(name="Arial", size=10, bold=True, color=WHITE)
BODY_FONT = Font(name="Arial", size=10)
LABEL_FONT = Font(name="Arial", size=10, bold=True)


def merge_title(ws, row: int, last_col: int, text: str) -> None:
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=last_col)
    cell = ws.cell(row=row, column=1, value=text)
    cell.fill = TITLE_FILL
    cell.font = TITLE_FONT
    cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[row].height = 30


def merge_subtitle(ws, row: int, last_col: int, text: str) -> None:
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=last_col)
    cell = ws.cell(row=row, column=1, value=text)
    cell.fill = SUBTITLE_FILL
    cell.font = SUBTITLE_FONT
    cell.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[row].height = 22


def section(ws, row: int, last_col: int, text: str) -> None:
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=last_col)
    cell = ws.cell(row=row, column=1, value=text)
    cell.fill = SECTION_FILL
    cell.font = SECTION_FONT
    cell.alignment = Alignment(horizontal="left", vertical="center")
    cell.border = Border(bottom=Side(style="medium", color="2F5597"))
    ws.row_dimensions[row].height = 22


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
        v.font = BODY_FONT
        v.border = BORDER
        v.alignment = Alignment(vertical="center", wrap_text=True)
        col += 1
    for c in range(col, last_col + 1):
        cell = ws.cell(row=row, column=c)
        cell.border = BORDER
    ws.row_dimensions[row].height = 30


def table(ws, start_row: int, headers: list[str], rows: list[list[object]],
          formats: list[str | None], widths: list[float]) -> int:
    for i, header in enumerate(headers, 1):
        cell = ws.cell(row=start_row, column=i, value=header)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
        ws.column_dimensions[get_column_letter(i)].width = widths[i - 1]
    ws.row_dimensions[start_row].height = 34

    for r, values in enumerate(rows, start_row + 1):
        for i, value in enumerate(values, 1):
            cell = ws.cell(row=r, column=i, value=value)
            cell.font = BODY_FONT
            cell.border = BORDER
            cell.alignment = Alignment(vertical="top", wrap_text=i == 1)
            fmt = formats[i - 1]
            if fmt:
                cell.number_format = fmt
        ws.row_dimensions[r].height = 24

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
    wb, ws = base_sheet("Заказ покупателя", variant_subtitle(v), 4)
    customer = v["customers"][0]
    label_value(ws, 4, [
        ("Номер заказа", v["id"] + "-01"),
        ("Дата", ORDER_DATE),
    ], 4)
    ws.cell(row=4, column=4).number_format = "DD.MM.YYYY"
    label_value(ws, 5, [
        ("Срок", DUE_DATE),
        ("Код заказчика", customer["id"]),
    ], 4)
    ws.cell(row=5, column=2).number_format = "DD.MM.YYYY"
    label_value(ws, 7, [
        ("Изготовитель", v["brand"]),
        ("Заказчик", customer["name"]),
    ], 4)
    section(ws, 9, 4, "Продукция")
    table(ws, 10, ["Продукция", "Единица", "Количество", "Примечание"],
          [[v["product"], "ед.", v["qty"], "Нормативная стоимость рассчитывается в задании 3"]],
          [None, None, "0.###", None], [30, 14, 18, 32])
    ws.freeze_panes = "A4"
    save(wb, path)


def build_production(v: dict, path: Path) -> None:
    wb, ws = base_sheet("Заказ на производство", variant_subtitle(v), 4)
    label_value(ws, 4, [
        ("Производственный заказ", v["id"] + "-P01"),
        ("Заказ покупателя", v["id"] + "-01"),
    ], 4)
    label_value(ws, 5, [
        ("Дата запуска", LAUNCH_DATE),
        ("Подразделение", "Основное производство"),
    ], 4)
    ws.cell(row=5, column=2).number_format = "DD.MM.YYYY"
    section(ws, 7, 4, "Продукция к выпуску")
    table(ws, 8, ["Продукция", "Единица", "Количество", "Спецификация"],
          [[v["product"], "ед.", v["qty"], "Нормы на одну единицу"]],
          [None, None, "0.###", None], [36, 12, 14, 30])
    section(ws, 11, 4, "Потребность в ресурсах")
    rows = []
    for r in v["resources"]:
        plan = v["qty"] * (r["norm"] if r["kind"] == "material" else r["time"])
        rows.append([r["name"], "материал" if r["kind"] == "material" else "операция", plan, r["unit"]])
    table(ws, 12, ["Ресурс", "Вид", "Плановый расход", "Единица"],
          rows, [None, None, "0.###", None], [36, 16, 18, 12])
    ws.freeze_panes = "A4"
    save(wb, path)


def build_spec(v: dict, path: Path) -> None:
    wb, ws = base_sheet("Спецификация", variant_subtitle(v), 5)
    label_value(ws, 4, [
        ("Продукция", v["product"]),
        ("Нормы", "На одну единицу"),
    ], 5)
    section(ws, 6, 5, "Состав изделия")
    rows = []
    for r in v["resources"]:
        rows.append([
            r["name"],
            "материал" if r["kind"] == "material" else "операция",
            r["unit"],
            r["norm"],
            r["time"] if r["kind"] == "operation" else None,
        ])
    table(ws, 7, ["Ресурс", "Вид", "Единица", "Норма расхода", "Часы на единицу"],
          rows, [None, None, None, "0.###", "0.###"], [34, 14, 12, 16, 18])
    ws.freeze_panes = "A8"
    save(wb, path)


def build_prices(v: dict, path: Path) -> None:
    wb, ws = base_sheet("Цены", variant_subtitle(v), 4)
    section(ws, 4, 4, "Действующие цены")
    rows = [[r["name"], r["price"], r["unit"], PRICE_DATE] for r in v["resources"]]
    table(ws, 5, ["Ресурс", "Цена, руб./ед.", "Единица", "Действует с"],
          rows, [None, "#,##0.00", None, "DD.MM.YYYY"], [34, 16, 12, 16])
    ws.freeze_panes = "A6"
    save(wb, path)


def build_calc(v: dict, path: Path) -> None:
    wb, ws = base_sheet("Расчет стоимости заказа", variant_subtitle(v), 8)
    for col, width in zip("ABCDEFGH", [28, 15, 18, 12, 11, 12, 13, 17]):
        ws.column_dimensions[col].width = width

    label_value(ws, 4, [("Заказ", v["id"] + "-01")], 8)
    ws.cell(row=4, column=3, value="Продукция").font = LABEL_FONT
    ws.cell(row=4, column=3).fill = LABEL_FILL
    ws.cell(row=4, column=3).border = BORDER
    ws.cell(row=4, column=3).alignment = Alignment(vertical="center", wrap_text=True)
    ws.merge_cells(start_row=4, start_column=4, end_row=4, end_column=8)
    product = ws.cell(row=4, column=4, value=v["product"])
    product.font = BODY_FONT
    product.alignment = Alignment(vertical="center", wrap_text=True)

    label_value(ws, 5, [("Количество изделий", v["qty"])], 8)
    ws.cell(row=5, column=3, value="Дата заказа").font = LABEL_FONT
    ws.cell(row=5, column=3).fill = LABEL_FILL
    ws.cell(row=5, column=3).border = BORDER
    ws.cell(row=5, column=3).alignment = Alignment(vertical="center", wrap_text=True)
    date_cell = ws.cell(row=5, column=4, value=ORDER_DATE)
    date_cell.font = BODY_FONT
    date_cell.border = BORDER
    date_cell.number_format = "DD.MM.YYYY"
    date_cell.alignment = Alignment(vertical="center")

    section(ws, 7, 8, "Данные для расчета")
    rows = []
    for r in v["resources"]:
        rows.append([
            r["name"],
            "материал" if r["kind"] == "material" else "операция",
            r["unit"],
            r["norm"],
            r["time"] if r["kind"] == "operation" else None,
            r["price"],
            v["qty"],
            None,
        ])
    table(ws, 8, ["Ресурс", "Вид", "Ед.", "Норма", "Часы", "Цена", "Количество", "Стоимость строки"],
          rows, [None, None, None, "0.###", "0.###", "#,##0.00", "0.###", "#,##0.00"],
          [28, 15, 18, 12, 11, 12, 13, 17])
    last = 8 + len(rows)
    ws.cell(row=last + 1, column=7, value="Итого:").font = LABEL_FONT
    ws.cell(row=last + 1, column=7).alignment = Alignment(horizontal="right")
    ws.cell(row=last + 1, column=8).number_format = "#,##0.00"
    ws.cell(row=last + 1, column=8).fill = INPUT_FILL
    ws.cell(row=last + 1, column=8).border = BORDER
    for c in range(1, 9):
        ws.cell(row=last + 1, column=c).border = BORDER
    for r in range(9, last + 2):
        ws.cell(row=r, column=8).fill = INPUT_FILL
    note = ws.cell(row=last + 3, column=1,
                   value="Стоимость строки = количество изделий × норма × цена. "
                         "Для операции вместо нормы используется время в часах. "
                         "Итог округлить до копеек.")
    note.font = Font(name="Arial", size=9, italic=True, color="595959")
    note.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=last + 3, start_column=1, end_row=last + 3, end_column=8)
    ws.row_dimensions[last + 3].height = 32
    ws.freeze_panes = "A9"
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
    print(f"formatted {len(data)} variants")


if __name__ == "__main__":
    main()
