#!/usr/bin/env python3
"""Build the source data of a variant in the exam file set.

KIM 09.02.07-5-2027 gives the customer documents as five Excel books and one
JSON file:

    Заказ покупателя.xlsx
    Заказ на производство.xlsx
    Спецификация.xlsx
    Цены.xlsx
    Расчет стоимости.xlsx
    Заказчики.json

The script writes that set into every ``reports/variants/Vxx`` folder, packs it
into ``reports/variants/Vxx.zip`` and repeats the same six files for the three
preparation variants under ``reports/prep/Vxx`` with ``reports/prep/Vxx.zip``.

Existing books in ``reports/variants`` are not rewritten: the script only adds a
missing file, so rerunning it does not churn binary history. The preparation set
and the archives are rebuilt on every run.

Run from the repository root:

    python courses/4/ДЭ-2027/reports/make_prep_data.py
"""

import json
import zipfile
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

HERE = Path(__file__).resolve().parent
REPORTS = HERE
VARIANTS = REPORTS / "variants"
PREP = REPORTS / "prep"
DATA = REPORTS / "variants.json"

ORDER_DATE = date(2027, 3, 15)
DUE_DATE = date(2027, 3, 22)
LAUNCH_DATE = date(2027, 3, 16)
PRICE_DATE = date(2027, 3, 1)
ZIP_DATE = (2027, 3, 1, 0, 0, 0)

EXAM_FILES = (
    "Заказ покупателя.xlsx",
    "Заказ на производство.xlsx",
    "Спецификация.xlsx",
    "Цены.xlsx",
    "Расчет стоимости.xlsx",
    "Заказчики.json",
)

HEAD_FONT = Font(bold=True, color="FFFFFF")
HEAD_FILL = PatternFill("solid", fgColor="A61F32")
NUM = "0.###"
MONEY = "0.00"
DATE = "dd.mm.yyyy"


def dec(value) -> Decimal:
    return Decimal(str(value))


