---
title: Предварительная подготовка
dek: Три тестовых варианта и пошаговый разбор первых трёх заданий только в draw.io и sqliteonline.com.
chapter: "Подготовка"
level: СПО
glyph: "00"
outcomes:
  - Строить ER-диаграмму в draw.io и сохранять её в PDF
  - Создавать таблицы и импортировать JSON в sqliteonline.com
  - Считать стоимость заказа запросом с JOIN и агрегацией
---

## Зачем этот раздел

Первые три задания проверяют модель данных, базу и расчёт. Их можно пройти без установки сервера: диаграмма собирается в draw.io, база и запросы выполняются в sqliteonline.com. Оба инструмента работают в браузере, поэтому подготовка не зависит от прав администратора и настроек учебного компьютера.

| Задание | Инструмент | Что сдать |
|---|---|---|
| 1. ER-диаграмма | draw.io | PDF с диаграммой и исходник `.drawio` |
| 2. База и импорт JSON | sqliteonline.com | SQL-скрипт схемы и заполненная база |
| 3. SQL-запрос стоимости | sqliteonline.com | SQL-запрос и таблица результата |

Разбор идёт на варианте V01 «Швейное производство». Варианты V02 и V03 даны для самостоятельной работы: структура заданий та же, меняются предприятие, продукция и числа. Снимки экрана кликабельны: по щелчку они открываются в полном размере.

## Три тестовых варианта

| Вариант | Предприятие | Продукция | Количество |
|---|---|---|---|
| V01 | Ателье «Стежок» | Фартук поварской | 12 |
| V02 | Пекарня «Колос» | Хлеб ржаной 500 г | 40 |
| V03 | Мастерская «Глина» | Кружка 300 мл | 18 |

Файлы варианта:

- [V01: заказчики, JSON](reports/prep/V01_customers.json) и [ресурсы, CSV](reports/prep/V01_resources.csv)
- [V02: заказчики, JSON](reports/prep/V02_customers.json) и [ресурсы, CSV](reports/prep/V02_resources.csv)
- [V03: заказчики, JSON](reports/prep/V03_customers.json) и [ресурсы, CSV](reports/prep/V03_resources.csv)

В JSON лежат заказчики с полями `id`, `name`, `inn`, `addres`, `phone`, `type`. В CSV лежат ресурсы с полями `name`, `kind`, `unit`, `norm`, `time`, `price`. Для материалов `norm` это расход на единицу, для операций `time` это часы на единицу.

## Задание 1. ER-диаграмма в draw.io

### Шаг 1. Откройте редактор

Откройте `app.diagrams.net`. Учётная запись не нужна. На стартовом экране выберите создание пустой диаграммы и хранение на устройстве, чтобы файл сохранился в папку занятия.

<a href="reports/screens/prep/drawio-start.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-start.png" alt="Стартовый экран draw.io: пустой холст, панель фигур и меню Файл"></a>
<figcaption>Стартовый экран draw.io. Слева панель фигур, справа настройки холста, сверху меню файла и экспорта.</figcaption>

Не начинайте с готового шаблона: на защите нужно объяснить каждую таблицу. Пустой холст заставляет принимать решения по документам варианта.

### Шаг 2. Соберите первую таблицу

Возьмите фигуру таблицы и назовите её `counterparty`. Внутри разместите поля:

```text
PK  id          TEXT
    name        TEXT NOT NULL
    inn         TEXT
    address     TEXT
    phone       TEXT
    party_type  TEXT
```

`PK` отмечает первичный ключ. `NOT NULL` показывает обязательное поле. `party_type` хранит роль контрагента: покупатель, изготовитель или поставщик.

<a href="reports/screens/prep/drawio-step1.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-step1.png" alt="Первая таблица counterparty в draw.io: ключ, поля и типы"></a>
<figcaption>Первая таблица. Заголовок, первичный ключ и поля с типами. Пока этого достаточно, чтобы проверить подход.</figcaption>

Не рисуйте таблицу обычными прямоугольниками. Фигура таблицы держит строки и столбцы, поэтому поля не разъезжаются при перемещении.

### Шаг 3. Добавьте заказ и строки заказа

