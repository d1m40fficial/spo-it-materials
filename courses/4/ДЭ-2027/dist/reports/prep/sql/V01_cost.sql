USE dkip2027_course;

INSERT INTO counterparty (id, name, inn, address, phone, party_type) VALUES
('000000001', 'ООО "Поставка"', '', 'г. Пятигорск', '+79198634592', 'Поставщик'),
('000000002', 'ООО "Кинотеатр Квант"', '26320045123', 'г. Железноводск, ул. Мира, 123', '+79884581555', 'Покупатель'),
('000000008', 'ООО "Новый JDTO"', '26320045111', 'г. Железноводск', '+79884581555', 'Покупатель'),
('000000003', 'ООО "Ромашка"', '4140784214', 'г. Омск, ул. Строителей, 294', '+79882584546', 'Поставщик'),
('000000009', 'ООО "Ипподром"', '5874045632', 'г. Уфа, ул. Набережная, 37', '+79627486389', 'Поставщик'),
('000000010', 'ООО "Ассоль"', '2629011278', 'г. Калуга, ул. Пушкина, 94', '+79184572398', 'Покупатель'),
('000000004', 'ИП Томилин Александр Сергеевич', '', 'г. Пятигорск', '', 'Покупатель'),
('M-001', 'ООО ТД "Вершина"', '', 'г. Пятигорск', '', 'Изготовитель');

INSERT INTO item (id, code, name, kind, unit) VALUES
(1, 'ФР-00000034', 'Стол кухонный "Самобранка"', 'product', 'шт'),
(2, 'ФР-00000009', 'Столешница круглая', 'material', 'шт'),
(3, 'ФР-00000013', 'Мебельная деталь 500х800', 'material', 'шт'),
(4, 'ФР-00000016', 'Мебельная деталь 600х800', 'material', 'шт'),
(5, 'ФР-00000027', 'Евровинт 6,5х5', 'material', 'тыс. шт'),
(6, 'ФР-00000026', 'Опора', 'material', 'шт'),
(7, 'ФР-00000053', 'Сборка модулей', 'operation', 'ч'),
(8, 'ФР-00000052', 'Распил ДСП, МДФ и листового материала', 'operation', 'ч'),
(9, 'ФР-00000494', 'Упаковка', 'operation', 'ч');

INSERT INTO price (item_id, valid_from, amount) VALUES
(2, '2026-04-01', 3250.00),
(3, '2026-04-01', 95.00),
(4, '2026-04-01', 140.00),
(5, '2026-04-01', 595.00),
(6, '2026-04-01', 245.00),
(7, '2026-04-01', 1400.00),
(8, '2026-04-01', 450.00),
(9, '2026-04-01', 950.00);

INSERT INTO specification (id, product_id, name, output_qty, manufacturer_id) VALUES
(1, 1, 'Стол кухонный "Самобранка"', 1.000, 'M-001');

INSERT INTO specification_component (specification_id, item_id, qty, time_norm) VALUES
(1, 2, 1.000, 0.000),
(1, 3, 2.000, 0.000),
(1, 4, 4.000, 0.000),
(1, 5, 0.012, 0.000),
(1, 6, 4.000, 0.000),
(1, 7, 0.000, 0.750),
(1, 8, 0.000, 1.500),
(1, 9, 0.000, 0.500);

INSERT INTO customer_order (id, doc_no, doc_date, customer_id, executor_id) VALUES
(1, 'V01-01', '2026-04-22', '000000004', 'M-001');

INSERT INTO customer_order_line (id, order_id, product_id, qty, sale_price, discount) VALUES
(1, 1, 1, 2, 14120.00, 1412.00);

INSERT INTO production_order (id, doc_no, doc_date, launch_date, department) VALUES
(1, 'V01-P-01', '2026-04-22', '2026-04-23', 'Основное подразделение');

INSERT INTO production_product (production_id, product_id, qty) VALUES
(1, 1, 2);

INSERT INTO production_resource (production_id, item_id, qty, time_norm) VALUES
(1, 2, 2.000, 0.000),
(1, 3, 4.000, 0.000),
(1, 4, 8.000, 0.000),
(1, 5, 0.024, 0.000),
(1, 6, 8.000, 0.000),
(1, 7, 0.000, 2.000),
(1, 8, 0.000, 2.000),
(1, 9, 0.000, 2.000);

INSERT INTO users (id, login, password_hash, salt, role, failed_attempts, is_locked) VALUES
(1, 'admin', 'hash-admin', 'salt-admin', 'admin', 0, 0),
(2, 'manager', 'hash-manager', 'salt-manager', 'user', 0, 0),
(3, 'technologist', 'hash-technologist', 'salt-technologist', 'user', 0, 0),
(4, 'master', 'hash-master', 'salt-master', 'user', 0, 0);

INSERT INTO notes (id, title, content, id_user, created_at) VALUES
(1, 'Заказ принят', 'Заказ V01-01: Стол кухонный "Самобранка", 2 ед.; срок 29.04.2026.', 2, '2026-04-22'),
(2, 'Спецификация согласована', 'Нормы даны на один стол; материалы считаются в штуках и тысячах штук.', 3, '2026-04-22'),
(3, 'Материалы проверены', 'Подготовить: столешницу, детали 500х800 и 600х800, евровинты, опоры.', 4, '2026-04-22'),
(4, 'Порядок производства', 'Раскрой ДСП, сборка модулей, упаковка.', 4, '2026-04-22'),
(5, 'Расчёт заказа', 'Использовать цены от 01.04.2026. Итог округлить до копеек.', 2, '2026-04-22');

-- Нормативная стоимость заказа V01-01
SELECT
  o.doc_no,
  ROUND(SUM(l.qty / s.output_qty
    * CASE WHEN i.kind = 'operation' THEN c.time_norm ELSE c.qty END
    * p.amount), 2) AS total_cost
FROM customer_order o
JOIN customer_order_line l ON l.order_id = o.id
JOIN specification s ON s.product_id = l.product_id
JOIN specification_component c ON c.specification_id = s.id
JOIN item i ON i.id = c.item_id
JOIN price p ON p.item_id = c.item_id
  AND p.valid_from = (
    SELECT MAX(p2.valid_from)
    FROM price p2
    WHERE p2.item_id = c.item_id
      AND p2.valid_from <= o.doc_date
  )
WHERE o.doc_no = 'V01-01'
GROUP BY o.doc_no;
