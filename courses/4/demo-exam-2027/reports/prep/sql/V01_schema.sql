PRAGMA foreign_keys = ON;

CREATE TABLE counterparty (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    inn TEXT,
    address TEXT,
    phone TEXT,
    party_type TEXT NOT NULL CHECK (party_type IN ('Покупатель', 'Изготовитель', 'Поставщик'))
);

CREATE TABLE item (
    id INTEGER PRIMARY KEY,
    code TEXT,
    name TEXT NOT NULL,
    kind TEXT NOT NULL CHECK (kind IN ('product', 'material', 'operation')),
    unit TEXT NOT NULL
);

CREATE TABLE price (
    item_id INTEGER NOT NULL REFERENCES item(id),
    valid_from TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount >= 0),
    PRIMARY KEY (item_id, valid_from)
);

CREATE TABLE specification (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL UNIQUE REFERENCES item(id),
    name TEXT NOT NULL,
    output_qty REAL NOT NULL CHECK (output_qty > 0),
    manufacturer_id TEXT NOT NULL REFERENCES counterparty(id)
);

CREATE TABLE specification_component (
    specification_id INTEGER NOT NULL REFERENCES specification(id),
    item_id INTEGER NOT NULL REFERENCES item(id),
    qty REAL NOT NULL CHECK (qty >= 0),
    time_norm REAL NOT NULL CHECK (time_norm >= 0),
    PRIMARY KEY (specification_id, item_id)
);

CREATE TABLE customer_order (
    id INTEGER PRIMARY KEY,
    doc_no TEXT NOT NULL UNIQUE,
    doc_date TEXT NOT NULL,
    customer_id TEXT NOT NULL REFERENCES counterparty(id),
    executor_id TEXT NOT NULL REFERENCES counterparty(id)
);

CREATE TABLE customer_order_line (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES customer_order(id),
    product_id INTEGER NOT NULL REFERENCES item(id),
    qty INTEGER NOT NULL CHECK (qty > 0),
    sale_price REAL NOT NULL CHECK (sale_price >= 0),
    discount REAL NOT NULL DEFAULT 0 CHECK (discount >= 0)
);

CREATE TABLE production_order (
    id INTEGER PRIMARY KEY,
    doc_no TEXT NOT NULL UNIQUE,
    doc_date TEXT NOT NULL,
    launch_date TEXT NOT NULL,
    department TEXT NOT NULL
);

CREATE TABLE production_product (
    production_id INTEGER NOT NULL REFERENCES production_order(id),
    product_id INTEGER NOT NULL REFERENCES item(id),
    qty INTEGER NOT NULL CHECK (qty > 0),
    PRIMARY KEY (production_id, product_id)
);

CREATE TABLE production_resource (
    production_id INTEGER NOT NULL REFERENCES production_order(id),
    item_id INTEGER NOT NULL REFERENCES item(id),
    qty REAL NOT NULL CHECK (qty >= 0),
    time_norm REAL NOT NULL CHECK (time_norm >= 0),
    PRIMARY KEY (production_id, item_id)
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    login TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    failed_attempts INTEGER NOT NULL DEFAULT 0,
    is_locked INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    id_user INTEGER NOT NULL REFERENCES users(id),
    created_at TEXT NOT NULL
);