Заказ делится на шапку и строки. В шапке `customer_order` хранятся номер, дата, заказчик и исполнитель. В строках `customer_order_line` хранятся изделие, количество и продажная цена.

```text
customer_order
PK  id             INTEGER
    doc_no         TEXT
    doc_date       TEXT
FK  customer_id    TEXT
FK  executor_id    TEXT

customer_order_line
PK  id             INTEGER
FK  order_id       INTEGER
FK  product_id     INTEGER
    qty            INTEGER
    sale_price     REAL
```

Один заказ содержит много строк, поэтому связь читается как `1:N`: единица у заказа, `N` у строки.

<a href="reports/screens/prep/drawio-step2.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-step2.png" alt="Шапка заказа, строки заказа и изделие в draw.io с подписями 1:N"></a>
<figcaption>Шапка, строки и изделие. У каждой связи подписана кратность, внешние ключи отмечены буквами FK.</figcaption>

### Шаг 4. Добавьте остальные таблицы

Полная модель варианта содержит двенадцать таблиц. В варианте меняются названия предприятия и продукции, но структура остаётся той же.

| Таблица | Что хранит | Первичный ключ |
|---|---|---|
| `counterparty` | заказчиков, изготовителей, поставщиков | `id` |
| `item` | продукцию, материалы и операции | `id` |
| `price` | историю цен ресурса | `item_id`, `valid_from` |
| `specification` | шапку спецификации изделия | `id` |
| `specification_component` | строки состава с нормами | `specification_id`, `item_id` |
| `customer_order` | шапку заказа покупателя | `id` |
| `customer_order_line` | строки заказа | `id` |
| `production_order` | шапку производственного заказа | `id` |
| `production_product` | продукцию к выпуску | `production_id`, `product_id` |
| `production_resource` | плановый расход ресурсов | `production_id`, `item_id` |
| `users` | учётные записи приложения | `id` |
| `notes` | заметки сотрудников | `id` |

<a href="reports/screens/prep/drawio-er.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-er.png" alt="Полная ER-диаграмма варианта V01: двенадцать таблиц и связи между ними"></a>
<figcaption>Полная модель V01. Двенадцать таблиц, составные ключи в связующих таблицах и подписи кратности у каждой связи.</figcaption>

Обратите внимание на `item`. Продукция, материалы и операции живут в одном справочнике, а различаются полем `kind`. Так состав спецификации не раздваивается на две почти одинаковые таблицы.

### Шаг 5. Подпишите связи

Каждая линия идёт от внешнего ключа к первичному ключу другой таблицы. Подпись ставится по смыслу: `1` у родителя, `N` у дочерней таблицы.

| Связь | Откуда | Куда | Кратность |
|---|---|---|---|
| заказчик заказа | `customer_order.customer_id` | `counterparty.id` | 1:N |
| исполнитель заказа | `customer_order.executor_id` | `counterparty.id` | 1:N |
| строки заказа | `customer_order_line.order_id` | `customer_order.id` | 1:N |
| изделие в строке | `customer_order_line.product_id` | `item.id` | 1:N |
| спецификация изделия | `specification.product_id` | `item.id` | 1:N |
| изготовитель спецификации | `specification.manufacturer_id` | `counterparty.id` | 1:N |
| состав спецификации | `specification_component.specification_id` | `specification.id` | 1:N |
| ресурс в составе | `specification_component.item_id` | `item.id` | 1:N |
| цена ресурса | `price.item_id` | `item.id` | 1:N |
| продукция к выпуску | `production_product.production_id` | `production_order.id` | 1:N |
| изделие к выпуску | `production_product.product_id` | `item.id` | 1:N |
| расход по заказу | `production_resource.production_id` | `production_order.id` | 1:N |
| ресурс в расходе | `production_resource.item_id` | `item.id` | 1:N |
| автор заметки | `notes.id_user` | `users.id` | 1:N |

Связи многие ко многим без промежуточной таблицы быть не должно. Если у изделия много материалов, а материал входит во много изделий, между ними стоит `specification_component`.

### Шаг 6. Проверьте третью нормальную форму

К каждой таблице задайте три вопроса:

