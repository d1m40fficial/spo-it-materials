-- V02. Пекарня «Колос». Данные из документов варианта.
USE dkip2027_v02;

INSERT INTO counterparty (id, name, inn, address, phone, party_type) VALUES
('V02-MAKER', 'Пекарня «Колос»', '', 'Учебный город, улица Производственная, 2', '+79990020000', 'Изготовитель'),
('002000001', 'Магазин «Колос-1»', '', 'Учебный город, улица Производственная, 2, офис 1', '+79990020001', 'Покупатель'),
('002000002', 'Торговый дом «Колос-2»', '', 'Учебный город, улица Производственная, 2, офис 2', '+79990020002', 'Покупатель'),
('002000003', 'Студия «Колос-3»', '', 'Учебный город, улица Производственная, 2, офис 3', '+79990020003', 'Покупатель'),
('002000004', 'Магазин подарков «Колос-4»', '', 'Учебный город, улица Производственная, 2, офис 4', '+79990020004', 'Покупатель'),
('002000005', 'Мастерская «Колос-5»', '', 'Учебный город, улица Производственная, 2, офис 5', '+79990020005', 'Покупатель'),
('002000006', 'Оптовый склад «Колос-6»', '', 'Учебный город, улица Производственная, 2, офис 6', '+79990020006', 'Покупатель');

INSERT INTO item (id, code, name, kind, unit) VALUES
(1, 'V02-P01', 'Хлеб ржаной 500 г', 'product', 'ед.'),
(2, 'V02-M01', 'Мука ржаная', 'material', 'кг'),
(3, 'V02-M02', 'Закваска', 'material', 'кг'),
(4, 'V02-M03', 'Пакет', 'material', 'шт'),
(5, 'V02-O01', 'Замес и формование', 'operation', 'ч'),
(6, 'V02-O02', 'Выпечка', 'operation', 'ч');

INSERT INTO price (item_id, valid_from, amount) VALUES
(2, '2027-03-01', 65.00),
(3, '2027-03-01', 100.00),
(4, '2027-03-01', 4.00),
(5, '2027-03-01', 500.00),
(6, '2027-03-01', 700.00);

INSERT INTO specification (id, product_id, name, output_qty, manufacturer_id) VALUES
(1, 1, 'Хлеб ржаной 500 г', 1.000, 'V02-MAKER');

INSERT INTO specification_component (specification_id, item_id, qty, time_norm) VALUES
(1, 2, 0.320, NULL),
(1, 3, 0.080, NULL),
(1, 4, 1.000, NULL),
(1, 5, 1.000, 0.0400),
(1, 6, 1.000, 0.0200);

INSERT INTO customer_order (id, doc_no, doc_date, due_date, customer_id, executor_id) VALUES
(1, 'V02-01', '2027-03-15', '2027-03-22', '002000001', 'V02-MAKER');

INSERT INTO customer_order_line (id, order_id, product_id, qty) VALUES
(1, 1, 1, 40.000);

INSERT INTO production_order (id, doc_no, order_id, launch_date) VALUES
(1, 'V02-P01', 1, '2027-03-16');

INSERT INTO production_product (production_id, product_id, qty) VALUES
(1, 1, 40.000);

INSERT INTO production_resource (production_id, item_id, qty) VALUES
(1, 2, 12.800),
(1, 3, 3.200),
(1, 4, 40.000),
(1, 5, 1.600),
(1, 6, 0.800);
