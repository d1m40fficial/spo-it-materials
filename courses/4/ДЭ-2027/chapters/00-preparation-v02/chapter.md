---
title: "Предварительная подготовка: вариант V02"
dek: "Разбор V02 на данных пекарни «Колос»: откуда берутся таблицы, как создать их запросами, добавить связи и вставить строки."
chapter: "Подготовка V02"
level: СПО
glyph: "00B"
outcomes:
  - Объяснять, из каких файлов и полей получается каждая таблица
  - Создавать таблицы запросами и добавлять связи через ALTER TABLE
  - Загружать данные V02 и считать стоимость заказа запросом
---

## Чем V02 отличается от V01

Первый разбор построен на мебельном производстве. Здесь то же устройство базы, но другие предприятие, продукция, ресурсы и числа. Схема таблиц не меняется: меняются строки данных. Разбор V01 находится на странице [Предварительная подготовка: вариант V01](00-preparation.html).

| Что | V01 | V02 |
|---|---|---|
| Предприятие | ООО ТД «Вершина» | Пекарня «Колос» |
| Продукция | Стол кухонный «Самобранка» | Хлеб ржаной 500 г |
| Количество | 2 | 40 |
| Заказ | V01-01 от 22.04.2026 | V02-01 от 15.03.2027 |
| Цены | с 01.04.2026 | с 01.03.2027 |
| Материалы | столешница, детали, евровинты, опоры | мука, закваска, пакет |
| Операции | сборка, распил, упаковка | замес и формование, выпечка |

Скачать файлы варианта: [V02_исходные_данные.zip](reports/variants/V02/V02_исходные_данные.zip).

<figure class="diagram">
<img src="reports/screens/prep/V02_order_xlsx.png" alt="Заказ покупателя V02: номер, дата, заказчик и продукция">
<figcaption>Заказ V02-01: заказчик Магазин «Колос-1», изделие «Хлеб ржаной 500 г», количество 40.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/prep/V02_spec_xlsx.png" alt="Спецификация V02: материалы, операции и нормы">
<figcaption>Спецификация: три материала и две операции с нормами на одну буханку.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/prep/V02_prices_xlsx.png" alt="Цены V02: ресурс, цена и дата">
<figcaption>Цены: у каждого ресурса указана цена и дата начала действия 01.03.2027.</figcaption>
</figure>

## Задание 1. ER-диаграмма

Для V02 меняются предприятие, продукция и ресурсы, но набор из двенадцати таблиц и четырнадцати связей остаётся тем же. Пошаговая сборка диаграммы в draw.io находится в методичке [Задание 1. ER-диаграмма](02-task-1-er.html). Подставляйте данные V02: изделие «Хлеб ржаной 500 г», материалы «Мука ржаная», «Закваска», «Пакет», операции «Замес и формование» и «Выпечка».

## Задание 2. База данных и импорт

Запустите Apache и MySQL в XAMPP. В phpMyAdmin создайте базу `dkip2027_v02` в кодировке `utf8mb4` и сравнении `utf8mb4_unicode_ci`. Дальше все запросы выполняйте в этой базе.

