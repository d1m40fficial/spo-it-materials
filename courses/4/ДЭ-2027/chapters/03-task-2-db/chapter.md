---
title: Задание 2. База данных и импорт
dek: Создаём базу в XAMPP, таблицы и связи запросами, загружаем заказчиков из JSON и документы из Excel.
chapter: "Задание 2"
level: СПО
glyph: "03"
outcomes:
  - Создавать базу и таблицы запросами CREATE TABLE
  - Объяснять структуру CREATE TABLE, типы и ограничения
  - Строить связи через ALTER TABLE и проверять внешние ключи
  - Загружать заказчиков из JSON и документы из Excel
---

## Что требуется

Создать работающую базу данных предприятия по своей ER-диаграмме и загрузить в неё данные из документов варианта. База называется `dkip2027_course` и создаётся в кодировке `utf8mb4`. В ней должны быть таблицы, первичные и внешние ключи, обязательные поля и проверки значений.

В базу загружаются:

- шесть заказчиков из `Заказчики.json`;
- ИП Томилин из заказа покупателя, потому что в JSON его нет;
- изготовитель ООО ТД «Вершина» отдельной строкой;
- заказ покупателя, спецификация, состав спецификации и цены из книг Excel;
- производственный заказ, продукция к выпуску и плановый расход ресурсов;
- при необходимости пользователи и заметки, если они есть в вашей модели.

После загрузки нужно проверить, что коды заказчиков сохранили ведущие нули, что внешние ключи не пропускают несуществующие ссылки и что количество строк совпадает с документами. Затем база выгружается в SQL-файл и восстанавливается в пустую базу.

Сдаются SQL-скрипт схемы, файл выгрузки `dkip2027-mysql.sql` и протокол проверок со скриншотами: действие, команда, ожидаемый и фактический результат.

База должна открываться на другом компьютере после восстановления.

## Что понадобится

| Что открыть | Где найти | Зачем |
|---|---|---|
| XAMPP Control Panel | `Пуск`, затем `XAMPP Control Panel` | запуск Apache и MySQL |
| Браузер | ярлык на рабочем столе | phpMyAdmin |
| phpMyAdmin | `http://localhost:4433/phpmyadmin` | создание базы, таблиц, связей и экспорт |
| Архив варианта | `reports/variants/V01/V01_исходные_данные.zip` | все исходные файлы одним архивом |
| `Заказчики.json` | архив варианта | шесть заказчиков |
| Заказ покупателя.xlsx | архив варианта | номер, дата, заказчик, изделие и количество |
| Спецификация.xlsx | там же | материалы, операции и нормы |
| Цены.xlsx | там же | цены ресурсов |
| Заказ на производство.xlsx | там же | производственный заказ и плановый расход |
| Расчет стоимости.xlsx | там же | таблица для ручной проверки |
| Excel | `Пуск` | просмотр документов |
| Блокнот или VS Code | `Пуск` | просмотр JSON и SQL-файла |
| ER-диаграмма из задания 1 | папка `task1` | имена таблиц и полей |
| Папка `task2` | ваша рабочая папка | схема, выгрузка, протокол |

Права администратора Windows не нужны.

Скачать все исходные файлы: [V01_исходные_данные.zip](reports/variants/V01/V01_исходные_данные.zip).

В `Заказчики.json` шесть записей. Код записан строкой, поэтому ведущие нули не теряются. Ключ адреса в исходном файле называется `addres`, при переносе в таблицу он становится `address`. JSON не импортируется в phpMyAdmin отдельной кнопкой: значения переносят в `INSERT` или вставляют через форму. Это нормальный экзаменационный путь, потому что показывает, что вы понимаете структуру данных.

## Как устроено задание

MySQL это отдельная служба. Она слушает порт 3306 и хранит данные в своих файлах. phpMyAdmin это веб-приложение, которое открывается в браузере и передаёт команды серверу. Ему нужен Apache, потому что PHP выполняется веб-сервером. Поэтому в XAMPP запускают обе службы: Apache для phpMyAdmin, MySQL для данных.

Если Apache остановлен, phpMyAdmin не откроется, хотя база продолжит работать. Если MySQL остановлен, phpMyAdmin покажет ошибку подключения.

Кодировка задаётся у базы, таблиц и соединения. `utf8mb4` хранит до четырёх байт на символ и вмещает кириллицу, редкие знаки и эмодзи. Старое имя `utf8` в MySQL ограничено тремя байтами. Сравнение `utf8mb4_unicode_ci` не различает регистр и правильно сортирует кириллицу. Главное, чтобы кодировка была одинаковой у базы, таблиц и клиента.

Схема задания повторяет ER-диаграмму. В базовом наборе двенадцать таблиц, для задания 2 достаточно семи основных.

| Таблица | Первичный ключ | Внешние ключи | Что хранит |
|---|---|---|---|
| `counterparty` | `id` | нет | заказчиков, изготовителей, поставщиков |
| `item` | `id` | нет | продукцию, материалы и операции |
| `price` | `item_id`, `valid_from` | `item_id` | историю цен ресурса |
| `specification` | `id` | `product_id`, `manufacturer_id` | шапку спецификации |
| `specification_component` | `specification_id`, `item_id` | `specification_id`, `item_id` | нормы расхода и времени |
| `customer_order` | `id` | `customer_id`, `executor_id` | шапку заказа покупателя |
| `customer_order_line` | `id` | `order_id`, `product_id` | строки заказа |
| `production_order` | `id` | нет | шапку производственного заказа |
| `production_product` | `production_id`, `product_id` | `production_id`, `product_id` | продукцию к выпуску |
| `production_resource` | `production_id`, `item_id` | `production_id`, `item_id` | плановый расход ресурсов |
| `users` | `id` | нет | учётные записи приложения |
| `notes` | `id` | `id_user` | заметки сотрудников |

