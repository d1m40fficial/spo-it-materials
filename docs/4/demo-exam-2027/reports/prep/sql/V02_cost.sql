USE dkip2027_v02;

INSERT INTO counterparty (id, name, inn, address, phone, party_type) VALUES
('002000001', 'Магазин «Колос-1»', '', 'Учебный город, улица Производственная, 2, офис 1', '+79990020001', 'Покупатель'),
('002000002', 'Торговый дом «Колос-2»', '', 'Учебный город, улица Производственная, 2, офис 2', '+79990020002', 'Покупатель'),
('002000003', 'Студия «Колос-3»', '', 'Учебный город, улица Производственная, 2, офис 3', '+79990020003', 'Покупатель'),
('002000004', 'Магазин подарков «Колос-4»', '', 'Учебный город, улица Производственная, 2, офис 4', '+79990020004', 'Покупатель'),
('002000005', 'Мастерская «Колос-5»', '', 'Учебный город, улица Производственная, 2, офис 5', '+79990020005', 'Покупатель'),
('002000006', 'Оптовый склад «Колос-6»', '', 'Учебный город, улица Производственная, 2, офис 6', '+79990020006', 'Покупатель'),
('M-001', 'Пекарня «Колос»', '', 'Учебный город, улица Производственная, 2', '+79990020000', 'Изготовитель');

INSERT INTO item (id, code, name, kind, unit) VALUES
(1, 'P-01', 'Хлеб ржаной 500 г', 'product', 'ед.'),
(2, 'M-01', 'Мука ржаная', 'material', 'кг'),
(3, 'M-02', 'Закваска', 'material', 'кг'),
(4, 'M-03', 'Пакет', 'material', 'шт'),
(5, 'O-01', 'Замес и формование', 'operation', 'ч'),
(6, 'O-02', 'Выпечка', 'operation', 'ч');

INSERT INTO price (item_id, valid_from, amount) VALUES
(2, '2027-03-01', 65.00),
(3, '2027-03-01', 100.00),
(4, '2027-03-01', 4.00),
(5, '2027-03-01', 500.00),
(6, '2027-03-01', 700.00);

INSERT INTO specification (id, product_id, name, output_qty, manufacturer_id) VALUES
(1, 1, 'Хлеб ржаной 500 г', 1.000, 'M-001');

INSERT INTO specification_component (specification_id, item_id, qty, time_norm) VALUES
(1, 2, 0.320, 0.000),
(1, 3, 0.080, 0.000),
(1, 4, 1.000, 0.000),
(1, 5, 0.000, 0.040),
(1, 6, 0.000, 0.020);

INSERT INTO customer_order (id, doc_no, doc_date, customer_id, executor_id) VALUES
(1, 'V02-01', '2027-03-15', '002000001', 'M-001');

INSERT INTO customer_order_line (id, order_id, product_id, qty, sale_price, discount) VALUES
(1, 1, 1, 40, 700.00, 0.00);

INSERT INTO production_order (id, doc_no, doc_date, launch_date, department) VALUES
(1, 'V02-P01', '2027-03-15', '2027-03-16', 'Основное производство');

INSERT INTO production_product (production_id, product_id, qty) VALUES
(1, 1, 40);

INSERT INTO production_resource (production_id, item_id, qty, time_norm) VALUES
(1, 2, 12.800, 0.000),
(1, 3, 3.200, 0.000),
(1, 4, 40.000, 0.000),
(1, 5, 0.000, 1.600),
(1, 6, 0.000, 0.800);

INSERT INTO users (id, login, password_hash, salt, role, failed_attempts, is_locked) VALUES
(1, 'admin', 'hash-admin', 'salt-admin', 'admin', 0, 0),
(2, 'manager', 'hash-manager', 'salt-manager', 'user', 0, 0),
(3, 'technologist', 'hash-technologist', 'salt-technologist', 'user', 0, 0),
(4, 'master', 'hash-master', 'salt-master', 'user', 0, 0);

INSERT INTO notes (id, title, content, id_user, created_at) VALUES
(1, 'Заказ принят', 'Заказ V02-01: Хлеб ржаной 500 г, 40 ед.; срок 22.03.2027.', 2, '2027-03-16'),
(2, 'Спецификация согласована', 'Нормы относятся к одной буханке; время печи распределено на изделие.', 3, '2027-03-16'),
(3, 'Материалы проверены', 'Подготовить: муку ржаную, закваску, пакеты.', 4, '2027-03-16'),
(4, 'Порядок производства', 'Замес, формование, выпечка, упаковка.', 4, '2027-03-16'),
(5, 'Расчёт заказа', 'Использовать цены от 01.03.2027. Итог округлить до копеек.', 2, '2027-03-16');

-- Нормативная стоимость заказа V02-01
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
WHERE o.doc_no = 'V02-01'
GROUP BY o.doc_no;
