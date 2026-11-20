"""Показатели по выгрузке."""


def total(records):
    return sum(record["amount"] for record in records)


def by_region(records):
    result = {}
    for record in records:
        region = record["region"]
        result[region] = result.get(region, 0.0) + record["amount"]
    return result


def average(records):
    if not records:
        return 0.0
    return total(records) / len(records)