**Контрагент** это организация или предприниматель, с которым предприятие оформляет деловые отношения: заказчик, поставщик, изготовитель. В базе все роли сведены в одну таблицу `counterparty`, а конкретная роль хранится в поле `party_type`. Поэтому заказчик и изготовитель не дублируются, а заказ ссылается на один и тот же справочник двумя полями: `customer_id` и `executor_id`.

Ограничение это правило, которое сервер проверяет до записи. Основные виды перечислены в таблице.

| Ограничение | Что запрещает | Пример |
|---|---|---|
| `PRIMARY KEY` | повтор ключа и пустое значение | `id` различает строки |
| `FOREIGN KEY` | ссылку на отсутствующую строку | строка заказа ссылается на заказ |
| `NOT NULL` | пустое значение | имя заказчика обязательно |
| `UNIQUE` | повтор значения | код ресурса не повторяется |
| `CHECK` | значение вне диапазона | количество больше нуля |
| `DEFAULT` | отсутствие значения | дата создания по умолчанию |

Тип выбирают по смыслу. Деньги хранят в `DECIMAL(14,2)`, количество и нормы времени в `DECIMAL(14,3)`. `FLOAT` и `DOUBLE` хранят двоичную дробь, поэтому 0,1 в них не равно 0,1, и сумма из сотни строк может разойтись с ручным расчётом.

Коды заказчиков, ИНН и телефоны хранят текстом. В JSON код выглядит как `000000001`. Если объявить столбец целым, ведущие нули исчезнут: `000000001` станет `1`. Если объявить `VARCHAR(32)`, код сохранится символ в символ. Текстовыми также делают ИНН и телефон: ИНН может начинаться с нуля, телефон содержит плюс, а арифметика над ними не нужна.

JSON это текстовый формат: объект в фигурных скобках, массив в квадратных, поля разделены запятыми. Для переноса в базу важен не сам формат, а соответствие имён: `addres` из источника становится `address` в таблице, `type` становится `party_type`. Значения дат и чисел перед вставкой приводят к типам столбцов.

Excel хранит данные по ячейкам. При переносе в базу важны заголовки табличной части, а не оформление листа. Заголовок книги, объединённые ячейки и пустые строки пропускаются: в `INSERT` попадают только столбцы и строки таблицы.

### Как читать файлы Excel

Документы варианта оформлены как бумажные формы: заголовок, блок реквизитов и табличная часть с сеткой. Сетка не украшение: по ней видно, где заканчивается шапка и начинаются строки.

<figure class="diagram">
<img src="reports/screens/prep/V01_order_xlsx.png" alt="Заказ покупателя V01: заголовок, реквизиты и таблица продукции">
<figcaption>Заказ покупателя: заголовок, номер, дата, срок, заказчик и таблица продукции.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/prep/V01_spec_xlsx.png" alt="Спецификация V01: нормы материалов и часы операций">
<figcaption>Спецификация: шапка изделия, затем таблица состава с нормами и часами.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/prep/V01_prices_xlsx.png" alt="Цены V01: ресурс и цена">
<figcaption>Цены: у каждого ресурса указана цена. Дата начала действия задана условием варианта.</figcaption>
</figure>

## Пошаговая инструкция

Перед первым запросом откройте общую шпаргалку. В ней три команды, которые понадобятся дальше.

<details class="hint">
<summary>Шпаргалка: CREATE TABLE, ALTER TABLE и INSERT</summary>

**Создание таблицы**

```sql
CREATE TABLE имя_таблицы (
  имя_поля ТИП ОГРАНИЧЕНИЕ,
  имя_поля ТИП ОГРАНИЧЕНИЕ,
  PRIMARY KEY (имя_поля),
  CONSTRAINT имя_правила FOREIGN KEY (имя_поля)
    REFERENCES родительская_таблица (имя_поля)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

`CREATE TABLE` создаёт таблицу. В скобках перечисляются поля, затем ключи и проверки. Каждое поле описывается тремя частями: имя, тип и ограничение. Запятая разделяет описания, после последнего запятая не ставится.

**Добавление связи**

```sql
ALTER TABLE дочерняя_таблица
  ADD CONSTRAINT имя_связи
  FOREIGN KEY (поле_дочерней)
  REFERENCES родительская_таблица (поле_родительской);
```

`ALTER TABLE` меняет уже созданную таблицу. `ADD CONSTRAINT` добавляет правило с именем. `FOREIGN KEY` называет поле текущей таблицы. `REFERENCES` указывает родительскую таблицу и её ключ.

**Вставка строк**

```sql
INSERT INTO имя_таблицы (поле1, поле2, поле3)
VALUES (значение1, значение2, значение3);
```

`INSERT INTO` выбирает таблицу. В скобках перечислены поля в том порядке, в котором пойдут значения. `VALUES` начинает список значений. Текст и даты пишут в кавычках, числа без кавычек. Несколько строк разделяют запятыми, после последней строки запятая не ставится.

</details>

### Шаг 1. Запустите Apache и MySQL

Откройте `Пуск`, найдите `XAMPP Control Panel` и запустите его. В окне список служб, нам нужны `Apache` и `MySQL`. Нажмите кнопку `Start` в строке `Apache`. Через несколько секунд строка станет зелёной, в колонке `Status` появится `Running`. Затем нажмите `Start` в строке `MySQL`. Она тоже должна стать зелёной.

<figure class="diagram">
<img src="reports/screens/mysql/db-start.png" alt="XAMPP Control Panel с запущенными Apache и MySQL">
<figcaption>XAMPP Control Panel: Apache и MySQL в состоянии Running, MySQL слушает порт 3306.</figcaption>
</figure>

На учебных компьютерах Apache уже переведён на порт 4433, поэтому дальше открывайте phpMyAdmin по адресу с этим портом.

### Шаг 2. Откройте phpMyAdmin

Откройте браузер и перейдите по адресу `http://localhost:4433/phpmyadmin`. Появится страница входа. В поле `Пользователь` введите `root`, поле `Пароль` оставьте пустым, нажмите `Войти`.