1. Есть ли ячейка с несколькими значениями? Если да, вынесите значение в отдельную строку или таблицу.
2. Зависит ли поле от части составного ключа? Если да, вынесите его в таблицу, где ключ полный.
3. Зависит ли неключевое поле от другого неключевого поля? Если да, вынесите зависимость в отдельную таблицу.

Цена материала хранится в `price`, а не в строке состава. Норма хранится в `specification_component`, а не в `item`. Часы операции хранятся в составе, а не в справочнике операций. Стоимость заказа не хранится нигде: она вычисляется запросом.

### Шаг 7. Сохраните исходник и выгрузите PDF

1. Откройте `Файл`, затем `Сохранить как` и выберите `Это устройство`.
2. Назовите файл `V01_ER.drawio` и сохраните в папку занятия.
3. Откройте `Файл`, затем `Экспорт как`, затем `PDF`.
4. Оставьте экспорт всей диаграммы, а не выделения. Проверьте, что все двенадцать таблиц попали на лист.
5. Откройте готовый PDF и увеличьте масштаб: подписи должны читаться без догадок.

<a href="reports/screens/prep/drawio-export.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-export.png" alt="Диалог экспорта PDF в draw.io с включённым экспортом всей диаграммы"></a>
<figcaption>Экспорт PDF. В диалоге не выбирайте «Только выделение», иначе на листе останется одна таблица.</figcaption>

Перед экспортом проверьте: двенадцать таблиц, у каждой первичный ключ, четырнадцать подписанных связей, нет вычисляемых полей. Если таблиц девять, скорее всего шапка заказа слита со строками. Если пятнадцать, появилась лишняя таблица под каждую строку документа.

## Задание 2. База в sqliteonline.com

### Шаг 1. Откройте sqliteonline.com

Откройте `sqliteonline.com` и выберите SQLite. Слева появится список таблиц демонстрационной базы, сверху кнопки `Import` и `Export`, в центре редактор SQL, снизу результат.

<a href="reports/screens/prep/sqlite-start.png" target="_blank" rel="noopener"><img src="reports/screens/prep/sqlite-start.png" alt="sqliteonline.com: список таблиц, редактор SQL и кнопка Run"></a>
<figcaption>sqliteonline.com. Слева база, в центре редактор, сверху запуск и импорт, снизу таблица результата.</figcaption>

Демонстрационная таблица `demo` не мешает: свои таблицы создаются рядом. Перед работой закройте зелёное уведомление, чтобы оно не закрывало результат.

### Шаг 2. Создайте таблицы

Вставьте в редактор скрипт создания схемы. В нём двенадцать таблиц, первичные и внешние ключи, проверки `CHECK` и составные ключи.

```sql
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
```

Нажмите `Run`. Слева появятся двенадцать таблиц, а в результате список имён из `sqlite_master`.

<a href="reports/screens/prep/sqlite-schema.png" target="_blank" rel="noopener"><img src="reports/screens/prep/sqlite-schema.png" alt="Схема из двенадцати таблиц в sqliteonline.com и список созданных таблиц"></a>
<figcaption>Схема создана. Слева двенадцать таблиц, в результате проверочный список имён.</figcaption>

Составной ключ записывается двумя строками `PK` или одной строкой `PRIMARY KEY (item_id, valid_from)` в конце таблицы. Внешний ключ всегда ссылается на первичный ключ другой таблицы.

### Шаг 3. Импортируйте JSON

JSON не нужно разбирать вручную. Загрузите его во временную таблицу и разверните функцией `json_each`.

```sql
CREATE TABLE json_import (payload TEXT);

INSERT INTO json_import(payload) VALUES ('[{"id":"001000001","name":"Магазин «Стежок-1»","inn":"","addres":"Учебный город, улица Производственная, 1, офис 1","phone":"+79990010001","type":"Покупатель"}]');

INSERT INTO counterparty (id, name, inn, address, phone, party_type)
SELECT json_extract(value, '$.id'),
       json_extract(value, '$.name'),
       json_extract(value, '$.inn'),
       json_extract(value, '$.addres'),
       json_extract(value, '$.phone'),
       json_extract(value, '$.type')
FROM json_import, json_each(json_import.payload);

SELECT id, name, phone, party_type FROM counterparty ORDER BY id;
```

