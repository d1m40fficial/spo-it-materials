-- V02. Пекарня «Колос». Схема базы dkip2027_v02.
CREATE DATABASE IF NOT EXISTS dkip2027_v02
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE dkip2027_v02;

CREATE TABLE counterparty (
  id VARCHAR(32) NOT NULL,
  name VARCHAR(255) NOT NULL,
  inn VARCHAR(20) NOT NULL DEFAULT '',
  address VARCHAR(500) NOT NULL,
  phone VARCHAR(64) NOT NULL,
  party_type VARCHAR(24) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE item (
  id INT AUTO_INCREMENT NOT NULL,
  code VARCHAR(64) NOT NULL,
  name VARCHAR(255) NOT NULL,
  kind VARCHAR(16) NOT NULL,
  unit VARCHAR(16) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_item_code (code),
  CONSTRAINT ck_item_kind CHECK (kind IN ('product','material','operation'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE price (
  item_id INT NOT NULL,
  valid_from DATE NOT NULL,
  amount DECIMAL(14,2) NOT NULL,
  PRIMARY KEY (item_id, valid_from),
  CONSTRAINT fk_price_item FOREIGN KEY (item_id) REFERENCES item(id),
  CONSTRAINT ck_price_amount CHECK (amount >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE specification (
  id INT AUTO_INCREMENT NOT NULL,
  product_id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  output_qty DECIMAL(14,3) NOT NULL,
  manufacturer_id VARCHAR(32) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_spec_product (product_id),
  CONSTRAINT fk_spec_product FOREIGN KEY (product_id) REFERENCES item(id),
  CONSTRAINT fk_spec_maker FOREIGN KEY (manufacturer_id) REFERENCES counterparty(id),
  CONSTRAINT ck_spec_output CHECK (output_qty > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE specification_component (
  specification_id INT NOT NULL,
  item_id INT NOT NULL,
  qty DECIMAL(14,3) NOT NULL,
  time_norm DECIMAL(14,4) NULL,
  PRIMARY KEY (specification_id, item_id),
  CONSTRAINT fk_comp_spec FOREIGN KEY (specification_id) REFERENCES specification(id),
  CONSTRAINT fk_comp_item FOREIGN KEY (item_id) REFERENCES item(id),
  CONSTRAINT ck_comp_qty CHECK (qty > 0),
  CONSTRAINT ck_comp_time CHECK (time_norm IS NULL OR time_norm >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE customer_order (
  id INT AUTO_INCREMENT NOT NULL,
  doc_no VARCHAR(64) NOT NULL,
  doc_date DATE NOT NULL,
  due_date DATE NOT NULL,
  customer_id VARCHAR(32) NOT NULL,
  executor_id VARCHAR(32) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_order_no (doc_no),
  CONSTRAINT fk_order_customer FOREIGN KEY (customer_id) REFERENCES counterparty(id),
  CONSTRAINT fk_order_executor FOREIGN KEY (executor_id) REFERENCES counterparty(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE customer_order_line (
  id INT AUTO_INCREMENT NOT NULL,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  qty DECIMAL(14,3) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_line_order FOREIGN KEY (order_id) REFERENCES customer_order(id),
  CONSTRAINT fk_line_product FOREIGN KEY (product_id) REFERENCES item(id),
  CONSTRAINT ck_line_qty CHECK (qty > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE production_order (
  id INT AUTO_INCREMENT NOT NULL,
  doc_no VARCHAR(64) NOT NULL,
  order_id INT NOT NULL,
  launch_date DATE NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_production_no (doc_no),
  CONSTRAINT fk_prod_order FOREIGN KEY (order_id) REFERENCES customer_order(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE production_product (
  production_id INT NOT NULL,
  product_id INT NOT NULL,
  qty DECIMAL(14,3) NOT NULL,
  PRIMARY KEY (production_id, product_id),
  CONSTRAINT fk_pp_prod FOREIGN KEY (production_id) REFERENCES production_order(id),
  CONSTRAINT fk_pp_item FOREIGN KEY (product_id) REFERENCES item(id),
  CONSTRAINT ck_pp_qty CHECK (qty > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE production_resource (
  production_id INT NOT NULL,
  item_id INT NOT NULL,
  qty DECIMAL(14,3) NOT NULL,
  PRIMARY KEY (production_id, item_id),
  CONSTRAINT fk_pr_prod FOREIGN KEY (production_id) REFERENCES production_order(id),
  CONSTRAINT fk_pr_item FOREIGN KEY (item_id) REFERENCES item(id),
  CONSTRAINT ck_pr_qty CHECK (qty > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