После входа откроется главная страница: слева список баз, сверху вкладки `Обзор`, `Структура`, `SQL`, `Импорт`, `Экспорт`, справа основная область.

### Шаг 3. Создайте базу dkip2027_course

В левой панели нажмите `Создать БД`. В поле `Имя базы данных` введите `dkip2027_course`. В списке `Сравнение` выберите `utf8mb4_unicode_ci`. Нажмите `Создать`.

<figure class="diagram">
<img src="reports/screens/mysql/t2-create.png" alt="Создание базы dkip2027_course в phpMyAdmin: форма и новая строка в списке">
<figcaption>Создание базы: имя dkip2027_course и сравнение utf8mb4_unicode_ci.</figcaption>
</figure>

Слева появится новая база, она сразу откроется. В основной области будет написано, что таблиц пока нет.

```sql
CREATE DATABASE dkip2027_course
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

### Шаг 4. Разберите структуру CREATE TABLE

Все таблицы создаются запросами. Разберём команду по частям на таблице `counterparty`.

```sql
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
```

Читайте запрос сверху вниз:

1. `CREATE TABLE counterparty` означает «создай таблицу с именем counterparty». Имя пишут латиницей, цифрами и знаком подчёркивания. Пробелы и дефисы не используйте. Слово `order` в MySQL зарезервировано, поэтому таблица заказа называется `customer_order`.
2. Открывающая скобка `(` начинает список полей. Закрывающая `)` завершает его. Между ними перечислены поля, ключи и проверки.
3. `id VARCHAR(32) NOT NULL` это поле `id`. `VARCHAR(32)` хранит строку до 32 символов. `NOT NULL` запрещает пустое значение. Код заказчика хранят текстом, иначе ведущие нули исчезнут.
4. `inn VARCHAR(20) NOT NULL DEFAULT ''` означает, что ИНН обязателен, но если его не передали, подставится пустая строка.
5. `PRIMARY KEY (id)` объявляет поле `id` первичным ключом. Первичный ключ уникален, не может быть пустым и ускоряет поиск.
6. `CONSTRAINT ck_party_type` даёт проверке имя. Имя нужно, чтобы в сообщении об ошибке было видно, какое правило сработало.
7. `CHECK (party_type IN (...))` пропускает только три допустимых значения. Это защита от опечаток вроде «Покупател».
8. `ENGINE=InnoDB` выбирает движок. Только InnoDB поддерживает транзакции и внешние ключи.
9. `DEFAULT CHARSET=utf8mb4` задаёт кодировку таблицы.

Типы, которые нужны в этом задании:

| Тип | Что хранит | Пример |
|---|---|---|
| `INT` | целое число | `id`, количество штук |
| `VARCHAR` | строку до n символов | `name`, `code`, `phone` |
| `DECIMAL` | точное число с дробью | `amount`, `qty` |
| `DATE` | дату без времени | `valid_from`, `doc_date` |
| `TEXT` | длинный текст | заметка, комментарий |

`INT AUTO_INCREMENT` это целое, которое сервер заполняет сам. `VARCHAR(64)` считает символы. `DECIMAL(14,2)` хранит 14 цифр, из них 2 после запятой. Деньги считают только в `DECIMAL`. `DATE` принимает значение в формате `2026-04-22`.

Ограничения:

| Ограничение | Что проверяет | Пример |
|---|---|---|
| `NOT NULL` | значение обязательно | `name VARCHAR(255) NOT NULL` |
| `UNIQUE` | значение не повторяется | `code VARCHAR(64) UNIQUE` |
| `DEFAULT` | значение по умолчанию | `created_at DATE DEFAULT (CURRENT_DATE)` |
| `CHECK` | значение попадает в диапазон | `CHECK (amount >= 0)` |
| `PRIMARY KEY` | строку можно отличить | `PRIMARY KEY (id)` |
| `FOREIGN KEY` | ссылка ведёт на существующую строку | `REFERENCES item(id)` |

Первичный ключ делает строку узнаваемой. Он одновременно означает `NOT NULL`, `UNIQUE` и индекс для поиска. У таблицы может быть только один первичный ключ.

Простой ключ это одно поле. Естественный ключ берут из документа, если он уникален и не меняется: у контрагента это код. Составной ключ состоит из двух полей: у цены это ресурс и дата, у состава это спецификация и ресурс.

Внешний ключ связывает строку с первичным ключом другой таблицы. Разберём объявление:

```sql
CONSTRAINT fk_price_item
  FOREIGN KEY (item_id)
  REFERENCES item(id)
