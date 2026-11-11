CREATE DATABASE IF NOT EXISTS dkip2027_v02
  CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE dkip2027_v02;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS notes, users,
  production_resource, production_product, production_order,
  customer_order_line, customer_order,
  specification_component, specification,
  price, item, counterparty;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE counterparty (
  id VARCHAR(32) NOT NULL,
  name VARCHAR(255) NOT NULL,
  inn VARCHAR(20) NOT NULL DEFAULT '',
  address VARCHAR(500) NOT NULL,
  phone VARCHAR(64) NOT NULL,
  party_type VARCHAR(24) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT ck_party_type
    CHECK (party_type IN ('Покупатель', 'Поставщик', 'Изготовитель'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE item (
  id INT NOT NULL,
  code VARCHAR(64) DEFAULT NULL,
  name VARCHAR(255) NOT NULL,
  kind VARCHAR(16) NOT NULL,
  unit VARCHAR(16) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_item_code (code),
  CONSTRAINT ck_item_kind
    CHECK (kind IN ('product', 'material', 'operation'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE price (
  item_id INT NOT NULL,
  valid_from DATE NOT NULL,
  amount DECIMAL(14,2) NOT NULL,
  PRIMARY KEY (item_id, valid_from),
  CONSTRAINT ck_price_amount CHECK (amount >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE specification (
  id INT NOT NULL,
  product_id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  output_qty DECIMAL(14,3) NOT NULL,
  manufacturer_id VARCHAR(32) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_spec_product (product_id),
  KEY ix_spec_maker (manufacturer_id),
  CONSTRAINT ck_spec_output CHECK (output_qty > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE specification_component (
  specification_id INT NOT NULL,
  item_id INT NOT NULL,
  qty DECIMAL(14,3) NOT NULL,
  time_norm DECIMAL(14,3) NOT NULL,
  PRIMARY KEY (specification_id, item_id),
  KEY ix_comp_item (item_id),
  CONSTRAINT ck_comp_qty CHECK (qty >= 0),
  CONSTRAINT ck_comp_time CHECK (time_norm >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE customer_order (
  id INT NOT NULL,
  doc_no VARCHAR(64) NOT NULL,
  doc_date DATE NOT NULL,
  customer_id VARCHAR(32) NOT NULL,
  executor_id VARCHAR(32) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_order_doc (doc_no),
  KEY ix_order_customer (customer_id),
  KEY ix_order_executor (executor_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE customer_order_line (
  id INT NOT NULL,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  qty INT NOT NULL,
  sale_price DECIMAL(14,2) NOT NULL,
  discount DECIMAL(14,2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (id),
  KEY ix_line_order (order_id),
  KEY ix_line_product (product_id),
  CONSTRAINT ck_line_qty CHECK (qty > 0),
  CONSTRAINT ck_line_price CHECK (sale_price >= 0),
  CONSTRAINT ck_line_discount CHECK (discount >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE production_order (
  id INT NOT NULL,
  doc_no VARCHAR(64) NOT NULL,
  doc_date DATE NOT NULL,
  launch_date DATE NOT NULL,
  department VARCHAR(128) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_prod_doc (doc_no)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE production_product (
  production_id INT NOT NULL,
  product_id INT NOT NULL,
  qty INT NOT NULL,
  PRIMARY KEY (production_id, product_id),
  KEY ix_prod_product (product_id),
  CONSTRAINT ck_pp_qty CHECK (qty > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE production_resource (
  production_id INT NOT NULL,
  item_id INT NOT NULL,
  qty DECIMAL(14,3) NOT NULL,
  time_norm DECIMAL(14,3) NOT NULL,
  PRIMARY KEY (production_id, item_id),
  KEY ix_prod_resource (item_id),
  CONSTRAINT ck_pr_qty CHECK (qty >= 0),
  CONSTRAINT ck_pr_time CHECK (time_norm >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT,
  login VARCHAR(64) NOT NULL,
  password_hash VARCHAR(64) NOT NULL,
  salt VARCHAR(32) NOT NULL,
  role ENUM('admin', 'user') NOT NULL DEFAULT 'user',
  failed_attempts INT NOT NULL DEFAULT 0,
  is_locked TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_users_login (login)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE notes (
  id INT NOT NULL AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  id_user INT NOT NULL,
  created_at DATE NOT NULL,
  PRIMARY KEY (id),
  KEY ix_notes_user (id_user)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
