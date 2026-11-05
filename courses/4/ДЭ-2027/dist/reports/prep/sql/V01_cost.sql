INSERT INTO counterparty (id, name, inn, address, phone, party_type)
VALUES ('M-001', 'Ателье «Стежок»', '', 'Учебный город, улица Производственная, 1', '+79990000001', 'Изготовитель');

INSERT INTO item (id, code, name, kind, unit) VALUES

    (1, 'P-01', 'Фартук поварской', 'product', 'шт'),
    (2, 'M-01', 'Бязь', 'material', 'м'),
    (3, 'M-02', 'Тесьма', 'material', 'м'),
    (4, 'M-03', 'Нить', 'material', 'м'),
    (5, 'O-01', 'Раскрой', 'operation', 'ч'),
    (6, 'O-02', 'Пошив', 'operation', 'ч');

INSERT INTO price (item_id, valid_from, amount) VALUES

    (2, '2027-03-01', 280),
    (3, '2027-03-01', 25),
    (4, '2027-03-01', 0.4),
    (5, '2027-03-01', 600),
    (6, '2027-03-01', 800);

INSERT INTO specification (id, product_id, name, output_qty, manufacturer_id)
VALUES (1, 1, 'Фартук поварской', 1, 'M-001');

INSERT INTO specification_component (specification_id, item_id, qty, time_norm) VALUES

    (1, 2, 0.8, 1),
    (1, 3, 2, 1),
    (1, 4, 35, 1),
    (1, 5, 1, 0.12),
    (1, 6, 1, 0.35);

INSERT INTO customer_order (id, doc_no, doc_date, customer_id, executor_id)
VALUES (1, 'V01-01', '2027-03-15', '001000001', 'M-001');

INSERT INTO customer_order_line (id, order_id, product_id, qty, sale_price, discount)
VALUES (1, 1, 1, 12, 700, 0);

INSERT INTO production_order (id, doc_no, doc_date, launch_date, department)
VALUES (1, 'V01-P-01', '2027-03-02', '2027-03-05', 'Швейный цех');

INSERT INTO production_product (production_id, product_id, qty)
VALUES (1, 1, 12);

INSERT INTO production_resource (production_id, item_id, qty, time_norm) VALUES

    (1, 2, 9.6, 1),
    (1, 3, 24, 1),
    (1, 4, 420, 1),
    (1, 5, 1.44, 0.12),
    (1, 6, 4.2, 0.35);

INSERT INTO users (id, login, password_hash, role, failed_attempts, is_locked)
VALUES (1, 'admin', 'hash-admin', 'admin', 0, 0),
       (2, 'manager', 'hash-manager', 'manager', 0, 0);

INSERT INTO notes (id, title, content, id_user, created_at)
VALUES (1, 'Проверить нормы', 'Сверить расход бязи по спецификации', 2, '2027-03-10');

WITH price_on_date AS (
    SELECT p.item_id, p.amount
    FROM price p
    WHERE p.valid_from = (
        SELECT MAX(p2.valid_from)
        FROM price p2
        WHERE p2.item_id = p.item_id
          AND p2.valid_from <= '2027-03-15'
    )
)
SELECT o.doc_no,
       ROUND(SUM(l.qty / s.output_qty * c.qty * c.time_norm * pd.amount), 2) AS total_cost
FROM customer_order o
JOIN customer_order_line l ON l.order_id = o.id
JOIN specification s ON s.product_id = l.product_id
JOIN specification_component c ON c.specification_id = s.id
JOIN price_on_date pd ON pd.item_id = c.item_id
WHERE o.doc_no = 'V01-01'
GROUP BY o.doc_no;