```

`CONSTRAINT fk_price_item` задаёт имя правила. `FOREIGN KEY (item_id)` называет поле текущей таблицы. `REFERENCES item(id)` говорит, что значение должно найтись в поле `id` таблицы `item`.

Работают четыре требования. Тип ссылающегося поля совпадает с типом целевого. Целевое поле является первичным или уникальным ключом. Обе таблицы используют InnoDB. Родительская таблица уже создана. Если цена объявлена раньше ресурса, сервер ответит ошибкой 1215.

Связь многие ко многим раскладывают на связывающую таблицу. В модели это `specification_component`: одна спецификация содержит много ресурсов, один ресурс входит в много спецификаций. Пара `specification_id` и `item_id` объявлена первичным ключом, поэтому один ресурс не попадёт в спецификацию дважды.

<figure class="diagram">
<img src="reports/screens/mysql/t2-create-counterparty-sql.png" alt="Создание таблицы counterparty запросом в phpMyAdmin">
<figcaption>Создание таблицы запросом: вкладка SQL, команда `CREATE TABLE counterparty` и кнопка «Вперёд».</figcaption>
</figure>

### Шаг 5. Создайте все таблицы

Создайте таблицы в порядке зависимостей: сначала `counterparty` и `item`, затем `price`, `specification`, `specification_component`, потом `customer_order` и `customer_order_line`, затем `production_order`, `production_product`, `production_resource`, `users`, `notes`. Таблица не может ссылаться на ещё не созданную родительскую.

Ниже два слайдера. Первый показывает, откуда взялась каждая таблица, второй разбирает её создание построчно. В конце второго слайдера есть полный скрипт для проверки.

<p>Первый слайдер показывает, откуда взялась каждая таблица: какой файл или документ её породил, какие поля в неё попадают и почему.</p>

<div class="schema-slider" data-slider>
<div class="schema-slider-bar">
<strong>Откуда берутся таблицы: V01, 12 слайдов</strong>
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
<p><b>Откуда берём:</b> Заказчики.json: шесть записей. Заказ покупателя.xlsx: блоки «Заказчик» и «Исполнитель». Для V01 добавляются ИП Томилин и ООО ТД «Вершина», для V02 изготовитель Пекарня «Колос».</p>
<table class="schema-lines"><thead><tr><th>Поле</th><th>Откуда значение и почему</th></tr></thead><tbody><tr><td><code>id</code></td><td>JSON id; для ИП Томилина 000000004, для изготовителя M-001.</td></tr><tr><td><code>name</code></td><td>JSON name; из заказа название заказчика и исполнителя.</td></tr><tr><td><code>inn</code></td><td>JSON inn; пустая строка, если ИНН нет.</td></tr><tr><td><code>address</code></td><td>JSON addres; в таблице address.</td></tr><tr><td><code>phone</code></td><td>JSON phone.</td></tr><tr><td><code>party_type</code></td><td>JSON type: Покупатель, Поставщик или Изготовитель.</td></tr></tbody></table>
</article>
<article class="schema-slide" aria-label="item">
<h4>2. <code>item</code></h4>
<p>Один справочник ресурсов: продукция, материалы и операции. Поле kind говорит, как ресурс участвует в расчёте.</p>
<p><b>Откуда берём:</b> Заказ покупателя.xlsx: строка продукции. Спецификация.xlsx и Цены.xlsx: материалы, операции, единицы. Заказ на производство.xlsx: коды и плановые наименования.</p>
<table class="schema-lines"><thead><tr><th>Поле</th><th>Откуда значение и почему</th></tr></thead><tbody><tr><td><code>id</code></td><td>Номер по порядку: 1 продукция, далее материалы и операции.</td></tr><tr><td><code>code</code></td><td>Код из заказа и производственного заказа: P-01/ФР-00000034.</td></tr><tr><td><code>name</code></td><td>Название из строки продукции и таблиц спецификации.</td></tr><tr><td><code>kind</code></td><td>product для изделия, material для материалов, operation для операций.</td></tr><tr><td><code>unit</code></td><td>Единица из спецификации и цен.</td></tr></tbody></table>
</article>
<article class="schema-slide" aria-label="price">
<h4>3. <code>price</code></h4>
<p>История цен. Цена не хранится в item, потому что со временем меняется.</p>
<p><b>Откуда берём:</b> Цены.xlsx: столбцы «Номенклатура» и «Цена». Дата начала действия задана условием варианта.</p>
<table class="schema-lines"><thead><tr><th>Поле</th><th>Откуда значение и почему</th></tr></thead><tbody><tr><td><code>item_id</code></td><td>Код ресурса из item, а не название. Название может измениться.</td></tr><tr><td><code>valid_from</code></td><td>2026-04-01 для V01.</td></tr><tr><td><code>amount</code></td><td>Цена из строки ресурса в Цены.xlsx.</td></tr></tbody></table>
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
<table class="schema-lines"><thead><tr><th>Поле</th><th>Откуда значение и почему</th></tr></thead><tbody><tr><td><code>id</code></td><td>1, внутренний номер.</td></tr><tr><td><code>doc_no</code></td><td>V01-01.</td></tr><tr><td><code>doc_date</code></td><td>22.04.2026.</td></tr><tr><td><code>customer_id</code></td><td>000000004, ИП Томилин.</td></tr><tr><td><code>executor_id</code></td><td>M-001, ООО ТД «Вершина».</td></tr></tbody></table>
</article>
<article class="schema-slide" aria-label="customer_order_line">
<h4>7. <code>customer_order_line</code></h4>
<p>Строки заказа: какое изделие, сколько, по какой продажной цене и со скидкой.</p>
<p><b>Откуда берём:</b> Заказ покупателя.xlsx: строка «Товары (работы, услуги)».</p>
<table class="schema-lines"><thead><tr><th>Поле</th><th>Откуда значение и почему</th></tr></thead><tbody><tr><td><code>id</code></td><td>1, одна строка заказа.</td></tr><tr><td><code>order_id</code></td><td>1, ссылка на шапку.</td></tr><tr><td><code>product_id</code></td><td>1, ссылка на изделие.</td></tr><tr><td><code>qty</code></td><td>2.</td></tr><tr><td><code>sale_price</code></td><td>14120.00.</td></tr><tr><td><code>discount</code></td><td>1412.00.</td></tr></tbody></table>
</article>
<article class="schema-slide" aria-label="production_order">
<h4>8. <code>production_order</code></h4>
<p>Шапка производственного заказа: номер, дата, дата запуска и подразделение.</p>
<p><b>Откуда берём:</b> Заказ на производство.xlsx: шапка.</p>
<table class="schema-lines"><thead><tr><th>Поле</th><th>Откуда значение и почему</th></tr></thead><tbody><tr><td><code>id</code></td><td>1, внутренний номер.</td></tr><tr><td><code>doc_no</code></td><td>V01-P-01.</td></tr><tr><td><code>doc_date</code></td><td>22.04.2026, дата заказа.</td></tr><tr><td><code>launch_date</code></td><td>23.04.2026.</td></tr><tr><td><code>department</code></td><td>Основное подразделение.</td></tr></tbody></table>
</article>
<article class="schema-slide" aria-label="production_product">
<h4>9. <code>production_product</code></h4>
<p>Что выпускаем по производственному заказу и в каком количестве.</p>
<p><b>Откуда берём:</b> Заказ на производство.xlsx: «Продукция к выпуску».</p>
<table class="schema-lines"><thead><tr><th>Поле</th><th>Откуда значение и почему</th></tr></thead><tbody><tr><td><code>production_id</code></td><td>1, ссылка на производственный заказ.</td></tr><tr><td><code>product_id</code></td><td>1, ссылка на изделие.</td></tr><tr><td><code>qty</code></td><td>2.</td></tr></tbody></table>
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

<p>Второй слайдер разбирает создание таблиц построчно. В конце каждого слайда есть полный скрипт для проверки.</p>

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

После выполнения запросов откройте вкладку `Структура` базы. В списке должно быть двенадцать таблиц.

<figure class="diagram">
<img src="reports/screens/mysql/t2-tables.png" alt="Список таблиц базы dkip2027_course после выполнения CREATE TABLE">
<figcaption>Результат: в базе двенадцать таблиц. Проверьте список перед добавлением связей и данных.</figcaption>
</figure>

### Шаг 6. Постройте связи запросами

Связи добавляются командой `ALTER TABLE`. Перед первым запросом откройте шпаргалку.

<details class="hint">
<summary>Шпаргалка: ALTER TABLE и внешний ключ</summary>

```sql
ALTER TABLE дочерняя_таблица
  ADD CONSTRAINT имя_связи
  FOREIGN KEY (поле_дочерней)
  REFERENCES родительская_таблица (поле_родительской);
