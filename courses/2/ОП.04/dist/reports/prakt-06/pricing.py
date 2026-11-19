"""Практика 6. Модуль расчёта.

Заполните функции. Этот файл импортируется в starter.py и может
запускаться отдельно для самопроверки:

    python pricing.py
"""


def order_total(price, quantity, discount=0):
    """Вернуть стоимость заказа с учётом скидки в процентах."""
    # TODO: посчитайте сумму, размер скидки и итог.
    # Скидка не может сделать итог отрицательным.
    return 0.0


def delivery_cost(total, zone="город"):
    """Вернуть стоимость доставки.

    город: 300, но бесплатно при сумме от 3000;
    область: 500;
    самовывоз: 0.
    """
    # TODO: постройте условие по зоне и сумме.
    return 0.0


if __name__ == "__main__":
    print("Самопроверка pricing.py")
    print("order_total(640, 3, 10) =", order_total(640, 3, 10))
    print("order_total(40, 10, 5) =", order_total(40, 10, 5))
    print("delivery_cost(1728) =", delivery_cost(1728))
    print("delivery_cost(4500) =", delivery_cost(4500))
    print("delivery_cost(1728, 'область') =", delivery_cost(1728, "область"))
