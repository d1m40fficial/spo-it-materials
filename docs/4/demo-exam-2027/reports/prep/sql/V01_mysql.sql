CREATE DATABASE IF NOT EXISTS dkip2027_course CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE dkip2027_course;

DROP VIEW IF EXISTS order_cost_lines;
DROP VIEW IF EXISTS order_cost;
DROP TABLE IF EXISTS customer_order_line, customer_order, specification_component, specification, price, item, counterparty;

CREATE TABLE counterparty (
  id VARCHAR(32) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  inn VARCHAR(20) NOT NULL DEFAULT '',
  address VARCHAR(500) NOT NULL,
  phone VARCHAR(64) NOT NULL,
  party_type VARCHAR(24) NOT NULL,
  CONSTRAINT ck_party_type CHECK (party_type IN ('Покупатель','Поставщик','Изготовитель'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE item (
  id INT PRIMARY KEY,
  code VARCHAR(64) UNIQUE,
  name VARCHAR(255) NOT NULL,
  kind VARCHAR(16) NOT NULL,
  unit VARCHAR(16) NOT NULL,
  CONSTRAINT ck_item_kind CHECK (kind IN ('product','material','operation'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE price (
  item_id INT NOT NULL,
  valid_from DATE NOT NULL,
  amount DECIMAL(14,2) NOT NULL,
  PRIMARY KEY (item_id, valid_from),
  CONSTRAINT fk_price_item FOREIGN KEY (item_id) REFERENCES item(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE specification (
  id INT PRIMARY KEY,
  product_id INT NOT NULL UNIQUE,
  name VARCHAR(255) NOT NULL,
  output_qty DECIMAL(14,3) NOT NULL,
  manufacturer_id VARCHAR(32) NOT NULL,
  CONSTRAINT fk_spec_product FOREIGN KEY (product_id) REFERENCES item(id),
  CONSTRAINT fk_spec_maker FOREIGN KEY (manufacturer_id) REFERENCES counterparty(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE specification_component (
  specification_id INT NOT NULL,
  item_id INT NOT NULL,
  qty DECIMAL(14,3) NOT NULL,
  time_norm DECIMAL(14,3) NOT NULL,
  PRIMARY KEY (specification_id, item_id),
  CONSTRAINT fk_comp_spec FOREIGN KEY (specification_id) REFERENCES specification(id),
  CONSTRAINT fk_comp_item FOREIGN KEY (item_id) REFERENCES item(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE customer_order (
  id INT PRIMARY KEY,
  doc_no VARCHAR(64) NOT NULL UNIQUE,
  doc_date DATE NOT NULL,
  customer_id VARCHAR(32) NOT NULL,
  executor_id VARCHAR(32) NOT NULL,
  CONSTRAINT fk_order_customer FOREIGN KEY (customer_id) REFERENCES counterparty(id),
  CONSTRAINT fk_order_executor FOREIGN KEY (executor_id) REFERENCES counterparty(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE customer_order_line (
  id INT PRIMARY KEY,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  qty INT NOT NULL,
  sale_price DECIMAL(14,2) NOT NULL,
  discount DECIMAL(14,2) NOT NULL DEFAULT 0,
  CONSTRAINT fk_line_order FOREIGN KEY (order_id) REFERENCES customer_order(id),
  CONSTRAINT fk_line_product FOREIGN KEY (product_id) REFERENCES item(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO counterparty (id,name,inn,address,phone,party_type) VALUES
('M-001','Ателье «Стежок»','','Учебный город, улица Производственная, 1','+79990000001','Изготовитель'),
('001000001','Магазин «Стежок-1»','','Учебный город, улица Производственная, 1, офис 1','+79990010001','Покупатель'),
('001000002','Торговый дом «Стежок-2»','','Учебный город, улица Производственная, 1, офис 2','+79990010002','Покупатель'),
('001000003','Студия «Стежок-3»','','Учебный город, улица Производственная, 1, офис 3','+79990010003','Покупатель'),
('001000004','Магазин подарков «Стежок-4»','','Учебный город, улица Производственная, 1, офис 4','+79990010004','Покупатель'),
('001000005','Мастерская «Стежок-5»','','Учебный город, улица Производственная, 1, офис 5','+79990010005','Покупатель'),
('001000006','Оптовый склад «Стежок-6»','','Учебный город, улица Производственная, 1, офис 6','+79990010006','Покупатель');

INSERT INTO item (id,code,name,kind,unit) VALUES
(1,'P-01','Фартук поварской','product','шт'),
(2,'M-01','Бязь','material','м'),
(3,'M-02','Тесьма','material','м'),
(4,'M-03','Нить','material','кат.'),
(5,'O-01','Раскрой','operation','ч'),
(6,'O-02','Пошив','operation','ч');

INSERT INTO price (item_id,valid_from,amount) VALUES
(2,'2027-03-01',280.00),(3,'2027-03-01',25.00),(4,'2027-03-01',0.40),
(5,'2027-03-01',600.00),(6,'2027-03-01',800.00);

INSERT INTO specification (id,product_id,name,output_qty,manufacturer_id) VALUES
(1,1,'Фартук поварской',1.000,'M-001');

INSERT INTO specification_component (specification_id,item_id,qty,time_norm) VALUES
(1,2,0.800,1.000),(1,3,2.000,1.000),(1,4,35.000,1.000),
(1,5,1.000,0.120),(1,6,1.000,0.350);

INSERT INTO customer_order (id,doc_no,doc_date,customer_id,executor_id) VALUES
(1,'V01-01','2027-03-15','001000001','M-001');

INSERT INTO customer_order_line (id,order_id,product_id,qty,sale_price,discount) VALUES
(1,1,1,12,700.00,0.00);

CREATE VIEW order_cost AS
SELECT o.id AS order_id, o.doc_no,
       ROUND(SUM(l.qty / s.output_qty * c.qty * c.time_norm * p.amount), 2) AS total_cost
FROM customer_order o
JOIN customer_order_line l ON l.order_id = o.id
JOIN specification s ON s.product_id = l.product_id
JOIN specification_component c ON c.specification_id = s.id
JOIN price p ON p.item_id = c.item_id
WHERE p.valid_from = (
  SELECT MAX(p2.valid_from) FROM price p2
  WHERE p2.item_id = p.item_id AND p2.valid_from <= o.doc_date
)
GROUP BY o.id, o.doc_no;

CREATE VIEW order_cost_lines AS
SELECT 'Материал' AS section, i.name, l.qty AS product_qty,
       c.qty AS norm, p.amount AS price,
       ROUND(l.qty / s.output_qty * c.qty * p.amount, 2) AS amount
FROM customer_order o
JOIN customer_order_line l ON l.order_id = o.id
JOIN specification s ON s.product_id = l.product_id
JOIN specification_component c ON c.specification_id = s.id
JOIN item i ON i.id = c.item_id
JOIN price p ON p.item_id = i.id AND p.valid_from = '2027-03-01'
WHERE o.doc_no = 'V01-01' AND i.kind = 'material'
UNION ALL
SELECT 'Операция', i.name, l.qty,
       c.time_norm, p.amount,
       ROUND(l.qty / s.output_qty * c.time_norm * p.amount, 2)
FROM customer_order o
JOIN customer_order_line l ON l.order_id = o.id
JOIN specification s ON s.product_id = l.product_id
JOIN specification_component c ON c.specification_id = s.id
JOIN item i ON i.id = c.item_id
JOIN price p ON p.item_id = i.id AND p.valid_from = '2027-03-01'
WHERE o.doc_no = 'V01-01' AND i.kind = 'operation';