```

`ALTER TABLE` меняет уже созданную таблицу. `ADD CONSTRAINT` добавляет правило с именем. `FOREIGN KEY` называет поле текущей таблицы. `REFERENCES` указывает родительскую таблицу и её ключ.

</details>

```sql
ALTER TABLE customer_order
  ADD CONSTRAINT fk_order_customer
  FOREIGN KEY (customer_id) REFERENCES counterparty(id),
  ADD CONSTRAINT fk_order_executor
  FOREIGN KEY (executor_id) REFERENCES counterparty(id);
```

<figure class="diagram">
<img src="reports/screens/mysql/t2-alter-sql.png" alt="Добавление внешних ключей запросом ALTER TABLE в phpMyAdmin">
<figcaption>Связи запросом: два внешних ключа заказа добавляются одной командой `ALTER TABLE`.</figcaption>
</figure>

Таблицы созданы без внешних ключей. Ниже все четырнадцать связей: выполняйте команды по одной после создания таблиц. Слайдер идёт в порядке зависимостей, поэтому родительская таблица уже существует к моменту добавления связи.

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

После добавления связей проверьте их запросом:

```sql
SELECT table_name, constraint_name, referenced_table_name
FROM information_schema.KEY_COLUMN_USAGE
WHERE table_schema = 'dkip2027_course'
  AND referenced_table_name IS NOT NULL