В рабочем скрипте вставьте весь массив заказчиков из `V01_customers.json`, а не одну строку. Ключ `addres` в исходном JSON записан с одной буквой `s`, поэтому путь в `json_extract` повторяет написание источника. Если исправить путь на `address`, значение станет пустым.

<a href="reports/screens/prep/sqlite-import.png" target="_blank" rel="noopener"><img src="reports/screens/prep/sqlite-import.png" alt="Импорт JSON в sqliteonline.com: разбор через json_each и шесть строк заказчиков"></a>
<figcaption>Импорт JSON. Шесть заказчиков, ведущие нули в кодах сохранены, тип записан в поле party_type.</figcaption>

Поле `id` объявлено как `TEXT`, поэтому код `001000001` не превращается в число и не теряет ведущие нули. Это одна из типичных ошибок импорта.

### Шаг 4. Проверьте данные и ограничения

Выполните три проверки:

```sql
SELECT COUNT(*) AS customers FROM counterparty;

SELECT id, name FROM counterparty ORDER BY id LIMIT 3;

PRAGMA foreign_key_check;
```

Первая проверка возвращает `6` для шести заказчиков, вторая показывает коды и названия, третья возвращает пустой результат: внешние ключи не нарушены.

Проверьте ограничение намеренно:

```sql
INSERT INTO counterparty (id, name, party_type)
VALUES ('X-1', 'Тест', 'Клиент');
```

Запрос должен завершиться ошибкой `CHECK constraint failed`, потому что тип `Клиент` не входит в список допустимых. Если ошибки нет, `PRAGMA foreign_keys = ON` не выполнился или таблица создана по старому скрипту.

### Шаг 5. Сохраните скрипты

Скачайте готовые файлы и сохраните их в папку занятия:

- [Схема V01, SQL](reports/prep/sql/V01_schema.sql)
- [Импорт JSON V01, SQL](reports/prep/sql/V01_import.sql)
- [Расчёт стоимости V01, SQL](reports/prep/sql/V01_cost.sql)

В sqliteonline.com скрипт можно хранить в истории запросов, но на защите нужен файл. История браузера не считается артефактом.

## Задание 3. Стоимость заказа

### Шаг 1. Заполните справочники и заказ

Скрипт `V01_cost.sql` добавляет изготовителя, изделие, ресурсы, цены, спецификацию, заказ и производственный заказ. Ключевые строки:

```sql
INSERT INTO item (id, code, name, kind, unit) VALUES
    (1, 'P-01', 'Фартук поварской', 'product', 'шт'),
    (2, 'M-01', 'Бязь', 'material', 'м'),
    (3, 'M-02', 'Тесьма', 'material', 'м'),
    (4, 'M-03', 'Нить', 'material', 'м'),
    (5, 'O-01', 'Раскрой', 'operation', 'ч'),
    (6, 'O-02', 'Пошив', 'operation', 'ч');

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
```

Для материалов `qty` в составе это норма на единицу, а `time_norm` равно `1`. Для операций `qty` равно `1`, а `time_norm` хранит часы на единицу. Такая запись позволяет считать материалы и операции одной формулой.

### Шаг 2. Соберите запрос

Сначала выберите цену, действующую на дату заказа. Затем соедините заказ, строки, спецификацию, состав и цену. Формула:

```text
количество в заказе / выпуск по спецификации × норма × коэффициент времени × цена
```

Для материалов коэффициент времени равен `1`, для операций он равен часам. Итог округляется один раз, после суммы.

```sql
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
```

<a href="reports/screens/prep/sqlite-query.png" target="_blank" rel="noopener"><img src="reports/screens/prep/sqlite-query.png" alt="Запрос стоимости заказа в sqliteonline.com и результат 7680"></a>
<figcaption>Запрос с общим табличным выражением. В результате одна строка V01-01 со стоимостью 7680.</figcaption>

Если соединить `price` и `specification_component` без подготовки, строки начнут размножаться: каждая строка состава получит несколько цен. Общее табличное выражение `price_on_date` оставляет одну действующую цену на ресурс.

