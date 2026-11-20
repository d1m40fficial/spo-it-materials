"""Формирование строк отчёта."""


def build_report(records, total_sum, regions, avg):
    lines = [
        f"Всего: {total_sum:.2f}",
        f"Записей: {len(records)}",
        f"Средняя: {avg:.2f}",
    ]
    for region in sorted(regions):
        lines.append(f"{region}: {regions[region]:.2f}")
    return lines