ORDER BY table_name, constraint_name;
```

### Откуда берутся значения для INSERT

Перед вставкой сопоставьте поля файлов и таблиц. Значения не придумываются: каждое берётся из конкретного столбца исходного документа. Для каждой группы сначала показано, из какой ячейки берётся значение, затем код, затем источник и результат.

| Файл | Что берём | Таблица |
|---|---|---|
| `Заказчики.json` | `id`, `name`, `inn`, `addres`, `phone`, `type` | `counterparty` |
| `Заказ покупателя.xlsx` | номер, дата, срок, код заказчика, изделие, количество, цена, скидка | `customer_order`, `customer_order_line` |
| `Спецификация.xlsx` | материал, операция, единица, норма, часы | `item`, `specification`, `specification_component` |
| `Цены.xlsx` | ресурс, цена | `price` |
| `Заказ на производство.xlsx` | заказ, дата запуска, изделие, плановый расход | `production_order`, `production_product`, `production_resource` |
| `Заметки.json` | заголовок, логин, текст, дата | `notes` |

В документах номера записаны как «№ 1». В базе к ним добавляется префикс варианта: заказ покупателя становится `V01-01`, производственный заказ `V01-P-01`.

### Шаг 7. Загрузите заказчиков из JSON

Сначала разберите одну запись JSON по полям.

| Поле таблицы | Откуда значение | Почему |
|---|---|---|
| `id` | `id` из JSON | код хранится текстом, ведущие нули не теряются |
| `name` | `name` из JSON | название организации |
| `inn` | `inn` из JSON | пустая строка, если ИНН нет |
| `address` | `addres` из JSON | в таблице поле переименовано |
| `phone` | `phone` из JSON | контакт |
| `party_type` | `type` из JSON | роль контрагента |

<figure class="diagram">
<img src="reports/screens/mysql/json-source.png" alt="Файл Заказчики.json: коды, названия и адреса">
<figcaption>Источник: JSON с полями `id`, `name`, `inn`, `addres`, `phone`, `type`. Код хранится строкой.</figcaption>
</figure>

Перед вставкой откройте шпаргалку.

<details class="hint">
<summary>Шпаргалка: INSERT</summary>

```sql
INSERT INTO имя_таблицы (поле1, поле2, поле3)
VALUES (значение1, значение2, значение3);
```

`INSERT INTO` выбирает таблицу. В скобках перечислены поля в том порядке, в котором пойдут значения. `VALUES` начинает список значений. Текст и даты пишут в кавычках, числа без кавычек. Несколько строк разделяют запятыми, после последней строки запятая не ставится.

</details>

Вставьте все строки одним запросом:

```sql
INSERT INTO counterparty (id, name, inn, address, phone, party_type) VALUES
('000000001', 'ООО "Поставка"', '', 'г. Пятигорск', '+79198634592', 'Поставщик'),
('000000002', 'ООО "Кинотеатр Квант"', '26320045123', 'г. Железноводск, ул. Мира, 123', '+79884581555', 'Покупатель'),
('000000008', 'ООО "Новый JDTO"', '26320045111', 'г. Железноводск', '+79884581555', 'Покупатель'),
('000000003', 'ООО "Ромашка"', '4140784214', 'г. Омск, ул. Строителей, 294', '+79882584546', 'Поставщик'),
('000000009', 'ООО "Ипподром"', '5874045632', 'г. Уфа, ул. Набережная, 37', '+79627486389', 'Поставщик'),
('000000010', 'ООО "Ассоль"', '2629011278', 'г. Калуга, ул. Пушкина, 94', '+79184572398', 'Покупатель');
```

В заказе указан ИП Томилин, а среди шести записей JSON его нет. Добавьте его отдельной строкой. Изготовитель тоже добавляется отдельно: в заказе он указан в блоке «Исполнитель».

```sql
INSERT INTO counterparty (id, name, inn, address, phone, party_type) VALUES
('000000004', 'ИП Томилин Александр Сергеевич', '', 'г. Пятигорск', '', 'Покупатель'),
('M-001', 'ООО ТД "Вершина"', '', 'г. Пятигорск', '', 'Изготовитель');
```

<figure class="diagram">
<img src="reports/screens/mysql/t2-insert-sql.png" alt="Вставка заказчиков запросом INSERT в phpMyAdmin">
<figcaption>Код в phpMyAdmin: список полей и значения в том же порядке. Текстовые значения в кавычках.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/mysql/t2-customers.png" alt="Таблица counterparty после загрузки: восемь контрагентов">
<figcaption>Результат: шесть записей JSON, ИП Томилин и изготовитель. Коды сохранили ведущие нули, `addres` стало `address`, `type` стало `party_type`.</figcaption>
</figure>

### Шаг 8. Загрузите изделия, цены, спецификацию, заказ и производство

#### Изделия и ресурсы

Сначала создайте строки в `item`. Одна таблица хранит и изделие, и материалы, и операции, а различает их поле `kind`.

| Поле | Откуда значение | Почему |
|---|---|---|
| `id` | назначается по порядку | 1 изделие, 2-6 материалы и операции |
| `code` | код из заказа и производственного заказа | код нужен для связи с документами |
| `name` | название из заказа, спецификации или цен | одинаковое имя во всех файлах |
| `kind` | по разделу файла | `product`, `material` или `operation` |
| `unit` | единица из спецификации или цен | шт, тыс. шт, ч |

```sql
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
```

<figure class="diagram">
<img src="reports/screens/prep/V01_order_xlsx.png" alt="Заказ покупателя: изделие, код, количество и цена">
<figcaption>Из заказа берём изделие, код и количество. Название изделия становится строкой `product` в `item`.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/prep/V01_spec_xlsx.png" alt="Спецификация: материалы, операции и нормы">
<figcaption>Из спецификации берём названия материалов и операций, единицы и нормы. Каждая строка станет отдельным ресурсом в `item`.</figcaption>
</figure>

#### Цены

| Поле | Откуда значение | Почему |
|---|---|---|
| `item_id` | код ресурса из `item` | цена ссылается на ресурс, а не на название |
| `valid_from` | `2026-04-01` | дата начала действия задана условием варианта |
| `amount` | столбец «Цена» в `Цены.xlsx` | цена за единицу ресурса |

```sql
INSERT INTO price (item_id, valid_from, amount) VALUES
(2, '2026-04-01', 3250.00),
(3, '2026-04-01', 95.00),
(4, '2026-04-01', 140.00),
(5, '2026-04-01', 595.00),
(6, '2026-04-01', 245.00),
(7, '2026-04-01', 1400.00),
(8, '2026-04-01', 450.00),
(9, '2026-04-01', 950.00);
```

<figure class="diagram">
<img src="reports/screens/prep/V01_prices_xlsx.png" alt="Цены: ресурс и цена">
<figcaption>Источник цен: название ресурса и цена. Дата `2026-04-01` задана условием варианта.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/mysql/t2-price-table.png" alt="Таблица price после вставки цен">
<figcaption>Результат: цены в `price`. У каждого ресурса своя строка и дата начала действия.</figcaption>
</figure>

#### Спецификация и состав

| Поле | Откуда значение | Почему |
|---|---|---|
| `specification.id` | 1 | в варианте одна спецификация |
| `specification.product_id` | 1 | ссылка на изделие |
| `specification.name` | шапка «Изделие» | название изделия |
| `specification.output_qty` | 1 | нормы даны на одну единицу |
| `specification.manufacturer_id` | `M-001` | изготовитель из шапки |
| `specification_component.qty` | «Норма расхода» | норма материала |
| `specification_component.time_norm` | «Норма времени» | часы операции |

```sql
INSERT INTO specification (id, product_id, name, output_qty, manufacturer_id)
VALUES (1, 1, 'Стол кухонный "Самобранка"', 1.000, 'M-001');