def money(value) -> float:
    return float(dec(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def quantity(value) -> float:
    value = dec(value).normalize()
    return int(value) if value == value.to_integral_value() else float(value)


def new_sheet(widths) -> openpyxl.worksheet.worksheet.Worksheet:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Данные"
    ws.sheet_view.showGridLines = False
    for index, width in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(index)].width = width
    return ws


def save(ws, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ws.parent.save(path)


def head(ws, row: int, values) -> None:
    for column, value in enumerate(values, 1):
        cell = ws.cell(row=row, column=column, value=value)
        cell.font = HEAD_FONT
        cell.fill = HEAD_FILL


def set_row(ws, row: int, values) -> None:
    for column, value in enumerate(values, 1):
        ws.cell(row=row, column=column, value=value)


def planned(variant: dict, resource: dict) -> float:
    per_unit = resource["time"] if resource["kind"] == "operation" else resource["norm"]
    return quantity(dec(variant["qty"]) * dec(per_unit))


def order_no(variant: dict) -> str:
    return f'{variant["id"]}-01'


def production_no(variant: dict) -> str:
    return f'{variant["id"]}-P01'


def write_customer_order(variant: dict, path: Path) -> None:
    ws = new_sheet([34, 25, 25, 25])
    set_row(ws, 1, ["Авторский учебный вариант", variant["id"], variant["domain"]])
    set_row(ws, 2, ["Номер заказа", "Дата", "Срок", "Код заказчика"])
    set_row(ws, 3, [order_no(variant), ORDER_DATE, DUE_DATE, variant["customers"][0]["id"]])
    set_row(ws, 4, ["Изготовитель", "Заказчик"])
    set_row(ws, 5, [variant["brand"], variant["customers"][0]["name"]])
    set_row(ws, 6, ["Продукция", "Единица", "Количество"])
    set_row(ws, 7, [variant["product"], "ед.", variant["qty"]])
    ws["B3"].number_format = DATE
    ws["C3"].number_format = DATE
    ws["C7"].number_format = NUM
    ws.freeze_panes = "A3"
    save(ws, path)


def write_production_order(variant: dict, path: Path) -> None:
    ws = new_sheet([34, 25, 25])
    set_row(ws, 1, ["Авторский учебный вариант", variant["id"], variant["domain"]])
    set_row(ws, 2, ["Производственный заказ", "Заказ покупателя", "Дата запуска"])
    set_row(ws, 3, [production_no(variant), order_no(variant), LAUNCH_DATE])
    set_row(ws, 4, ["Продукция", "Количество"])
    set_row(ws, 5, [variant["product"], variant["qty"]])
    head(ws, 6, ["Ресурс", "Плановый расход", "Единица"])
    for index, resource in enumerate(variant["resources"], 7):
        set_row(ws, index, [resource["name"], planned(variant, resource), resource["unit"]])
        ws.cell(row=index, column=2).number_format = NUM
    ws["C3"].number_format = DATE
    ws["B5"].number_format = NUM
    ws.freeze_panes = "A7"
    save(ws, path)


def write_specification(variant: dict, path: Path) -> None:
    ws = new_sheet([34, 25, 25, 25, 25])
    set_row(ws, 1, ["Авторский учебный вариант", variant["id"], variant["domain"]])
    set_row(ws, 2, ["Продукция", variant["product"], "На 1 единицу"])
    head(ws, 3, ["Ресурс", "Вид", "Единица", "Норма расхода", "Часы на единицу"])
    for index, resource in enumerate(variant["resources"], 4):
        time = resource["time"] if resource["kind"] == "operation" else None
        set_row(ws, index, [resource["name"], resource["kind"], resource["unit"], resource["norm"], time])
        ws.cell(row=index, column=4).number_format = NUM
        ws.cell(row=index, column=5).number_format = NUM
    ws.freeze_panes = "A4"
    save(ws, path)


def write_prices(variant: dict, path: Path) -> None:
    ws = new_sheet([34, 25, 25, 25])
    set_row(ws, 1, ["Авторский учебный вариант", variant["id"], variant["domain"]])
    head(ws, 2, ["Ресурс", "Цена, руб./ед.", "Единица", "Действует с"])
    for index, resource in enumerate(variant["resources"], 3):
        set_row(ws, index, [resource["name"], resource["price"], resource["unit"], PRICE_DATE])
        ws.cell(row=index, column=2).number_format = MONEY
        ws.cell(row=index, column=4).number_format = DATE
    ws.freeze_panes = "A3"
    save(ws, path)


def write_cost(variant: dict, path: Path) -> None:
    """The customer's own calculation, used to check the SQL query."""
    ws = new_sheet([34, 25, 25, 25, 25, 25, 25])
    set_row(ws, 1, ["Авторский учебный вариант", variant["id"], variant["domain"]])
    set_row(ws, 2, ["Расчет стоимости заказа", order_no(variant), "Дата расчета", ORDER_DATE])
    set_row(ws, 3, ["Предприятие", variant["brand"]])
    set_row(ws, 4, ["Продукция", variant["product"], "Единица", "ед.", "Количество", variant["qty"]])
    head(ws, 6, ["Ресурс", "Вид", "Единица", "Норма на единицу",
                 "Количество на заказ", "Цена, руб./ед.", "Сумма, руб."])

    materials = Decimal("0")
    operations = Decimal("0")
    row = 7
    for resource in variant["resources"]:
        per_unit = resource["time"] if resource["kind"] == "operation" else resource["norm"]
        amount = dec(variant["qty"]) * dec(per_unit)
        total = amount * dec(resource["price"])
        if resource["kind"] == "operation":
            operations += total
        else:
            materials += total
        set_row(ws, row, [resource["name"], resource["kind"], resource["unit"],
                          quantity(resource["norm"]), quantity(amount),
                          resource["price"], money(total)])
        ws.cell(row=row, column=4).number_format = NUM
        ws.cell(row=row, column=5).number_format = NUM
        ws.cell(row=row, column=6).number_format = MONEY
        ws.cell(row=row, column=7).number_format = MONEY
        row += 1

    grand = materials + operations
    unit = grand / dec(variant["qty"])
    for label, value in (("Материалы", materials), ("Операции", operations),
                         ("Итого по заказу", grand),
                         ("Стоимость единицы", unit)):
        row += 1
        ws.cell(row=row, column=6, value=label)
        ws.cell(row=row, column=7, value=money(value)).number_format = MONEY
        ws.cell(row=row, column=6).font = Font(bold=True)

    ws["D2"].number_format = DATE
    ws["F4"].number_format = NUM
    ws.freeze_panes = "A7"
    save(ws, path)


def write_customers(variant: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(variant["customers"], ensure_ascii=False, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")


WRITERS = {
    "Заказ покупателя.xlsx": write_customer_order,
    "Заказ на производство.xlsx": write_production_order,
    "Спецификация.xlsx": write_specification,
    "Цены.xlsx": write_prices,
    "Расчет стоимости.xlsx": write_cost,
    "Заказчики.json": write_customers,
}


def write_set(variant: dict, folder: Path) -> None:
    for name in EXAM_FILES:
        writer = WRITERS[name]
        writer(variant, folder / name)


def make_zip(folder: Path, dest: Path) -> None:
    """Pack the six exam files at the archive root with fixed metadata."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w") as archive:
        for name in EXAM_FILES:
            info = zipfile.ZipInfo(name, date_time=ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 0
            info.external_attr = 0o644 << 16
            archive.writestr(info, (folder / name).read_bytes())


def main() -> None:
    variants = json.loads(DATA.read_text(encoding="utf-8"))
    by_id = {v["id"]: v for v in variants}

    for variant in variants:
        folder = VARIANTS / variant["id"]
        # the existing books stay as they are; only a missing file is written
        for name in EXAM_FILES:
            target = folder / name
            if not target.exists():
                WRITERS[name](variant, target)
        make_zip(folder, VARIANTS / f'{variant["id"]}.zip')
        print(f'{variant["id"]}: {len(EXAM_FILES)} files, {VARIANTS / variant["id"]}.zip')

    for variant_id in ("V01", "V02", "V03"):
        variant = by_id[variant_id]
        folder = PREP / variant_id
        write_set(variant, folder)
        make_zip(folder, PREP / f"{variant_id}.zip")
        print(f"{variant_id}: preparation set, {PREP / variant_id}.zip")


if __name__ == "__main__":
    main()