```sql
CREATE DATABASE dkip2027_v02
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

### Как из файлов получаются таблицы

Первый слайдер показывает, откуда взялась каждая таблица: какой файл или документ её породил, какие поля в неё попадают и почему. Листайте стрелками.

<div class="schema-slider" data-slider>
<div class="schema-slider-bar">
<strong>Откуда берутся таблицы: V02, 12 слайдов</strong>
<div class="schema-slider-actions">
<button type="button" class="schema-btn" data-slider-prev aria-label="Предыдущий слайд">←</button>
<span class="schema-slider-counter" data-slider-counter>1 / 12</span>
<button type="button" class="schema-btn" data-slider-next aria-label="Следующий слайд">→</button>
</div>
</div>
<div class="schema-track" data-slider-track>
<article class="schema-slide" aria-label="counterparty">
<h4>1. <code>counterparty</code></h4>
<p>Кто участвует в системе: покупатели, поставщики и изготовители. Одна таблица вместо трёх справочников, роль хранится в поле party_type.</p>
<p><b>Откуда берём:</b> Заказчики.json: шесть записей. Заказ покупателя.xlsx: блоки «Заказчик» и «Исполнитель». Для V02 добавляется изготовитель Пекарня «Колос». Заказчик Магазин «Колос-1» уже есть в JSON.</p>
<table class="schema-lines"><thead><tr><th>Поле</th><th>Откуда значение и почему</th></tr></thead><tbody><tr><td><code>id</code></td><td>JSON id 002000001...002000006; для изготовителя M-001.</td></tr><tr><td><code>name</code></td><td>JSON name; из заказа название заказчика и исполнителя.</td></tr><tr><td><code>inn</code></td><td>JSON inn; пустая строка, если ИНН нет.</td></tr><tr><td><code>address</code></td><td>JSON addres; в таблице address.</td></tr><tr><td><code>phone</code></td><td>JSON phone.</td></tr><tr><td><code>party_type</code></td><td>JSON type: Покупатель, Поставщик или Изготовитель.</td></tr></tbody></table>
</article>
<article class="schema-slide" aria-label="item">
<h4>2. <code>item</code></h4>
<p>Один справочник ресурсов: продукция, материалы и операции. Поле kind говорит, как ресурс участвует в расчёте.</p>
<p><b>Откуда берём:</b> Заказ покупателя.xlsx: строка продукции. Спецификация.xlsx и Цены.xlsx: материалы, операции, единицы. Заказ на производство.xlsx: коды и плановые наименования.</p>
<table class="schema-lines"><thead><tr><th>Поле</th><th>Откуда значение и почему</th></tr></thead><tbody><tr><td><code>id</code></td><td>Номер по порядку: 1 продукция, далее материалы и операции.</td></tr><tr><td><code>code</code></td><td>Код из заказа и производства: P-01, M-01...M-03, O-01, O-02.</td></tr><tr><td><code>name</code></td><td>Название из строки продукции и таблиц спецификации.</td></tr><tr><td><code>kind</code></td><td>product для изделия, material для материалов, operation для операций.</td></tr><tr><td><code>unit</code></td><td>Единица из спецификации и цен.</td></tr></tbody></table>
</article>
<article class="schema-slide" aria-label="price">
<h4>3. <code>price</code></h4>
<p>История цен. Цена не хранится в item, потому что со временем меняется.</p>
<p><b>Откуда берём:</b> Цены.xlsx: столбцы «Номенклатура» и «Цена». Дата начала действия задана условием варианта.</p>
<table class="schema-lines"><thead><tr><th>Поле</th><th>Откуда значение и почему</th></tr></thead><tbody><tr><td><code>item_id</code></td><td>Код ресурса из item, а не название. Название может измениться.</td></tr><tr><td><code>valid_from</code></td><td>2027-03-01 для V02.</td></tr><tr><td><code>amount</code></td><td>Цена из строки ресурса в Цены.xlsx.</td></tr></tbody></table>
</article>
<article class="schema-slide" aria-label="specification">
<h4>4. <code>specification</code></h4>
<p>Шапка спецификации: какое изделие и на какое количество выпуска описано.</p>
<p><b>Откуда берём:</b> Спецификация.xlsx: шапка «Изделие», «Изготовитель», нормы на одну единицу.</p>
<table class="schema-lines"><thead><tr><th>Поле</th><th>Откуда значение и почему</th></tr></thead><tbody><tr><td><code>id</code></td><td>1, потому что в варианте одна спецификация.</td></tr><tr><td><code>product_id</code></td><td>1, ссылка на изделие в item.</td></tr><tr><td><code>name</code></td><td>Название изделия из шапки.</td></tr><tr><td><code>output_qty</code></td><td>1, нормы даны на одну единицу.</td></tr><tr><td><code>manufacturer_id</code></td><td>M-001, изготовитель из шапки.</td></tr></tbody></table>
</article>
<article class="schema-slide" aria-label="specification_component">
<h4>5. <code>specification_component</code></h4>
<p>Строки состава: сколько материала нужно на единицу и сколько часов занимает операция.</p>
<p><b>Откуда берём:</b> Спецификация.xlsx: таблицы «Состав» и «Технологические операции».</p>
<table class="schema-lines"><thead><tr><th>Поле</th><th>Откуда значение и почему</th></tr></thead><tbody><tr><td><code>specification_id</code></td><td>1, ссылка на шапку.</td></tr><tr><td><code>item_id</code></td><td>Код материала или операции из item.</td></tr><tr><td><code>qty</code></td><td>Норма расхода материала из столбца «Норма расхода».</td></tr><tr><td><code>time_norm</code></td><td>Норма времени операции из столбца «Норма времени».</td></tr></tbody></table>
</article>
<article class="schema-slide" aria-label="customer_order">
<h4>6. <code>customer_order</code></h4>
<p>Шапка заказа покупателя: номер, дата, заказчик и исполнитель.</p>
<p><b>Откуда берём:</b> Заказ покупателя.xlsx: шапка заказа.</p>
<table class="schema-lines"><thead><tr><th>Поле</th><th>Откуда значение и почему</th></tr></thead><tbody><tr><td><code>id</code></td><td>1, внутренний номер.</td></tr><tr><td><code>doc_no</code></td><td>V02-01.</td></tr><tr><td><code>doc_date</code></td><td>15.03.2027.</td></tr><tr><td><code>customer_id</code></td><td>002000001, Магазин «Колос-1».</td></tr><tr><td><code>executor_id</code></td><td>M-001, Пекарня «Колос».</td></tr></tbody></table>
</article>
<article class="schema-slide" aria-label="customer_order_line">
<h4>7. <code>customer_order_line</code></h4>
<p>Строки заказа: какое изделие, сколько, по какой продажной цене и со скидкой.</p>
<p><b>Откуда берём:</b> Заказ покупателя.xlsx: строка «Товары (работы, услуги)».</p>
<table class="schema-lines"><thead><tr><th>Поле</th><th>Откуда значение и почему</th></tr></thead><tbody><tr><td><code>id</code></td><td>1, одна строка заказа.</td></tr><tr><td><code>order_id</code></td><td>1, ссылка на шапку.</td></tr><tr><td><code>product_id</code></td><td>1, ссылка на изделие.</td></tr><tr><td><code>qty</code></td><td>40.</td></tr><tr><td><code>sale_price</code></td><td>700.00.</td></tr><tr><td><code>discount</code></td><td>0.00.</td></tr></tbody></table>
</article>
<article class="schema-slide" aria-label="production_order">
<h4>8. <code>production_order</code></h4>
<p>Шапка производственного заказа: номер, дата, дата запуска и подразделение.</p>
<p><b>Откуда берём:</b> Заказ на производство.xlsx: шапка.</p>
<table class="schema-lines"><thead><tr><th>Поле</th><th>Откуда значение и почему</th></tr></thead><tbody><tr><td><code>id</code></td><td>1, внутренний номер.</td></tr><tr><td><code>doc_no</code></td><td>V02-P01.</td></tr><tr><td><code>doc_date</code></td><td>15.03.2027, дата заказа.</td></tr><tr><td><code>launch_date</code></td><td>16.03.2027.</td></tr><tr><td><code>department</code></td><td>Основное производство.</td></tr></tbody></table>
</article>
<article class="schema-slide" aria-label="production_product">
<h4>9. <code>production_product</code></h4>
<p>Что выпускаем по производственному заказу и в каком количестве.</p>
<p><b>Откуда берём:</b> Заказ на производство.xlsx: «Продукция к выпуску».</p>
<table class="schema-lines"><thead><tr><th>Поле</th><th>Откуда значение и почему</th></tr></thead><tbody><tr><td><code>production_id</code></td><td>1, ссылка на производственный заказ.</td></tr><tr><td><code>product_id</code></td><td>1, ссылка на изделие.</td></tr><tr><td><code>qty</code></td><td>40.</td></tr></tbody></table>
</article>
<article class="schema-slide" aria-label="production_resource">
<h4>10. <code>production_resource</code></h4>
<p>Плановый расход материалов и времени по производственному заказу.</p>
<p><b>Откуда берём:</b> Заказ на производство.xlsx: «Потребность в материалах» и «Технологические операции».</p>
<table class="schema-lines"><thead><tr><th>Поле</th><th>Откуда значение и почему</th></tr></thead><tbody><tr><td><code>production_id</code></td><td>1, ссылка на заказ.</td></tr><tr><td><code>item_id</code></td><td>Код материала или операции.</td></tr><tr><td><code>qty</code></td><td>Плановое количество материала.</td></tr><tr><td><code>time_norm</code></td><td>Плановые часы операции.</td></tr></tbody></table>
</article>
<article class="schema-slide" aria-label="users">
<h4>11. <code>users</code></h4>
<p>Учётные записи приложения: логин, хеш пароля, роль и блокировка.</p>
<p><b>Откуда берём:</b> Требования задания 4. В Excel и JSON этих данных нет.</p>
<table class="schema-lines"><thead><tr><th>Поле</th><th>Откуда значение и почему</th></tr></thead><tbody><tr><td><code>id</code></td><td>AUTO_INCREMENT, сервер сам выдаёт номер.</td></tr><tr><td><code>login</code></td><td>Логин пользователя.</td></tr><tr><td><code>password_hash</code></td><td>Хеш пароля.</td></tr><tr><td><code>salt</code></td><td>Соль.</td></tr><tr><td><code>role</code></td><td>admin или user.</td></tr><tr><td><code>failed_attempts</code></td><td>Счётчик ошибок.</td></tr><tr><td><code>is_locked</code></td><td>Блокировка.</td></tr></tbody></table>
</article>
<article class="schema-slide" aria-label="notes">
<h4>12. <code>notes</code></h4>
<p>Заметки сотрудников. Автор хранится ссылкой на users.</p>
<p><b>Откуда берём:</b> Заметки.json: пять записей.</p>
<table class="schema-lines"><thead><tr><th>Поле</th><th>Откуда значение и почему</th></tr></thead><tbody><tr><td><code>id</code></td><td>AUTO_INCREMENT.</td></tr><tr><td><code>title</code></td><td>Поле title.</td></tr><tr><td><code>content</code></td><td>Поле content.</td></tr><tr><td><code>id_user</code></td><td>Пользователь по login: manager 2, technologist 3, master 4.</td></tr><tr><td><code>created_at</code></td><td>Поле created_date.</td></tr></tbody></table>
</article>
</div>
</div>

### Создание таблиц построчно

Перед запросами откройте шпаргалку.

<details class="hint">
<summary>Шпаргалка: CREATE TABLE</summary>

```sql
CREATE TABLE имя_таблицы (
  имя_поля ТИП ОГРАНИЧЕНИЕ,
  имя_поля ТИП ОГРАНИЧЕНИЕ,
  PRIMARY KEY (имя_поля)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

`CREATE TABLE` создаёт таблицу. В скобках перечисляются поля, затем ключи и проверки. Каждое поле описывается тремя частями: имя, тип и ограничение. Запятая разделяет описания, после последнего запятая не ставится.

</details>

Второй слайдер разбирает создание таблиц построчно. В конце каждого слайда есть полный скрипт для проверки.

<div class="schema-slider" data-slider>
<div class="schema-slider-bar">
<strong>Создание всех таблиц построчно: 12 слайдов</strong>
<div class="schema-slider-actions">
<button type="button" class="schema-btn" data-slider-prev aria-label="Предыдущий слайд">←</button>
<span class="schema-slider-counter" data-slider-counter>1 / 12</span>
<button type="button" class="schema-btn" data-slider-next aria-label="Следующий слайд">→</button>
</div>
</div>
<div class="schema-track" data-slider-track>
<article class="schema-slide" aria-label="counterparty">
<h4>1. <code>counterparty</code></h4>
<p>Кто участвует в системе: покупатели, поставщики и изготовители. Одна таблица вместо трёх справочников, роль хранится в поле party_type.</p>
<table class="schema-lines"><thead><tr><th>Строка</th><th>Что означает и почему</th></tr></thead><tbody><tr><td><code>id VARCHAR(32) NOT NULL,</code></td><td>Код контрагента. В JSON это id, для изготовителя код назначается вручную. Ведущие нули сохраняются, поэтому тип VARCHAR.</td></tr><tr><td><code>name VARCHAR(255) NOT NULL,</code></td><td>Название из name JSON или из блока «Заказчик»/«Исполнитель» заказа.</td></tr><tr><td><code>inn VARCHAR(20) NOT NULL DEFAULT &#x27;&#x27;,</code></td><td>ИНН из inn. Если его нет, DEFAULT &#x27;&#x27; подставляет пустую строку.</td></tr><tr><td><code>address VARCHAR(500) NOT NULL,</code></td><td>Адрес из addres. В таблице поле называется address.</td></tr><tr><td><code>phone VARCHAR(64) NOT NULL,</code></td><td>Телефон из phone.</td></tr><tr><td><code>party_type VARCHAR(24) NOT NULL,</code></td><td>Тип из type: Покупатель, Поставщик или Изготовитель.</td></tr><tr><td><code>PRIMARY KEY (id),</code></td><td>Первичный ключ делает строку узнаваемой и запрещает пустое значение.</td></tr><tr><td><code>CONSTRAINT ck_party_type</code></td><td>Проверка разрешает только три роли контрагента.</td></tr><tr><td><code>CHECK (party_type IN (&#x27;Покупатель&#x27;, &#x27;Поставщик&#x27;, &#x27;Изготовитель&#x27;))</code></td><td>Список допустимых ролей: покупатель, поставщик, изготовитель.</td></tr></tbody></table>
<p><b>Полный скрипт для проверки</b></p>
<pre><code>CREATE TABLE counterparty (
  id VARCHAR(32) NOT NULL,
  name VARCHAR(255) NOT NULL,
  inn VARCHAR(20) NOT NULL DEFAULT &#x27;&#x27;,
  address VARCHAR(500) NOT NULL,
  phone VARCHAR(64) NOT NULL,
  party_type VARCHAR(24) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT ck_party_type
    CHECK (party_type IN (&#x27;Покупатель&#x27;, &#x27;Поставщик&#x27;, &#x27;Изготовитель&#x27;))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="item">
<h4>2. <code>item</code></h4>
<p>Один справочник ресурсов: продукция, материалы и операции. Поле kind говорит, как ресурс участвует в расчёте.</p>
<table class="schema-lines"><thead><tr><th>Строка</th><th>Что означает и почему</th></tr></thead><tbody><tr><td><code>id INT NOT NULL,</code></td><td>Внутренний номер ресурса. Назначаем по порядку: 1 продукция, затем материалы и операции.</td></tr><tr><td><code>code VARCHAR(64) DEFAULT NULL,</code></td><td>Код из документа: ФР-00000034 у стола, ФР-00000009 у столешницы и так далее. UNIQUE не даёт повторять код.</td></tr><tr><td><code>name VARCHAR(255) NOT NULL,</code></td><td>Название из заказа, спецификации или цен.</td></tr><tr><td><code>kind VARCHAR(16) NOT NULL,</code></td><td>product, material или operation. По этому полю запрос понимает, что считать.</td></tr><tr><td><code>unit VARCHAR(16) NOT NULL,</code></td><td>Единица из спецификации или цен: шт, тыс. шт, ч.</td></tr><tr><td><code>PRIMARY KEY (id),</code></td><td>Первичный ключ делает строку узнаваемой и запрещает пустое значение.</td></tr><tr><td><code>UNIQUE KEY uq_item_code (code),</code></td><td>Уникальный индекс не даёт двум строкам получить одинаковое значение.</td></tr><tr><td><code>CONSTRAINT ck_item_kind</code></td><td>Проверка разрешает только три вида ресурса.</td></tr><tr><td><code>CHECK (kind IN (&#x27;product&#x27;, &#x27;material&#x27;, &#x27;operation&#x27;))</code></td><td>Список допустимых видов: product, material, operation.</td></tr></tbody></table>
<p><b>Полный скрипт для проверки</b></p>
<pre><code>CREATE TABLE item (
  id INT NOT NULL,
  code VARCHAR(64) DEFAULT NULL,
  name VARCHAR(255) NOT NULL,
  kind VARCHAR(16) NOT NULL,
  unit VARCHAR(16) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_item_code (code),
  CONSTRAINT ck_item_kind
    CHECK (kind IN (&#x27;product&#x27;, &#x27;material&#x27;, &#x27;operation&#x27;))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="price">
<h4>3. <code>price</code></h4>
<p>История цен. Цена не хранится в item, потому что со временем меняется.</p>
<table class="schema-lines"><thead><tr><th>Строка</th><th>Что означает и почему</th></tr></thead><tbody><tr><td><code>item_id INT NOT NULL,</code></td><td>Ссылка на ресурс в item.</td></tr><tr><td><code>valid_from DATE NOT NULL,</code></td><td>Дата начала действия цены.</td></tr><tr><td><code>amount DECIMAL(14,2) NOT NULL,</code></td><td>Цена из файла Цены.xlsx.</td></tr><tr><td><code>PRIMARY KEY (item_id, valid_from),</code></td><td>Первичный ключ делает строку узнаваемой и запрещает пустое значение.</td></tr><tr><td><code>CONSTRAINT ck_price_amount CHECK (amount &gt;= 0)</code></td><td>Цена не может быть отрицательной.</td></tr></tbody></table>
<p><b>Полный скрипт для проверки</b></p>
<pre><code>CREATE TABLE price (
  item_id INT NOT NULL,
  valid_from DATE NOT NULL,
  amount DECIMAL(14,2) NOT NULL,
  PRIMARY KEY (item_id, valid_from),
  CONSTRAINT ck_price_amount CHECK (amount &gt;= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="specification">
<h4>4. <code>specification</code></h4>
<p>Шапка спецификации: какое изделие и на какое количество выпуска описано.</p>
<table class="schema-lines"><thead><tr><th>Строка</th><th>Что означает и почему</th></tr></thead><tbody><tr><td><code>id INT NOT NULL,</code></td><td>Номер спецификации.</td></tr><tr><td><code>product_id INT NOT NULL,</code></td><td>Ссылка на изделие в item.</td></tr><tr><td><code>name VARCHAR(255) NOT NULL,</code></td><td>Название изделия из шапки спецификации.</td></tr><tr><td><code>output_qty DECIMAL(14,3) NOT NULL,</code></td><td>На какое количество изделий даны нормы.</td></tr><tr><td><code>manufacturer_id VARCHAR(32) NOT NULL,</code></td><td>Код изготовителя из блока «Исполнитель».</td></tr><tr><td><code>PRIMARY KEY (id),</code></td><td>Первичный ключ делает строку узнаваемой и запрещает пустое значение.</td></tr><tr><td><code>UNIQUE KEY uq_spec_product (product_id),</code></td><td>Уникальный индекс не даёт двум строкам получить одинаковое значение.</td></tr><tr><td><code>KEY ix_spec_maker (manufacturer_id),</code></td><td>Обычный индекс ускоряет поиск по внешнему ключу.</td></tr><tr><td><code>CONSTRAINT ck_spec_output CHECK (output_qty &gt; 0)</code></td><td>Количество выпуска должно быть больше нуля.</td></tr></tbody></table>
<p><b>Полный скрипт для проверки</b></p>
<pre><code>CREATE TABLE specification (
  id INT NOT NULL,
  product_id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  output_qty DECIMAL(14,3) NOT NULL,
  manufacturer_id VARCHAR(32) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_spec_product (product_id),
  KEY ix_spec_maker (manufacturer_id),
  CONSTRAINT ck_spec_output CHECK (output_qty &gt; 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="specification_component">
<h4>5. <code>specification_component</code></h4>
<p>Строки состава: сколько материала нужно на единицу и сколько часов занимает операция.</p>
<table class="schema-lines"><thead><tr><th>Строка</th><th>Что означает и почему</th></tr></thead><tbody><tr><td><code>specification_id INT NOT NULL,</code></td><td>Ссылка на шапку спецификации.</td></tr><tr><td><code>item_id INT NOT NULL,</code></td><td>Ссылка на материал или операцию в item.</td></tr><tr><td><code>qty DECIMAL(14,3) NOT NULL,</code></td><td>Норма расхода материала. Для операции ставим 0.</td></tr><tr><td><code>time_norm DECIMAL(14,3) NOT NULL,</code></td><td>Часы операции. Для материала ставим 0.</td></tr><tr><td><code>PRIMARY KEY (specification_id, item_id),</code></td><td>Первичный ключ делает строку узнаваемой и запрещает пустое значение.</td></tr><tr><td><code>KEY ix_comp_item (item_id),</code></td><td>Обычный индекс ускоряет поиск по внешнему ключу.</td></tr><tr><td><code>CONSTRAINT ck_comp_qty CHECK (qty &gt;= 0),</code></td><td>Норма расхода не может быть отрицательной.</td></tr><tr><td><code>CONSTRAINT ck_comp_time CHECK (time_norm &gt;= 0)</code></td><td>Время операции не может быть отрицательным.</td></tr></tbody></table>
<p><b>Полный скрипт для проверки</b></p>
<pre><code>CREATE TABLE specification_component (
  specification_id INT NOT NULL,
  item_id INT NOT NULL,
  qty DECIMAL(14,3) NOT NULL,
  time_norm DECIMAL(14,3) NOT NULL,
  PRIMARY KEY (specification_id, item_id),
  KEY ix_comp_item (item_id),
  CONSTRAINT ck_comp_qty CHECK (qty &gt;= 0),
  CONSTRAINT ck_comp_time CHECK (time_norm &gt;= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="customer_order">
<h4>6. <code>customer_order</code></h4>
<p>Шапка заказа покупателя: номер, дата, заказчик и исполнитель.</p>
<table class="schema-lines"><thead><tr><th>Строка</th><th>Что означает и почему</th></tr></thead><tbody><tr><td><code>id INT NOT NULL,</code></td><td>Внутренний номер заказа.</td></tr><tr><td><code>doc_no VARCHAR(64) NOT NULL,</code></td><td>Номер документа из шапки заказа.</td></tr><tr><td><code>doc_date DATE NOT NULL,</code></td><td>Дата заказа из шапки Excel.</td></tr><tr><td><code>customer_id VARCHAR(32) NOT NULL,</code></td><td>Код заказчика из блока «Заказчик».</td></tr><tr><td><code>executor_id VARCHAR(32) NOT NULL,</code></td><td>Код изготовителя из блока «Исполнитель».</td></tr><tr><td><code>PRIMARY KEY (id),</code></td><td>Первичный ключ делает строку узнаваемой и запрещает пустое значение.</td></tr><tr><td><code>UNIQUE KEY uq_order_doc (doc_no),</code></td><td>Уникальный индекс не даёт двум строкам получить одинаковое значение.</td></tr><tr><td><code>KEY ix_order_customer (customer_id),</code></td><td>Обычный индекс ускоряет поиск по внешнему ключу.</td></tr><tr><td><code>KEY ix_order_executor (executor_id)</code></td><td>Обычный индекс ускоряет поиск по внешнему ключу.</td></tr></tbody></table>
<p><b>Полный скрипт для проверки</b></p>
<pre><code>CREATE TABLE customer_order (
  id INT NOT NULL,
  doc_no VARCHAR(64) NOT NULL,
  doc_date DATE NOT NULL,
  customer_id VARCHAR(32) NOT NULL,
  executor_id VARCHAR(32) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_order_doc (doc_no),
  KEY ix_order_customer (customer_id),
  KEY ix_order_executor (executor_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="customer_order_line">
<h4>7. <code>customer_order_line</code></h4>
<p>Строки заказа: какое изделие, сколько, по какой продажной цене и со скидкой.</p>
<table class="schema-lines"><thead><tr><th>Строка</th><th>Что означает и почему</th></tr></thead><tbody><tr><td><code>id INT NOT NULL,</code></td><td>Номер строки заказа.</td></tr><tr><td><code>order_id INT NOT NULL,</code></td><td>Ссылка на шапку customer_order.</td></tr><tr><td><code>product_id INT NOT NULL,</code></td><td>Ссылка на изделие в item.</td></tr><tr><td><code>qty INT NOT NULL,</code></td><td>Количество изделий из строки продукции.</td></tr><tr><td><code>sale_price DECIMAL(14,2) NOT NULL,</code></td><td>Продажная цена из строки продукции.</td></tr><tr><td><code>discount DECIMAL(14,2) NOT NULL DEFAULT 0.00,</code></td><td>Скидка из строки продукции. Если скидки нет, 0.</td></tr><tr><td><code>PRIMARY KEY (id),</code></td><td>Первичный ключ делает строку узнаваемой и запрещает пустое значение.</td></tr><tr><td><code>KEY ix_line_order (order_id),</code></td><td>Обычный индекс ускоряет поиск по внешнему ключу.</td></tr><tr><td><code>KEY ix_line_product (product_id),</code></td><td>Обычный индекс ускоряет поиск по внешнему ключу.</td></tr><tr><td><code>CONSTRAINT ck_line_qty CHECK (qty &gt; 0),</code></td><td>Количество в заказе больше нуля.</td></tr><tr><td><code>CONSTRAINT ck_line_price CHECK (sale_price &gt;= 0),</code></td><td>Продажная цена не может быть отрицательной.</td></tr><tr><td><code>CONSTRAINT ck_line_discount CHECK (discount &gt;= 0)</code></td><td>Скидка не может быть отрицательной.</td></tr></tbody></table>
<p><b>Полный скрипт для проверки</b></p>
<pre><code>CREATE TABLE customer_order_line (
  id INT NOT NULL,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  qty INT NOT NULL,
  sale_price DECIMAL(14,2) NOT NULL,
  discount DECIMAL(14,2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (id),
  KEY ix_line_order (order_id),
  KEY ix_line_product (product_id),
  CONSTRAINT ck_line_qty CHECK (qty &gt; 0),
  CONSTRAINT ck_line_price CHECK (sale_price &gt;= 0),
  CONSTRAINT ck_line_discount CHECK (discount &gt;= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="production_order">
<h4>8. <code>production_order</code></h4>
<p>Шапка производственного заказа: номер, дата, дата запуска и подразделение.</p>
<table class="schema-lines"><thead><tr><th>Строка</th><th>Что означает и почему</th></tr></thead><tbody><tr><td><code>id INT NOT NULL,</code></td><td>Внутренний номер производственного заказа.</td></tr><tr><td><code>doc_no VARCHAR(64) NOT NULL,</code></td><td>Номер производственного заказа.</td></tr><tr><td><code>doc_date DATE NOT NULL,</code></td><td>Дата создания. Берём дату заказа покупателя.</td></tr><tr><td><code>launch_date DATE NOT NULL,</code></td><td>Дата запуска из шапки производственного заказа.</td></tr><tr><td><code>department VARCHAR(128) NOT NULL,</code></td><td>Подразделение из шапки.</td></tr><tr><td><code>PRIMARY KEY (id),</code></td><td>Первичный ключ делает строку узнаваемой и запрещает пустое значение.</td></tr><tr><td><code>UNIQUE KEY uq_prod_doc (doc_no)</code></td><td>Уникальный индекс не даёт двум строкам получить одинаковое значение.</td></tr></tbody></table>
<p><b>Полный скрипт для проверки</b></p>
<pre><code>CREATE TABLE production_order (
  id INT NOT NULL,
  doc_no VARCHAR(64) NOT NULL,
  doc_date DATE NOT NULL,
  launch_date DATE NOT NULL,
  department VARCHAR(128) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_prod_doc (doc_no)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="production_product">
<h4>9. <code>production_product</code></h4>
<p>Что выпускаем по производственному заказу и в каком количестве.</p>
<table class="schema-lines"><thead><tr><th>Строка</th><th>Что означает и почему</th></tr></thead><tbody><tr><td><code>production_id INT NOT NULL,</code></td><td>Ссылка на производственный заказ.</td></tr><tr><td><code>product_id INT NOT NULL,</code></td><td>Ссылка на изделие в item.</td></tr><tr><td><code>qty INT NOT NULL,</code></td><td>Количество к выпуску из строки «Продукция к выпуску».</td></tr><tr><td><code>PRIMARY KEY (production_id, product_id),</code></td><td>Первичный ключ делает строку узнаваемой и запрещает пустое значение.</td></tr><tr><td><code>KEY ix_prod_product (product_id),</code></td><td>Обычный индекс ускоряет поиск по внешнему ключу.</td></tr><tr><td><code>CONSTRAINT ck_pp_qty CHECK (qty &gt; 0)</code></td><td>Количество к выпуску больше нуля.</td></tr></tbody></table>
<p><b>Полный скрипт для проверки</b></p>
<pre><code>CREATE TABLE production_product (
  production_id INT NOT NULL,
  product_id INT NOT NULL,
  qty INT NOT NULL,
  PRIMARY KEY (production_id, product_id),
  KEY ix_prod_product (product_id),
  CONSTRAINT ck_pp_qty CHECK (qty &gt; 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="production_resource">
<h4>10. <code>production_resource</code></h4>
<p>Плановый расход материалов и времени по производственному заказу.</p>
<table class="schema-lines"><thead><tr><th>Строка</th><th>Что означает и почему</th></tr></thead><tbody><tr><td><code>production_id INT NOT NULL,</code></td><td>Ссылка на производственный заказ.</td></tr><tr><td><code>item_id INT NOT NULL,</code></td><td>Ссылка на материал или операцию.</td></tr><tr><td><code>qty DECIMAL(14,3) NOT NULL,</code></td><td>Плановое количество материала. Для операции 0.</td></tr><tr><td><code>time_norm DECIMAL(14,3) NOT NULL,</code></td><td>Плановые часы операции. Для материала 0.</td></tr><tr><td><code>PRIMARY KEY (production_id, item_id),</code></td><td>Первичный ключ делает строку узнаваемой и запрещает пустое значение.</td></tr><tr><td><code>KEY ix_prod_resource (item_id),</code></td><td>Обычный индекс ускоряет поиск по внешнему ключу.</td></tr><tr><td><code>CONSTRAINT ck_pr_qty CHECK (qty &gt;= 0),</code></td><td>Плановое количество не может быть отрицательным.</td></tr><tr><td><code>CONSTRAINT ck_pr_time CHECK (time_norm &gt;= 0)</code></td><td>Плановое время не может быть отрицательным.</td></tr></tbody></table>
<p><b>Полный скрипт для проверки</b></p>
<pre><code>CREATE TABLE production_resource (
  production_id INT NOT NULL,
  item_id INT NOT NULL,
  qty DECIMAL(14,3) NOT NULL,
  time_norm DECIMAL(14,3) NOT NULL,
  PRIMARY KEY (production_id, item_id),
  KEY ix_prod_resource (item_id),
  CONSTRAINT ck_pr_qty CHECK (qty &gt;= 0),
  CONSTRAINT ck_pr_time CHECK (time_norm &gt;= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="users">
<h4>11. <code>users</code></h4>
<p>Учётные записи приложения: логин, хеш пароля, роль и блокировка.</p>
<table class="schema-lines"><thead><tr><th>Строка</th><th>Что означает и почему</th></tr></thead><tbody><tr><td><code>id INT NOT NULL AUTO_INCREMENT,</code></td><td>Номер пользователя, AUTO_INCREMENT заполняет сервер.</td></tr><tr><td><code>login VARCHAR(64) NOT NULL,</code></td><td>Логин для входа. UNIQUE запрещает дубли.</td></tr><tr><td><code>password_hash VARCHAR(64) NOT NULL,</code></td><td>Хеш пароля, а не сам пароль.</td></tr><tr><td><code>salt VARCHAR(32) NOT NULL,</code></td><td>Соль для хеширования.</td></tr><tr><td><code>role ENUM(&#x27;admin&#x27;, &#x27;user&#x27;) NOT NULL DEFAULT &#x27;user&#x27;,</code></td><td>admin или user. ENUM не даёт записать другую роль.</td></tr><tr><td><code>failed_attempts INT NOT NULL DEFAULT 0,</code></td><td>Счётчик подряд ошибок входа.</td></tr><tr><td><code>is_locked TINYINT(1) NOT NULL DEFAULT 0,</code></td><td>Признак блокировки после третьей ошибки.</td></tr><tr><td><code>PRIMARY KEY (id),</code></td><td>Первичный ключ делает строку узнаваемой и запрещает пустое значение.</td></tr><tr><td><code>UNIQUE KEY uq_users_login (login)</code></td><td>Уникальный индекс не даёт двум строкам получить одинаковое значение.</td></tr></tbody></table>
<p><b>Полный скрипт для проверки</b></p>
<pre><code>CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT,
  login VARCHAR(64) NOT NULL,
  password_hash VARCHAR(64) NOT NULL,
  salt VARCHAR(32) NOT NULL,
  role ENUM(&#x27;admin&#x27;, &#x27;user&#x27;) NOT NULL DEFAULT &#x27;user&#x27;,
  failed_attempts INT NOT NULL DEFAULT 0,
  is_locked TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_users_login (login)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="notes">
<h4>12. <code>notes</code></h4>
<p>Заметки сотрудников. Автор хранится ссылкой на users.</p>
<table class="schema-lines"><thead><tr><th>Строка</th><th>Что означает и почему</th></tr></thead><tbody><tr><td><code>id INT NOT NULL AUTO_INCREMENT,</code></td><td>Номер заметки, AUTO_INCREMENT.</td></tr><tr><td><code>title VARCHAR(255) NOT NULL,</code></td><td>Заголовок заметки.</td></tr><tr><td><code>content TEXT NOT NULL,</code></td><td>Текст заметки.</td></tr><tr><td><code>id_user INT NOT NULL,</code></td><td>Ссылка на автора в users.</td></tr><tr><td><code>created_at DATE NOT NULL,</code></td><td>Дата создания заметки.</td></tr><tr><td><code>PRIMARY KEY (id),</code></td><td>Первичный ключ делает строку узнаваемой и запрещает пустое значение.</td></tr><tr><td><code>KEY ix_notes_user (id_user)</code></td><td>Обычный индекс ускоряет поиск по внешнему ключу.</td></tr></tbody></table>
<p><b>Полный скрипт для проверки</b></p>
<pre><code>CREATE TABLE notes (
  id INT NOT NULL AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  id_user INT NOT NULL,
  created_at DATE NOT NULL,
  PRIMARY KEY (id),
  KEY ix_notes_user (id_user)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
</div>
</div>

<figure class="diagram">
<img src="reports/screens/mysql/v02-tables.png" alt="Список таблиц базы dkip2027_v02">
<figcaption>Результат: в базе двенадцать таблиц. Внешние ключи добавляются на следующем шаге.</figcaption>
</figure>

### Связи между таблицами

Таблицы созданы без внешних ключей. Ниже все четырнадцать связей: выполняйте команды по одной после создания таблиц. Слайдер идёт в порядке зависимостей.

<details class="hint">
<summary>Шпаргалка: ALTER TABLE</summary>

```sql
ALTER TABLE дочерняя_таблица
  ADD CONSTRAINT имя_связи
  FOREIGN KEY (поле_дочерней)
  REFERENCES родительская_таблица (поле_родительской);
```

`ALTER TABLE` меняет готовую таблицу. `ADD CONSTRAINT` добавляет правило, `FOREIGN KEY` выбирает поле, `REFERENCES` указывает родительский ключ.

</details>

<div class="schema-slider" data-slider>
<div class="schema-slider-bar">
<strong>Все 14 связей: листайте стрелками</strong>
<div class="schema-slider-actions">
<button type="button" class="schema-btn" data-slider-prev aria-label="Предыдущая связь">←</button>
<span class="schema-slider-counter" data-slider-counter>1 / 14</span>
<button type="button" class="schema-btn" data-slider-next aria-label="Следующая связь">→</button>
</div>
</div>
<div class="schema-track" data-slider-track>
<article class="schema-slide" aria-label="price → item">
<h4>1. price → item</h4>
<p>Каждая цена ссылается на ресурс. Один ресурс может иметь несколько цен с разными датами.</p>
<pre><code>ALTER TABLE price
  ADD CONSTRAINT fk_price_item
  FOREIGN KEY (item_id)
  REFERENCES item (id);</code></pre>
</article>
<article class="schema-slide" aria-label="specification → item">
<h4>2. specification → item</h4>
<p>Спецификация описывает изделие. Ссылка ведёт на строку продукции в справочнике item.</p>
<pre><code>ALTER TABLE specification
  ADD CONSTRAINT fk_spec_product
  FOREIGN KEY (product_id)
  REFERENCES item (id);</code></pre>
</article>
<article class="schema-slide" aria-label="specification → counterparty">
<h4>3. specification → counterparty</h4>
<p>Изготовитель спецификации это контрагент с типом «Изготовитель».</p>
<pre><code>ALTER TABLE specification
  ADD CONSTRAINT fk_spec_maker
  FOREIGN KEY (manufacturer_id)
  REFERENCES counterparty (id);</code></pre>
</article>
<article class="schema-slide" aria-label="specification_component → specification">
<h4>4. specification_component → specification</h4>
<p>Строка состава принадлежит одной спецификации.</p>
<pre><code>ALTER TABLE specification_component
  ADD CONSTRAINT fk_comp_spec
  FOREIGN KEY (specification_id)
  REFERENCES specification (id);</code></pre>
</article>
<article class="schema-slide" aria-label="specification_component → item">
<h4>5. specification_component → item</h4>
<p>Строка состава ссылается на материал или операцию.</p>
<pre><code>ALTER TABLE specification_component
  ADD CONSTRAINT fk_comp_item
  FOREIGN KEY (item_id)
  REFERENCES item (id);</code></pre>
</article>
<article class="schema-slide" aria-label="customer_order → counterparty">
<h4>6. customer_order → counterparty</h4>
<p>Заказчик заказа это контрагент с типом «Покупатель».</p>
<pre><code>ALTER TABLE customer_order
  ADD CONSTRAINT fk_order_customer
  FOREIGN KEY (customer_id)
  REFERENCES counterparty (id);</code></pre>
</article>
<article class="schema-slide" aria-label="customer_order → counterparty">
<h4>7. customer_order → counterparty</h4>
<p>Исполнитель заказа это контрагент с типом «Изготовитель».</p>
<pre><code>ALTER TABLE customer_order
  ADD CONSTRAINT fk_order_executor
  FOREIGN KEY (executor_id)
  REFERENCES counterparty (id);</code></pre>
</article>
<article class="schema-slide" aria-label="customer_order_line → customer_order">
<h4>8. customer_order_line → customer_order</h4>
<p>Строка заказа принадлежит шапке заказа.</p>
<pre><code>ALTER TABLE customer_order_line
  ADD CONSTRAINT fk_line_order
  FOREIGN KEY (order_id)
  REFERENCES customer_order (id);</code></pre>
</article>
<article class="schema-slide" aria-label="customer_order_line → item">
<h4>9. customer_order_line → item</h4>
<p>Строка заказа ссылается на изделие из справочника.</p>
<pre><code>ALTER TABLE customer_order_line
  ADD CONSTRAINT fk_line_product
  FOREIGN KEY (product_id)
  REFERENCES item (id);</code></pre>
</article>
<article class="schema-slide" aria-label="production_product → production_order">
<h4>10. production_product → production_order</h4>
<p>Продукция к выпуску принадлежит производственному заказу.</p>
<pre><code>ALTER TABLE production_product
  ADD CONSTRAINT fk_pp_order
  FOREIGN KEY (production_id)
  REFERENCES production_order (id);</code></pre>
</article>
<article class="schema-slide" aria-label="production_product → item">
<h4>11. production_product → item</h4>
<p>Продукция к выпуску ссылается на изделие.</p>
<pre><code>ALTER TABLE production_product
  ADD CONSTRAINT fk_pp_item
  FOREIGN KEY (product_id)
  REFERENCES item (id);</code></pre>
</article>
<article class="schema-slide" aria-label="production_resource → production_order">
<h4>12. production_resource → production_order</h4>
<p>Плановый расход принадлежит производственному заказу.</p>
<pre><code>ALTER TABLE production_resource
  ADD CONSTRAINT fk_pr_order
  FOREIGN KEY (production_id)
  REFERENCES production_order (id);</code></pre>
</article>
<article class="schema-slide" aria-label="production_resource → item">
<h4>13. production_resource → item</h4>
<p>Плановый расход ссылается на материал или операцию.</p>
<pre><code>ALTER TABLE production_resource
  ADD CONSTRAINT fk_pr_item
  FOREIGN KEY (item_id)
  REFERENCES item (id);</code></pre>
</article>
<article class="schema-slide" aria-label="notes → users">
<h4>14. notes → users</h4>
<p>Заметка ссылается на автора в таблице пользователей.</p>
<pre><code>ALTER TABLE notes
  ADD CONSTRAINT fk_notes_user
  FOREIGN KEY (id_user)
  REFERENCES users (id);</code></pre>
</article>
</div>
</div>

### Вставка данных

Перед вставкой откройте шпаргалку.

<details class="hint">
<summary>Шпаргалка: INSERT</summary>

```sql
INSERT INTO имя_таблицы (поле1, поле2, поле3)
VALUES (значение1, значение2, значение3);
```

`INSERT INTO` выбирает таблицу. В скобках перечислены поля в порядке значений. `VALUES` начинает список. Текст и даты в пишут в кавычках, числа без кавычек. Строки разделяют запятыми, после последней запятой нет.

</details>

### Откуда берутся значения для INSERT

Перед вставкой сопоставьте поля файлов и таблиц. Значения не придумываются: каждое берётся из конкретного столбца исходного документа. Для каждой группы сначала показано, из какой ячейки берётся значение, затем код, затем источник и результат.

| Файл | Что берём | Таблица |
|---|---|---|
| `Заказчики.json` | `id`, `name`, `inn`, `addres`, `phone`, `type` | `counterparty` |
| `Заказ покупателя.xlsx` | номер, дата, срок, код заказчика, изделие, количество, цена, скидка | `customer_order`, `customer_order_line` |
| `Спецификация.xlsx` | материал, операция, единица, норма, часы | `item`, `specification`, `specification_component` |
| `Цены.xlsx` | ресурс, цена, дата | `price` |
| `Заказ на производство.xlsx` | заказ, дата запуска, изделие, плановый расход | `production_order`, `production_product`, `production_resource` |
| `Заметки.json` | заголовок, логин, текст, дата | `notes` |

В документах номера записаны как «№ 1». В базе к ним добавляется префикс варианта: заказ покупателя становится `V02-01`, производственный заказ `V02-P01`.

### Шаг 1. Загрузите заказчиков из JSON

<figure class="diagram">
<img src="reports/screens/mysql/json-source-v02.png" alt="Файл Заказчики.json варианта V02">
<figcaption>Источник: JSON с шестью заказчиками. Коды начинаются с `002`, ИНН может быть пустым.</figcaption>
</figure>

| Поле таблицы | Откуда значение | Почему |
|---|---|---|
| `id` | `id` из JSON | код хранится текстом, ведущие нули не теряются |
| `name` | `name` из JSON | название организации |
| `inn` | `inn` из JSON | пустая строка, если ИНН нет |
| `address` | `addres` из JSON | в таблице поле переименовано |
| `phone` | `phone` из JSON | контакт |
| `party_type` | `type` из JSON | роль контрагента |

```sql
INSERT INTO counterparty (id, name, inn, address, phone, party_type) VALUES
('002000001', 'Магазин «Колос-1»', '', 'Учебный город, улица Производственная, 2, офис 1', '+79990020001', 'Покупатель'),
('002000002', 'Торговый дом «Колос-2»', '', 'Учебный город, улица Производственная, 2, офис 2', '+79990020002', 'Покупатель'),
('002000003', 'Студия «Колос-3»', '', 'Учебный город, улица Производственная, 2, офис 3', '+79990020003', 'Покупатель'),
('002000004', 'Магазин подарков «Колос-4»', '', 'Учебный город, улица Производственная, 2, офис 4', '+79990020004', 'Покупатель'),
('002000005', 'Мастерская «Колос-5»', '', 'Учебный город, улица Производственная, 2, офис 5', '+79990020005', 'Покупатель'),
('002000006', 'Оптовый склад «Колос-6»', '', 'Учебный город, улица Производственная, 2, офис 6', '+79990020006', 'Покупатель');
```

Изготовитель в JSON отсутствует. В заказе он указан в блоке «Исполнитель», поэтому добавьте его отдельной строкой.

```sql
INSERT INTO counterparty (id, name, inn, address, phone, party_type) VALUES
('M-001', 'Пекарня «Колос»', '', 'Учебный город, улица Производственная, 2', '+79990020000', 'Изготовитель');
```

<figure class="diagram">
<img src="reports/screens/mysql/v02-customers.png" alt="Таблица counterparty после загрузки: заказчики и изготовитель">
<figcaption>Результат: шесть записей JSON и изготовитель. Коды `002000001`... сохранили ведущие нули.</figcaption>
</figure>

### Шаг 2. Загрузите изделия, цены, спецификацию, заказ и производство

#### Изделия и ресурсы

| Поле | Откуда значение | Почему |
|---|---|---|
| `id` | назначается по порядку | 1 изделие, 2-4 материалы, 5-6 операции |
| `code` | код из заказа и производства | код нужен для связи с документами |
| `name` | название из заказа, спецификации или цен | одинаковое имя во всех файлах |
| `kind` | по разделу файла | `product`, `material` или `operation` |
| `unit` | единица из спецификации или цен | ед., кг, шт, ч |

```sql
INSERT INTO item (id, code, name, kind, unit) VALUES
(1, 'P-01', 'Хлеб ржаной 500 г', 'product', 'ед.'),
(2, 'M-01', 'Мука ржаная', 'material', 'кг'),
(3, 'M-02', 'Закваска', 'material', 'кг'),
(4, 'M-03', 'Пакет', 'material', 'шт'),
(5, 'O-01', 'Замес и формование', 'operation', 'ч'),
(6, 'O-02', 'Выпечка', 'operation', 'ч');
```

<figure class="diagram">
<img src="reports/screens/prep/V02_order_xlsx.png" alt="Заказ покупателя V02: изделие, код и количество">
<figcaption>Из заказа берём изделие, код и количество. Название изделия становится строкой `product` в `item`.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/prep/V02_spec_xlsx.png" alt="Спецификация V02: материалы, операции и нормы">
<figcaption>Из спецификации берём названия материалов и операций, единицы и нормы. Каждая строка станет отдельным ресурсом в `item`.</figcaption>
</figure>

#### Цены

| Поле | Откуда значение | Почему |
|---|---|---|
| `item_id` | код ресурса из `item` | цена ссылается на ресурс, а не на название |
| `valid_from` | `2027-03-01` | дата из файла `Цены.xlsx` |
| `amount` | столбец «Цена» | цена за единицу ресурса |

```sql
INSERT INTO price (item_id, valid_from, amount) VALUES
(2, '2027-03-01', 65.00),
(3, '2027-03-01', 100.00),
(4, '2027-03-01', 4.00),
(5, '2027-03-01', 500.00),
(6, '2027-03-01', 700.00);
```

<figure class="diagram">
<img src="reports/screens/prep/V02_prices_xlsx.png" alt="Цены V02: ресурс, цена и дата">
<figcaption>Источник цен: название ресурса, цена и дата начала действия.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/mysql/v02-price.png" alt="Таблица price после вставки цен V02">
<figcaption>Результат: цены в `price`. У каждого ресурса своя строка и дата `2027-03-01`.</figcaption>
</figure>

#### Спецификация и состав

| Поле | Откуда значение | Почему |
|---|---|---|
| `specification.id` | 1 | в варианте одна спецификация |
| `specification.product_id` | 1 | ссылка на изделие |
| `specification.name` | шапка «Изделие» | название изделия |
| `specification.output_qty` | 1 | нормы даны на одну буханку |
| `specification.manufacturer_id` | `M-001` | изготовитель из шапки |
| `specification_component.qty` | «Норма расхода» | норма материала |
| `specification_component.time_norm` | «Норма времени» | часы операции |

```sql
INSERT INTO specification (id, product_id, name, output_qty, manufacturer_id)
VALUES (1, 1, 'Хлеб ржаной 500 г', 1.000, 'M-001');

INSERT INTO specification_component (specification_id, item_id, qty, time_norm) VALUES
(1, 2, 0.320, 0.000),
(1, 3, 0.080, 0.000),
(1, 4, 1.000, 0.000),
(1, 5, 0.000, 0.040),
(1, 6, 0.000, 0.020);
```

Для материалов `qty` это норма на единицу, `time_norm` равно нулю. Для операций `qty` равно нулю, `time_norm` хранит часы.

<figure class="diagram">
<img src="reports/screens/mysql/v02-spec.png" alt="Состав спецификации V02: материалы и операции с нормами">
<figcaption>Результат: пять строк состава. У материалов заполнена норма, у операций время.</figcaption>
</figure>

#### Заказ и строка заказа

| Поле | Откуда значение | Почему |
|---|---|---|
| `customer_order.doc_no` | номер заказа | `V02-01` |
| `customer_order.doc_date` | дата заказа | `15.03.2027` |
| `customer_order.customer_id` | код заказчика | `002000001` |
| `customer_order.executor_id` | код изготовителя | `M-001` |
| `customer_order_line.product_id` | изделие | `1` |
| `customer_order_line.qty` | «Кол-во» | 40 |
| `customer_order_line.sale_price` | «Цена» | 700,00 |
| `customer_order_line.discount` | «Скидка» | 0,00 |

```sql
INSERT INTO customer_order (id, doc_no, doc_date, customer_id, executor_id)
VALUES (1, 'V02-01', '2027-03-15', '002000001', 'M-001');

INSERT INTO customer_order_line (id, order_id, product_id, qty, sale_price, discount)
VALUES (1, 1, 1, 40, 700.00, 0.00);
```

<figure class="diagram">
<img src="reports/screens/prep/V02_order_xlsx.png" alt="Заказ покупателя V02: шапка и строка продукции">
<figcaption>Источник: номер, дата, заказчик, изделие, количество и цена. Из шапки получается `customer_order`, из строки продукции `customer_order_line`.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/mysql/v02-order.png" alt="Заказ V02-01 в таблице customer_order">
<figcaption>Результат: шапка заказа V02-01. Дата 15.03.2027, заказчик 002000001, исполнитель M-001.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/mysql/v02-lines.png" alt="Строка заказа V02 в таблице customer_order_line">
<figcaption>Результат: строка заказа. Количество 40, цена 700,00, скидка 0,00.</figcaption>
</figure>

#### Производственный заказ

| Поле | Откуда значение | Почему |
|---|---|---|
| `production_order.doc_no` | номер производственного заказа | `V02-P01` |
| `production_order.doc_date` | дата заказа покупателя | `15.03.2027` |
| `production_order.launch_date` | «Дата запуска» | `16.03.2027` |
| `production_order.department` | «Подразделение» | основное производство |
| `production_product.qty` | «Продукция к выпуску» | 40 |
| `production_resource.qty` | «Потребность в материалах» | плановый расход |
| `production_resource.time_norm` | «Технологические операции» | плановые часы |

```sql
INSERT INTO production_order (id, doc_no, doc_date, launch_date, department)
VALUES (1, 'V02-P01', '2027-03-15', '2027-03-16', 'Основное производство');

INSERT INTO production_product (production_id, product_id, qty)
VALUES (1, 1, 40);

INSERT INTO production_resource (production_id, item_id, qty, time_norm) VALUES
(1, 2, 12.800, 0.000),
(1, 3, 3.200, 0.000),
(1, 4, 40.000, 0.000),
(1, 5, 0.000, 1.600),
(1, 6, 0.000, 0.800);
```

<figure class="diagram">
<img src="reports/screens/prep/V02_production_xlsx.png" alt="Заказ на производство V02: продукция, материалы и операции">
<figcaption>Источник: изделие, потребность в материалах и технологические операции. Каждая строка становится строкой `production_resource`.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/mysql/v02-production.png" alt="Шапка производственного заказа V02">
<figcaption>Результат: производственный заказ V02-P01. Дата запуска и подразделение перенесены из Excel.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/mysql/v02-production-product.png" alt="Продукция к выпуску V02">
<figcaption>Результат: в производственном заказе 40 единиц изделия. Количество взято из строки «Продукция к выпуску».</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/mysql/v02-production-resource.png" alt="Плановый расход ресурсов V02">
<figcaption>Результат: пять строк планового расхода. Материалы и операции хранятся в одной таблице.</figcaption>
</figure>

### Шаг 3. Проверьте данные

```sql
SELECT COUNT(*) AS customers FROM counterparty;
SELECT COUNT(*) AS items FROM item;
SELECT COUNT(*) AS components FROM specification_component;
SELECT COUNT(*) AS orders FROM customer_order;
SELECT COUNT(*) AS production_rows FROM production_resource;
```

Ожидается семь контрагентов, шесть ресурсов, пять строк состава, один заказ и пять строк производственного расхода.

Попробуйте вставить заказ с несуществующим заказчиком:

```sql
INSERT INTO customer_order (id, doc_no, doc_date, customer_id, executor_id)
VALUES (99, 'TEST-1', '2027-03-20', 'NO-SUCH', 'M-001');
```

Сервер должен ответить ошибкой 1452. Это доказывает, что внешний ключ работает.


## Задание 3. SQL-запрос стоимости

Соберите запрос по тем же правилам, что и в V01. Материалы: количество выпуска × норма × цена. Операции: количество выпуска × часы × тариф за час. Цены действуют с 01.03.2027.

```sql
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
```

<figure class="diagram">
<img src="reports/screens/mysql/v02-total.png" alt="Итоговая стоимость заказа V02-01: 2672.00">
<figcaption>Итог запроса: номер заказа и нормативная стоимость 2 672,00.</figcaption>
</figure>

Проверьте строки расчёта:

```sql
SELECT
  i.name,
  i.kind,
  c.qty,
  c.time_norm,
  p.amount,
  ROUND(l.qty / s.output_qty
    * CASE WHEN i.kind = 'operation' THEN c.time_norm ELSE c.qty END
    * p.amount, 2) AS line_cost
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
ORDER BY i.kind, i.id;
```

<figure class="diagram">
<img src="reports/screens/mysql/v02-detail.png" alt="Пять строк расчёта стоимости V02">
<figcaption>Строки расчёта: три материала и две операции. Сумма равна 2 672,00.</figcaption>
</figure>

Материалы дают `1312.00`, операции `1360.00`, вместе `2672.00`. Если получилось другое число, проверьте пять строк состава и цену на дату `2027-03-15`, а не подгоняйте запрос.

Проверьте, что соединение не удвоило строки:

```sql
SELECT
  (SELECT COUNT(*) FROM specification s
   JOIN specification_component c ON c.specification_id = s.id
   WHERE s.product_id = 1) AS components,
  (SELECT COUNT(*) FROM customer_order o
   JOIN customer_order_line l ON l.order_id = o.id
   JOIN specification s ON s.product_id = l.product_id
   JOIN specification_component c ON c.specification_id = s.id
   JOIN price p ON p.item_id = c.item_id
     AND p.valid_from = (SELECT MAX(p2.valid_from) FROM price p2
                         WHERE p2.item_id = c.item_id AND p2.valid_from <= o.doc_date)
   WHERE o.doc_no = 'V02-01') AS joined_rows;
```

<figure class="diagram">
<img src="reports/screens/mysql/v02-count.png" alt="Проверка числа строк V02: 5 и 5">
<figcaption>Проверка: в составе 5 строк и после соединения тоже 5.</figcaption>
</figure>

## Файлы решения V02

| Файл | Что внутри |
|---|---|
| `V02_schema.sql` | двенадцать таблиц, `PRIMARY KEY` и `CHECK`, без внешних ключей |
| `V02_fk.sql` | четырнадцать связей через `ALTER TABLE` |
| `V02_import.sql` | заказчики, ресурсы, спецификация, цены и производственный заказ |
| `V02_cost.sql` | запрос стоимости и результат `2672.00` |

## Чек-лист V02

- База `dkip2027_v02` создана в `utf8mb4`.
- Все двенадцать таблиц используют `InnoDB`.
- Внешние ключи добавлены после создания таблиц.
- Шесть записей JSON и изготовитель загружены.
- Изделие, материалы, операции, цены, спецификация и заказ загружены.
- Производственный заказ и плановый расход загружены.
- Итог задания 3 равен `2672.00`.
- Скриншоты показывают источник, код и результат.