INSERT INTO specification_component (specification_id, item_id, qty, time_norm) VALUES
(1, 2, 1.000, 0.000),
(1, 3, 2.000, 0.000),
(1, 4, 4.000, 0.000),
(1, 5, 0.012, 0.000),
(1, 6, 4.000, 0.000),
(1, 7, 0.000, 0.750),
(1, 8, 0.000, 1.500),
(1, 9, 0.000, 0.500);
```

Для материалов `qty` это норма на единицу, `time_norm` равно нулю. Для операций `qty` равно нулю, `time_norm` хранит часы. Такая запись позволяет выбрать нужное поле через `CASE` в задании 3.

<figure class="diagram">
<img src="reports/screens/mysql/t2-spec.png" alt="Состав спецификации V01: материалы и операции с нормами">
<figcaption>Результат: восемь строк состава. У материалов заполнена норма, у операций время.</figcaption>
</figure>

#### Заказ и строка заказа

| Поле | Откуда значение | Почему |
|---|---|---|
| `customer_order.doc_no` | номер заказа | `V01-01` |
| `customer_order.doc_date` | дата заказа | `22.04.2026` |
| `customer_order.customer_id` | код ИП Томилина | `000000004` |
| `customer_order.executor_id` | код изготовителя | `M-001` |
| `customer_order_line.product_id` | изделие | `1` |
| `customer_order_line.qty` | «Кол-во» | 2 |
| `customer_order_line.sale_price` | «Цена» | 14 120,00 |
| `customer_order_line.discount` | «Скидка» | 1 412,00 |

```sql
INSERT INTO customer_order (id, doc_no, doc_date, customer_id, executor_id)
VALUES (1, 'V01-01', '2026-04-22', '000000004', 'M-001');

INSERT INTO customer_order_line (id, order_id, product_id, qty, sale_price, discount)
VALUES (1, 1, 1, 2, 14120.00, 1412.00);
```

<figure class="diagram">
<img src="reports/screens/prep/V01_order_xlsx.png" alt="Заказ покупателя: шапка и строка продукции">
<figcaption>Источник: номер, дата, заказчик, изделие, количество, цена и скидка. Из шапки получается `customer_order`, из строки продукции `customer_order_line`.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/mysql/t2-order.png" alt="Заказ V01-01 в phpMyAdmin: номер, дата, заказчик и исполнитель">
<figcaption>Результат: шапка заказа V01-01. Дата 22.04.2026, заказчик 000000004, исполнитель M-001.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/mysql/t2-lines-table.png" alt="Строка заказа в таблице customer_order_line">
<figcaption>Результат: строка заказа. Количество 2, цена 14 120,00, скидка 1 412,00.</figcaption>
</figure>

#### Производственный заказ

| Поле | Откуда значение | Почему |
|---|---|---|
| `production_order.doc_no` | номер производственного заказа | `V01-P-01` |
| `production_order.doc_date` | дата заказа покупателя | `22.04.2026` |
| `production_order.launch_date` | «Дата запуска» | `23.04.2026` |
| `production_order.department` | «Подразделение» | основное производство |
| `production_product.qty` | «Продукция к выпуску» | 2 |
| `production_resource.qty` | «Потребность в материалах» | плановый расход |
| `production_resource.time_norm` | «Технологические операции» | плановые часы |

```sql
INSERT INTO production_order (id, doc_no, doc_date, launch_date, department)
VALUES (1, 'V01-P-01', '2026-04-22', '2026-04-23', 'Основное подразделение');

INSERT INTO production_product (production_id, product_id, qty)
VALUES (1, 1, 2);

INSERT INTO production_resource (production_id, item_id, qty, time_norm) VALUES
(1, 2, 2.000, 0.000),
(1, 3, 4.000, 0.000),
(1, 4, 8.000, 0.000),
(1, 5, 0.024, 0.000),
(1, 6, 8.000, 0.000),
(1, 7, 0.000, 2.000),
(1, 8, 0.000, 2.000),
(1, 9, 0.000, 2.000);
```

<figure class="diagram">
<img src="reports/screens/prep/V01_production_xlsx.png" alt="Заказ на производство V01: продукция, материалы и операции">
<figcaption>Источник: изделие, потребность в материалах и технологические операции. Каждая строка становится строкой `production_resource`.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/mysql/t2-production.png" alt="Шапка производственного заказа в таблице production_order">
<figcaption>Результат: производственный заказ V01-P-01. Дата запуска и подразделение перенесены из Excel.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/mysql/t2-production-product.png" alt="Продукция к выпуску в таблице production_product">
<figcaption>Результат: в заказе две единицы изделия. Количество взято из строки «Продукция, работа».</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/mysql/t2-production-resource.png" alt="Плановый расход ресурсов в таблице production_resource">
<figcaption>Результат: восемь строк планового расхода. Материалы и операции хранятся в одной таблице.</figcaption>
</figure>

### Шаг 9. Проверьте данные и ограничения

Выполните проверки:

```sql
SELECT COUNT(*) AS customers FROM counterparty;

