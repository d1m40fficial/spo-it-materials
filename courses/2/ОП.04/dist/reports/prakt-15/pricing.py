"""Модуль расчёта для практики 15.

Функции уже реализованы. Менять их не нужно, нужно написать тесты.
"""


def discount(total, percent):
    """Вернуть сумму со скидкой в процентах."""
    if percent < 0 or percent > 100:
        raise ValueError("скидка должна быть от 0 до 100")
    if total < 0:
        raise ValueError("сумма не может быть отрицательной")
    return total - total * percent / 100


def delivery(total, zone="город"):
    """Вернуть стоимость доставки."""
    if zone == "город":
        return 0 if total >= 3000 else 300
    if zone == "область":
        return 500
    if zone == "самовывоз":
        return 0
    raise ValueError("неизвестная зона: " + zone)


def order_total(price, quantity, percent=0):
    """Вернуть стоимость заказа со скидкой."""
    if price < 0 or quantity < 0:
        raise ValueError("цена и количество не могут быть отрицательными")
    return discount(price * quantity, percent)