### Шаг 3. Проверьте результат

<a href="reports/screens/prep/sqlite-cost.png" target="_blank" rel="noopener"><img src="reports/screens/prep/sqlite-cost.png" alt="Результат расчёта стоимости: материалы 3456, операции 4224, итог 7680"></a>
<figcaption>Итоговая строка: материалы 3456, операции 4224, общая стоимость 7680.</figcaption>

Проверьте арифметику вручную:

```text
Материалы на единицу: 0,8 × 280 + 2 × 25 + 35 × 0,4 = 224 + 50 + 14 = 288
Операции на единицу: 0,12 × 600 + 0,35 × 800 = 72 + 280 = 352
Стоимость единицы: 288 + 352 = 640
Заказ на 12 единиц: 640 × 12 = 7680
```

Если получилось 15360, строки удвоились из-за соединения. Если получилось 3456 или 4224, в сумму попала только одна часть. Если получилось 7680 без копеек, проверьте, что `ROUND` стоит после `SUM`, а не внутри каждого слагаемого.

### Шаг 4. Проверьте на другом количестве

Измените количество в заказе на `10` и выполните запрос снова. Ожидаемый итог `6400`. Затем верните `12`. Такая проверка показывает, что формула зависит от количества, а не от случайного совпадения.

## Проверка варианта V01

| Артефакт | Что должно быть |
|---|---|
| `V01_ER.drawio` | двенадцать таблиц, ключи, четырнадцать связей |
| `V01_ER.pdf` | читаемая диаграмма на одном листе |
| `V01_schema.sql` | двенадцать таблиц, `PRIMARY KEY`, `FOREIGN KEY`, `CHECK` |
| `V01_import.sql` | разбор JSON через `json_each`, шесть заказчиков |
| `V01_cost.sql` | запрос стоимости и результат `7680.00` |

## Варианты V02 и V03

Повторите три задания на другом наборе. Структура модели не меняется, поэтому диаграмму можно взять за основу и заменить только названия и числа.

| Вариант | Материалы на единицу | Операции на единицу | Итог |
|---|---|---|---|
| V02, 40 единиц | 32.80 | 34.00 | 2672.00 |
| V03, 18 единиц | 122.50 | 435.00 | 10035.00 |

<details>
<summary>Проверка расчёта V02</summary>

```text
Мука: 0,32 × 65 = 20,80
Закваска: 0,08 × 100 = 8,00
Пакет: 1 × 4 = 4,00
Материалы: 32,80
Замес: 0,04 × 500 = 20,00
Выпечка: 0,02 × 700 = 14,00
Операции: 34,00
Стоимость единицы: 66,80
Заказ: 66,80 × 40 = 2672,00
```

</details>

<details>
<summary>Проверка расчёта V03</summary>

```text
Глина: 0,45 × 120 = 54,00
Глазурь: 0,03 × 950 = 28,50
Коробка: 1 × 40 = 40,00
Материалы: 122,50
Формовка: 0,4 × 750 = 300,00
Глазурование и обжиг: 0,15 × 900 = 135,00
Операции: 435,00
Стоимость единицы: 557,50
Заказ: 557,50 × 18 = 10035,00
```

</details>

## Чек-лист подготовки

- Диаграмма содержит двенадцать таблиц, а не только шапки документов.
- У каждой таблицы есть первичный ключ, у связующих таблиц ключ составной.
- Каждый внешний ключ соединён линией с первичным ключом другой таблицы.
- У каждой связи подписана кратность, связей многие ко многим без промежуточной таблицы нет.
- В таблицах нет вычисляемых полей: стоимости, суммы строки и количества изделий.
- Схема базы создаётся одним скриптом, ограничения `CHECK` и `FOREIGN KEY` включены.
- JSON импортируется через `json_each`, ведущие нули в кодах сохранены.
- Запрос стоимости использует действующую цену и не удваивает строки.
- Итог `7680.00` подтверждён ручным расчётом.
- Исходник `.drawio`, PDF и SQL-скрипты сохранены в папке занятия.

Дальше переходите к методичкам заданий 4, 5 и 6: приложение, API и документация собираются на той же модели данных.