SELECT id, name FROM counterparty ORDER BY id LIMIT 3;

SELECT COUNT(*) AS items FROM item;

SELECT COUNT(*) AS components FROM specification_component;

SELECT COUNT(*) AS orders FROM customer_order;

SELECT COUNT(*) AS production_rows FROM production_resource;
```

Ожидается восемь контрагентов, девять ресурсов, восемь строк состава, один заказ и восемь строк производственного расхода.

Проверьте внешние ключи. Попробуйте вставить заказ с несуществующим заказчиком:

```sql
INSERT INTO customer_order (id, doc_no, doc_date, customer_id, executor_id)
VALUES (99, 'TEST-1', '2026-04-25', 'NO-SUCH', 'M-001');
```

Сервер должен отклонить запрос с ошибкой 1452. Это доказательство, что внешний ключ работает. После проверки ничего удалять не нужно: строка не вставилась.

### Шаг 10. Сделайте выгрузку SQL

Откройте базу `dkip2027_course`, вкладку `Экспорт`. Выберите метод `Быстрый`, формат `SQL`, нажмите `Экспорт`. Браузер скачает файл. Переименуйте его в `dkip2027-mysql.sql` и положите в папку `task2`.

<figure class="diagram">
<img src="reports/screens/mysql/t2-export.png" alt="Экспорт базы dkip2027_course в SQL-файл">
<figcaption>Экспорт SQL: выбран формат SQL и метод Быстрый. Файл можно приложить к работе.</figcaption>
</figure>

Откройте файл в блокноте и проверьте две вещи: в нём есть команды `CREATE TABLE` и команды `INSERT INTO`. Если есть только структура, данные не выгрузились. Если есть только вставки, не выгрузилась структура.

### Шаг 11. Восстановите базу в пустую копию

Создайте базу `dkip2027_restore`. Откройте её, вкладку `Импорт`, выберите файл `dkip2027-mysql.sql`, формат `SQL`, кодировку `utf-8` и нажмите `Импорт`. После завершения проверьте список таблиц и число строк. Если данные на месте, выгрузка рабочая.

<figure class="diagram">
<img src="reports/screens/mysql/t2-restore.png" alt="Восстановление базы из SQL-файла в пустую копию">
<figcaption>Восстановление: файл выгрузки импортирован в пустую базу, таблицы и данные появились снова.</figcaption>
</figure>

## Команды и приёмы, которые нужны чаще всего

| Действие | Где выполнить | Зачем |
|---|---|---|
| `Создать БД` | phpMyAdmin, левая панель | новая база |
| `CREATE TABLE` | phpMyAdmin, SQL | создать таблицу запросом |
| `PRIMARY KEY` | внутри `CREATE TABLE` | уникальность строк |
| `FOREIGN KEY` / `ALTER TABLE` | phpMyAdmin, SQL | связь таблиц |
| `INSERT INTO` | phpMyAdmin, SQL | загрузка строк из JSON и Excel |
| `SELECT` | phpMyAdmin, SQL | проверка данных и ключей |
| `SHOW CREATE TABLE` | phpMyAdmin, SQL | полное определение таблицы |
| `SHOW TABLES;` | phpMyAdmin, SQL | список таблиц |
| `SELECT ... FROM information_schema` | phpMyAdmin, SQL | проверка ключей |
| `Экспорт` | phpMyAdmin, вкладка базы | SQL-файл для сдачи |
| `Импорт` | phpMyAdmin, вкладка базы | восстановление |

## Частые ошибки

**Таблица создана без первичного ключа.** Строки нельзя отличить, внешние ключи не работают. Исправление: добавить `PRIMARY KEY` через структуру таблицы.

**Код заказчика объявлен числом.** Ведущие нули исчезают. Исправление: `VARCHAR(32)` и вставка значения в кавычках.

**Внешний ключ создан до родительской таблицы.** Сервер отвечает ошибкой 1215. Исправление: сначала создать справочники.

**Типы ссылающегося и целевого поля разные.** Например, `INT` ссылается на `VARCHAR`. Исправление: привести типы к одному виду.

**Данные вставлены до создания связей.** Строка ссылается на несуществующего родителя. Исправление: сначала загрузить справочники.

**JSON перенесён с другим именем поля.** `addres` не становится `address` автоматически. Исправление: сопоставить имена в `INSERT`.

**Дата записана как `22.04.2026`.** MySQL ждёт `2026-04-22`. Исправление: привести дату к формату `ГГГГ-ММ-ДД`.

**Выгрузка без данных.** В файле только `CREATE TABLE`. Исправление: повторить экспорт и включить данные.

## Чек-лист перед сдачей

- База `dkip2027_course` создана в `utf8mb4_unicode_ci`.
- Все таблицы используют `InnoDB`.
- У каждой таблицы есть первичный ключ.
- Внешние ключи созданы и проверены запросом.
- Коды заказчиков хранятся текстом и не потеряли ведущие нули.
- Заказчики загружены из JSON, ИП Томилин и изготовитель добавлены отдельно.
- Заказ, спецификация, состав и цены загружены из Excel.
- Производственный заказ и плановый расход загружены из Excel.
- Даты записаны в формате `ГГГГ-ММ-ДД`.
- Проверка с несуществующим заказчиком даёт ошибку 1452.
- Выгрузка `dkip2027-mysql.sql` содержит структуру и данные.
- База восстановлена в пустую копию.
- Протокол заполнен фактическими результатами и скриншотами.
