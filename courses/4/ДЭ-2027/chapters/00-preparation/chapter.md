---
title: Предварительная подготовка
dek: "Разбор первых трёх заданий V01 в draw.io и XAMPP: диаграмма, база в phpMyAdmin и SQL-запрос стоимости."
chapter: "Подготовка"
level: СПО
glyph: "00"
outcomes:
  - Строить ER-диаграмму в draw.io и сохранять её в PDF
  - Создавать базу и таблицы в phpMyAdmin, импортировать данные
  - Считать стоимость заказа запросом с JOIN и агрегацией
---

## Зачем этот раздел

Первые три задания проверяют модель данных, базу и расчёт. В этом разделе они разобраны на варианте V01 «ООО ТД «Вершина»» в приложениях, которые уже установлены: draw.io для диаграммы, XAMPP и phpMyAdmin для базы. Дополнительно в конце раздела разобран вариант V02 на тех же инструментах.

| Задание | Инструмент | Что сдать |
|---|---|---|
| 1. ER-диаграмма | draw.io | PDF с диаграммой и исходник `.drawio` |
| 2. База и импорт | XAMPP, phpMyAdmin | SQL-скрипт схемы, выгрузка базы |
| 3. SQL-запрос стоимости | phpMyAdmin | SQL-запрос и таблица результата |

Разбор идёт на варианте V01 «Мебельное производство». Варианты V02 и V03 даны для самостоятельной работы: структура заданий та же, меняются предприятие, продукция и числа. Снимки экрана кликабельны: по щелчку они открываются в полном размере.

## Три тестовых варианта

| Вариант | Предприятие | Продукция | Количество |
|---|---|---|---|
| V01 | ООО ТД «Вершина» | Стол кухонный «Самобранка» | 2 |
| V02 | Пекарня «Колос» | Хлеб ржаной 500 г | 40 |
| V03 | Мастерская «Глина» | Кружка 300 мл | 18 |

## Исходные данные варианта

- [V01: архив исходных данных](reports/variants/V01/V01_исходные_данные.zip)
- [V02: архив исходных данных](reports/variants/V02/V02_исходные_данные.zip)
- [V03: архив исходных данных](reports/variants/V03/V03_исходные_данные.zip)

В архиве шесть файлов: `Заказ покупателя.xlsx`, `Заказ на производство.xlsx`, `Спецификация.xlsx`, `Цены.xlsx`, `Расчет стоимости.xlsx` и `Заказчики.json`. В JSON лежат заказчики с полями `id`, `name`, `inn`, `addres`, `phone`, `type`. В книгах Excel лежат ресурсы, нормы, цены и строки документов.

## Задание 1. ER-диаграмма в draw.io

### Что требуется

Нарисовать ER-диаграмму предприятия по документам варианта и сохранить её в PDF. На диаграмме должны быть таблицы, поля, первичные и внешние ключи, связи и кратность. Модель приводится к третьей нормальной форме.

Сдаются два файла: PDF с диаграммой и исходник `.drawio`. PDF проверяют на экране и на печати, исходник нужен, чтобы показать, что схема собрана в редакторе, а не нарисована картинкой.

В базовом наборе получается двенадцать таблиц и четырнадцать связей. В варианте другое предприятие, другая продукция и другие ресурсы, но набор сущностей тот же: контрагенты, ресурсы, цены, спецификация, состав, заказ покупателя, производственный заказ, пользователи и заметки.

### Сначала разберите исходные данные

До открытия draw.io прочитайте файлы варианта и выпишите факты. Диаграмма начинается не с прямоугольников, а с ответов на вопросы о системе.

| Файл | Что внутри | Что из него берут |
|---|---|---|
| `Заказчики.json` | заказчики: код, название, ИНН, адрес, телефон, тип | таблица `counterparty` |
| `Спецификация.xlsx` и `Цены.xlsx` | ресурсы, нормы, часы и цены | таблицы `item`, `price`, `specification_component` |
| `Заказ покупателя.xlsx` и `Заказ на производство.xlsx` | шапки и строки документов | `customer_order`, `customer_order_line`, `production_order` |

Задайте себе восемь вопросов и запишите ответы в черновик:

1. Кто участники системы: заказчик, изготовитель, поставщик, кладовщик, менеджер, администратор?
2. Какие документы есть в системе: заказ, спецификация, производственный заказ, накладная?
3. Какие документы состоят из шапки и строк?
4. Какие данные повторяются в строках и должны быть вынесены отдельно?
5. Какие значения меняются со временем: цена, остаток, статус?
6. Какие данные являются справочными: товар, материал, операция, площадка?
7. Что вычисляется, а не хранится: стоимость заказа, сумма строки, количество изделий?
8. Какие связи получаются один ко многим и где нужна промежуточная таблица?

Для V01 черновик выглядит так:

```text
Участники: покупатель, изготовитель, пользователь приложения.
Документы: заказ покупателя, спецификация изделия, производственный заказ.
Справочники: товар, материал, операция, цена.
Строки: состав спецификации, строки заказа, продукция к выпуску, расход ресурсов.
Вычисляется: стоимость заказа, сумма строки, число изделий в заказе.
```

### Ключевые понятия простыми словами

**ER-диаграмма** это схема данных, которая показывает, какие сущности есть в системе и как они связаны. Её читают слева направо: таблица, её поля, ключи и линии связей.

**Сущность** это тип объекта, о котором система хранит одинаковые по структуре записи. `counterparty` описывает контрагента, `customer_order` описывает заказ. Один конкретный заказ это экземпляр сущности, а не отдельная таблица.

**Атрибут** это поле сущности: название, дата, цена, количество. Атрибут отвечает на вопрос «какое свойство мы храним», а не «что делает система».

**Ключ** это поле или набор полей, по которым отличают одну запись от другой. **Первичный ключ** (PK) уникален внутри своей таблицы. **Внешний ключ** (FK) хранит ссылку на первичный ключ другой таблицы и создаёт связь.

| Понятие | Простыми словами | Пример |
|---|---|---|
| Первичный ключ | номер строки в своей таблице | `counterparty.id` |
| Внешний ключ | ссылка на строку в другой таблице | `customer_order.customer_id` |
| Составной ключ | уникальность по двум полям сразу | `price.item_id` + `price.valid_from` |
| Связь один ко многим | один заказ, много строк | `customer_order` → `customer_order_line` |
| Связь многие ко многим | товар входит во много спецификаций, спецификация содержит много товаров | промежуточная `specification_component` |

**Третья нормальная форма** означает три простых правила: в ячейке одно значение, поле зависит от всего ключа, неключевые поля не зависят друг от друга. Цена материала хранится в `price`, а не в строке состава. Норма хранится в составе, а не в справочнике товаров. Стоимость заказа не хранится нигде, потому что её можно посчитать.

### Шаг 1. Откройте draw.io и выберите фигуру

Откройте `app.diagrams.net`. Учётная запись не нужна. Выберите пустую диаграмму и хранение на устройстве.

Слева найдите раздел **Отношения сущностей** и фигуру **Entity**. Это таблица с заголовком и строками. Именно она нужна для ER-диаграммы.

<a href="reports/screens/prep/drawio-shapes.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-shapes.png" alt="Панель draw.io с открытым разделом Отношения сущностей и фигурой Entity"></a>
<figcaption>Раздел «Отношения сущностей» и фигура Entity. Заголовок станет именем таблицы, строки полями.</figcaption>

Не берите обычный прямоугольник: в нём нет строк, поля придётся рисовать линиями, и они разъедутся при первом сдвиге. Не берите и готовую таблицу из другого раздела, пока не понимаете, как она устроена.

### Шаг 2. Таблица `counterparty`: кто участвует в системе

Первая таблица появляется из вопроса «кто заказчик и кто исполнитель». В JSON есть шесть заказчиков, в описании варианта есть изготовитель. Все они имеют одинаковый набор полей, значит, это одна сущность.

| Поле | Тип | Ключ | Зачем |
|---|---|---|---|
| `id` | TEXT | PK | код контрагента из документа, ведущие нули сохраняются |
| `name` | TEXT |  | название организации |
| `inn` | TEXT |  | налоговый номер, может быть пустым |
| `address` | TEXT |  | адрес для документов |
| `phone` | TEXT |  | контакт |
| `party_type` | TEXT |  | покупатель, изготовитель или поставщик |

Создайте Entity, назовите её `counterparty`, добавьте шесть строк. В строках пишите `PK id TEXT`, затем `name TEXT` и так далее. Буквы `PK` и `FK` это пометки для проверяющего, а не часть имени поля.

<a href="reports/screens/prep/drawio-table-01.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-table-01.png" alt="Первая таблица counterparty в draw.io с полями и первичным ключом"></a>
<figcaption>Таблица `counterparty`. Первичный ключ `id`, остальные поля описывают контрагента.</figcaption>

Проверка: если убрать `id`, две организации с одинаковым названием станут неразличимы. Значит, ключ выбран правильно.

### Шаг 3. Таблица `item`: один справочник ресурсов

В книгах Excel есть материалы и операции. У них разные единицы, но общая структура: код, название, вид, единица. Если сделать отдельные таблицы `material` и `operation`, появятся две почти одинаковые сущности и два внешних ключа в составе. Проще один справочник с полем `kind`.

| Поле | Тип | Ключ | Зачем |
|---|---|---|---|
| `id` | INTEGER | PK | внутренний код ресурса |
| `code` | TEXT |  | код из документа |
| `name` | TEXT |  | название материала или операции |
| `kind` | TEXT |  | `product`, `material` или `operation` |
| `unit` | TEXT |  | метр, штука, час |


Ход мысли: «Что общего у ткани и раскроя? Оба расходуются в спецификации. Чем отличаются? Единицей и способом расчёта. Значит, общее выносим в справочник, различие в поле вида».

### Шаг 4. Таблица `price`: цена меняется во времени

Цена не принадлежит товару навсегда: с 1 марта одна, с 1 апреля другая. Если хранить цену в `item`, история потеряется. Появляется отдельная сущность с составным ключом: ресурс плюс дата, с которой цена действует.

| Поле | Тип | Ключ | Зачем |
|---|---|---|---|
| `item_id` | INTEGER | PK, FK | ссылка на ресурс |
| `valid_from` | TEXT | PK | дата начала действия цены |
| `amount` | REAL |  | цена за единицу |


Составной ключ читается так: одна и та же цена не может быть записана дважды на одну дату, но на разные даты может.

### Шаг 5. Таблица `specification`: шапка рецепта изделия

Спецификация описывает, из чего и как делают изделие. У неё есть номер, название, выпуск и изготовитель. Это шапка, как у заказа: одна спецификация на изделие.

| Поле | Тип | Ключ | Зачем |
|---|---|---|---|
| `id` | INTEGER | PK | номер спецификации |
| `product_id` | INTEGER | FK | ссылка на изделие |
| `name` | TEXT |  | название спецификации |
| `output_qty` | REAL |  | сколько единиц выпускается по нормам |
| `manufacturer_id` | TEXT | FK | кто изготавливает |


Почему `product_id` отдельно, а не название изделия? Название уже есть в `item`. Повторять его в спецификации значит хранить две версии одного факта.

### Шаг 6. Таблица `specification_component`: строки состава

В одной спецификации много материалов и операций. Это типичная связь многие ко многим, её нельзя оставить двумя стрелками. Появляется промежуточная таблица, где каждая строка это один ресурс в составе.

| Поле | Тип | Ключ | Зачем |
|---|---|---|---|
| `specification_id` | INTEGER | PK, FK | ссылка на шапку |
| `item_id` | INTEGER | PK, FK | ссылка на ресурс |
| `qty` | REAL |  | норма расхода на единицу |
| `time_norm` | REAL |  | часы для операции, `1` для материала |


Проверка: одну и ту же ткань нельзя добавить в спецификацию дважды с разными нормами без объяснения. Составной ключ это запрещает.

### Шаг 7. Таблица `customer_order`: шапка заказа

Заказ приходит от покупателя и содержит номер, дату, заказчика и исполнителя. Это шапка документа. Строки заказа появятся в следующей таблице.

| Поле | Тип | Ключ | Зачем |
|---|---|---|---|
| `id` | INTEGER | PK | внутренний номер заказа |
| `doc_no` | TEXT |  | номер документа из бумаги |
| `doc_date` | TEXT |  | дата заказа |
| `customer_id` | TEXT | FK | кто заказал |
| `executor_id` | TEXT | FK | кто выполняет |


Номер документа и внутренний `id` это разные вещи. Номер может измениться при переносе, а `id` остаётся ключом.

### Шаг 8. Таблица `customer_order_line`: строки заказа

В заказе несколько изделий. Если хранить их в шапке через запятую, нельзя посчитать количество и цену по каждому. Появляется таблица строк.

| Поле | Тип | Ключ | Зачем |
|---|---|---|---|
| `id` | INTEGER | PK | номер строки |
| `order_id` | INTEGER | FK | ссылка на шапку |
| `product_id` | INTEGER | FK | ссылка на изделие |
| `qty` | INTEGER |  | количество |
| `sale_price` | REAL |  | продажная цена |
| `discount` | REAL |  | скидка |


Ход мысли: «Что повторяется в каждой строке? Номер заказа и дата. Значит, они остаются в шапке. Что своё у строки? Изделие, количество, цена. Значит, это поля строки».

### Шаг 9. Таблица `production_order`: шапка производственного заказа

Производственный заказ запускает выпуск. У него свой номер, дата, дата запуска и подразделение. Это отдельный документ, поэтому отдельная шапка.

| Поле | Тип | Ключ | Зачем |
|---|---|---|---|
| `id` | INTEGER | PK | внутренний номер |
| `doc_no` | TEXT |  | номер документа |
| `doc_date` | TEXT |  | дата создания |
| `launch_date` | TEXT |  | дата запуска |
| `department` | TEXT |  | цех или участок |


### Шаг 10. Таблица `production_product`: что выпускаем

В производственном заказе может быть несколько изделий. Появляется таблица продукции к выпуску с количеством.

| Поле | Тип | Ключ | Зачем |
|---|---|---|---|
| `production_id` | INTEGER | PK, FK | ссылка на производственный заказ |
| `product_id` | INTEGER | PK, FK | ссылка на изделие |
| `qty` | INTEGER |  | сколько выпустить |


### Шаг 11. Таблица `production_resource`: плановый расход

Для производства нужно знать, сколько материалов и часов потребуется. Это отдельная таблица, потому что расход относится к производственному заказу, а не к заказу покупателя.

| Поле | Тип | Ключ | Зачем |
|---|---|---|---|
| `production_id` | INTEGER | PK, FK | ссылка на производственный заказ |
| `item_id` | INTEGER | PK, FK | ссылка на ресурс |
| `qty` | REAL |  | плановое количество |
| `time_norm` | REAL |  | плановые часы |


### Шаг 12. Таблица `users`: кто входит в приложение

В следующих заданиях приложению нужен вход. Появляется справочник учётных записей: логин, хеш пароля, роль, число ошибок и блокировка.

| Поле | Тип | Ключ | Зачем |
|---|---|---|---|
| `id` | INTEGER | PK | номер пользователя |
| `login` | TEXT |  | имя для входа |
| `password_hash` | TEXT |  | хеш, не сам пароль |
| `role` | TEXT |  | права |
| `failed_attempts` | INTEGER |  | счётчик ошибок |
| `is_locked` | INTEGER |  | признак блокировки |


### Шаг 13. Таблица `notes`: заметки сотрудников

Заметка принадлежит пользователю. Она не входит в заказ и не влияет на стоимость, но нужна приложению. Появляется последняя таблица с внешним ключом на `users`.

| Поле | Тип | Ключ | Зачем |
|---|---|---|---|
| `id` | INTEGER | PK | номер заметки |
| `title` | TEXT |  | заголовок |
| `content` | TEXT |  | текст |
| `id_user` | INTEGER | FK | автор |
| `created_at` | TEXT |  | дата создания |


После двенадцатой таблицы на холсте двенадцать сущностей. Если появилась тринадцатая, проверьте, не является ли она строкой уже существующего документа.

### Шаг 14. Соедините таблицы связями

Связь рисуется от внешнего ключа к первичному ключу. Наведите курсор на край таблицы, возьмите синюю стрелку и протяните к другой таблице. Подпись ставьте двойным щелчком по линии: `1:N`.

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

<a href="reports/screens/prep/drawio-er.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-er.png" alt="Полная ER-диаграмма V01: двенадцать таблиц и четырнадцать связей"></a>
<figcaption>Полная модель V01. Проверьте, что каждая линия соединяет внешний ключ с первичным, а не два произвольных поля.</figcaption>

Если линия идёт от строки заказа к шапке, подпись всё равно `1:N`: один заказ содержит много строк. Направление стрелки не меняет смысл кратности.

### Шаг 15. Проверьте третью нормальную форму

Пройдите по каждой таблице тремя вопросами:

1. Есть ли ячейка с несколькими значениями? Если да, вынесите значение в строку или отдельную таблицу.
2. Зависит ли поле от части составного ключа? Если да, вынесите его в таблицу с полным ключом.
3. Зависит ли неключевое поле от другого неключевого поля? Если да, вынесите зависимость отдельно.

Примеры для V01:

- цена хранится в `price`, потому что зависит от ресурса и даты, а не от строки заказа;
- норма хранится в `specification_component`, потому что относится к паре «спецификация и ресурс»;
- стоимость заказа не хранится: она вычисляется из количества, норм и цен;
- название изделия не дублируется в строке заказа: оно уже есть в `item`.

### Шаг 16. Сохраните исходник и выгрузите PDF

1. Откройте `Файл`, затем `Сохранить как` и выберите `Это устройство`.
2. На рабочем столе создайте личную папку по образцу `/Учебная папка/Название предмета/ФИО/номер практической работы`.
3. Назовите файл `V01_ER.drawio` и сохраните.
4. Откройте `Файл`, затем `Экспорт как`, затем `PDF`.
5. Оставьте экспорт всей диаграммы, а не выделения. Проверьте, что все двенадцать таблиц попали на лист.
6. Откройте PDF и увеличьте масштаб: подписи должны читаться без догадок.

<a href="reports/screens/prep/drawio-save-menu.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-save-menu.png" alt="Меню Файл в draw.io с командами сохранения и экспорта"></a>
<figcaption>Меню `Файл`: здесь находятся `Сохранить как` и `Экспорт как`. Сначала сохраните `.drawio`, затем экспортируйте PDF.</figcaption>

<a href="reports/screens/prep/drawio-export.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-export.png" alt="Диалог экспорта PDF в draw.io"></a>
<figcaption>Экспорт PDF. Не выбирайте «Только выделение», иначе на листе останется одна таблица.</figcaption>

Перед сдачей проверьте: двенадцать таблиц, у каждой первичный ключ, четырнадцать подписанных связей, нет вычисляемых полей. Если таблиц девять, скорее всего шапка заказа слита со строками. Если пятнадцать, появилась лишняя таблица под каждую строку документа.


## Задание 2. База в XAMPP и phpMyAdmin

Это основной маршрут для установленных приложений. Полный разбор каждой команды и ограничений находится в методичке [Задание 2. База данных и импорт](03-task-2-db.html). Здесь короткий маршрут V01, чтобы пройти первые три задания подряд.

### Шаг 1. Запустите Apache и MySQL

Откройте XAMPP Control Panel и нажмите `Start` у Apache и MySQL. На учебных компьютерах Apache слушает порт `4433`, MySQL слушает `3306`. Обе строки должны стать зелёными.

<figure class="diagram">
<img src="reports/screens/mysql/db-start.png" alt="XAMPP Control Panel с запущенными Apache и MySQL">
<figcaption>XAMPP: Apache и MySQL в состоянии Running. Без MySQL phpMyAdmin не подключится к базе.</figcaption>
</figure>

### Шаг 2. Откройте phpMyAdmin и создайте базу

Перейдите по адресу `http://localhost:4433/phpmyadmin`. Пользователь `root`, пароль пустой. В левой панели нажмите `Создать БД`, введите имя `dkip2027_course`, выберите сравнение `utf8mb4_unicode_ci` и нажмите `Создать`.

<figure class="diagram">
<img src="reports/screens/mysql/t2-create.png" alt="Создание базы dkip2027_course в phpMyAdmin">
<figcaption>Создание базы: имя, кодировка utf8mb4 и сравнение utf8mb4_unicode_ci.</figcaption>
</figure>

### Шаг 3. Создайте таблицы запросами

Все таблицы создаются запросами. Перед первым запросом откройте общую шпаргалку.

<details class="hint">
<summary>Шпаргалка: CREATE TABLE, ALTER TABLE, INSERT</summary>

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

`INSERT INTO` выбирает таблицу. В скобках перечислены поля в порядке значений. `VALUES` начинает список. Текст и даты в кавычках, числа без кавычек. Строки разделяют запятыми, после последней запятой нет.

</details>

Разберём `CREATE TABLE` на таблице `counterparty`:

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

- `CREATE TABLE counterparty` создаёт таблицу с именем `counterparty`.
- В скобках перечислены поля. У каждого три части: имя, тип и ограничения.
- `id VARCHAR(32) NOT NULL` хранит код текстом, поэтому ведущие нули не теряются.
- `PRIMARY KEY (id)` делает `id` первичным ключом.
- `CONSTRAINT ck_party_type CHECK (...)` разрешает только три значения типа контрагента.
- `ENGINE=InnoDB` включает поддержку внешних ключей, `DEFAULT CHARSET=utf8mb4` задаёт кодировку.

Остальные таблицы создайте по диаграмме. Ниже слайдер с двенадцатью определениями. Листайте стрелками и сверяйте поля, типы и ключи.

<div class="schema-slider" data-slider>
<div class="schema-slider-bar">
<strong>Все двенадцать таблиц: листайте стрелками</strong>
<div class="schema-slider-actions">
<button type="button" class="schema-btn" data-slider-prev aria-label="Предыдущая таблица">←</button>
<span class="schema-slider-counter" data-slider-counter>1 / 12</span>
<button type="button" class="schema-btn" data-slider-next aria-label="Следующая таблица">→</button>
</div>
</div>
<div class="schema-track" data-slider-track>
<article class="schema-slide" aria-label="counterparty">
<h4>1. <code>counterparty</code></h4>
<p>Контрагенты: покупатели, поставщики и изготовители. Код хранится текстом, поэтому ведущие нули не теряются.</p>
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
<p>Справочник продукции, материалов и операций. Поле kind показывает, что это за ресурс.</p>
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
<p>История цен. Ключ из ресурса и даты не даёт двум ценам действовать с одной даты.</p>
<pre><code>CREATE TABLE price (
  item_id INT NOT NULL,
  valid_from DATE NOT NULL,
  amount DECIMAL(14,2) NOT NULL,
  PRIMARY KEY (item_id, valid_from),
  CONSTRAINT fk_price_item
    FOREIGN KEY (item_id) REFERENCES item (id),
  CONSTRAINT ck_price_amount CHECK (amount &gt;= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="specification">
<h4>4. <code>specification</code></h4>
<p>Шапка спецификации изделия. Поле output_qty показывает, на какое количество изделий даны нормы.</p>
<pre><code>CREATE TABLE specification (
  id INT NOT NULL,
  product_id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  output_qty DECIMAL(14,3) NOT NULL,
  manufacturer_id VARCHAR(32) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_spec_product (product_id),
  KEY ix_spec_maker (manufacturer_id),
  CONSTRAINT fk_spec_product
    FOREIGN KEY (product_id) REFERENCES item (id),
  CONSTRAINT fk_spec_maker
    FOREIGN KEY (manufacturer_id) REFERENCES counterparty (id),
  CONSTRAINT ck_spec_output CHECK (output_qty &gt; 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="specification_component">
<h4>5. <code>specification_component</code></h4>
<p>Нормы материалов и время операций. Для материала заполнено qty, для операции time_norm.</p>
<pre><code>CREATE TABLE specification_component (
  specification_id INT NOT NULL,
  item_id INT NOT NULL,
  qty DECIMAL(14,3) NOT NULL,
  time_norm DECIMAL(14,3) NOT NULL,
  PRIMARY KEY (specification_id, item_id),
  KEY ix_comp_item (item_id),
  CONSTRAINT fk_comp_spec
    FOREIGN KEY (specification_id) REFERENCES specification (id),
  CONSTRAINT fk_comp_item
    FOREIGN KEY (item_id) REFERENCES item (id),
  CONSTRAINT ck_comp_qty CHECK (qty &gt;= 0),
  CONSTRAINT ck_comp_time CHECK (time_norm &gt;= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="customer_order">
<h4>6. <code>customer_order</code></h4>
<p>Шапка заказа покупателя: номер, дата, заказчик и исполнитель.</p>
<pre><code>CREATE TABLE customer_order (
  id INT NOT NULL,
  doc_no VARCHAR(64) NOT NULL,
  doc_date DATE NOT NULL,
  customer_id VARCHAR(32) NOT NULL,
  executor_id VARCHAR(32) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_order_doc (doc_no),
  KEY ix_order_customer (customer_id),
  KEY ix_order_executor (executor_id),
  CONSTRAINT fk_order_customer
    FOREIGN KEY (customer_id) REFERENCES counterparty (id),
  CONSTRAINT fk_order_executor
    FOREIGN KEY (executor_id) REFERENCES counterparty (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="customer_order_line">
<h4>7. <code>customer_order_line</code></h4>
<p>Строки заказа: изделие, количество, продажная цена и скидка.</p>
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
  CONSTRAINT fk_line_order
    FOREIGN KEY (order_id) REFERENCES customer_order (id),
  CONSTRAINT fk_line_product
    FOREIGN KEY (product_id) REFERENCES item (id),
  CONSTRAINT ck_line_qty CHECK (qty &gt; 0),
  CONSTRAINT ck_line_price CHECK (sale_price &gt;= 0),
  CONSTRAINT ck_line_discount CHECK (discount &gt;= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="production_order">
<h4>8. <code>production_order</code></h4>
<p>Шапка производственного заказа: номер, дата документа, дата запуска и подразделение.</p>
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
<p>Продукция к выпуску по производственному заказу.</p>
<pre><code>CREATE TABLE production_product (
  production_id INT NOT NULL,
  product_id INT NOT NULL,
  qty INT NOT NULL,
  PRIMARY KEY (production_id, product_id),
  KEY ix_prod_product (product_id),
  CONSTRAINT fk_pp_order
    FOREIGN KEY (production_id) REFERENCES production_order (id),
  CONSTRAINT fk_pp_item
    FOREIGN KEY (product_id) REFERENCES item (id),
  CONSTRAINT ck_pp_qty CHECK (qty &gt; 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="production_resource">
<h4>10. <code>production_resource</code></h4>
<p>Плановый расход материалов и времени по производственному заказу.</p>
<pre><code>CREATE TABLE production_resource (
  production_id INT NOT NULL,
  item_id INT NOT NULL,
  qty DECIMAL(14,3) NOT NULL,
  time_norm DECIMAL(14,3) NOT NULL,
  PRIMARY KEY (production_id, item_id),
  KEY ix_prod_resource (item_id),
  CONSTRAINT fk_pr_order
    FOREIGN KEY (production_id) REFERENCES production_order (id),
  CONSTRAINT fk_pr_item
    FOREIGN KEY (item_id) REFERENCES item (id),
  CONSTRAINT ck_pr_qty CHECK (qty &gt;= 0),
  CONSTRAINT ck_pr_time CHECK (time_norm &gt;= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="users">
<h4>11. <code>users</code></h4>
<p>Учётные записи приложения. Пароль хранится не открытым текстом, а хешем с солью.</p>
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
<p>Заметки сотрудников. Внешний ключ связывает заметку с автором.</p>
<pre><code>CREATE TABLE notes (
  id INT NOT NULL AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  id_user INT NOT NULL,
  created_at DATE NOT NULL,
  PRIMARY KEY (id),
  KEY ix_notes_user (id_user),
  CONSTRAINT fk_notes_user
    FOREIGN KEY (id_user) REFERENCES users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
</div>
</div>

<figure class="diagram">
<img src="reports/screens/mysql/t2-tables.png" alt="Список таблиц базы dkip2027_course после выполнения CREATE TABLE">
<figcaption>Результат: в базе двенадцать таблиц. Проверьте список перед добавлением связей и данных.</figcaption>
</figure>

### Шаг 4. Постройте связи запросами

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

```sql
ALTER TABLE customer_order
  ADD CONSTRAINT fk_order_customer
  FOREIGN KEY (customer_id) REFERENCES counterparty(id),
  ADD CONSTRAINT fk_order_executor
  FOREIGN KEY (executor_id) REFERENCES counterparty(id);
```

<figure class="diagram">
<img src="reports/screens/mysql/t2-alter-sql.png" alt="Добавление внешних ключей запросом ALTER TABLE">
<figcaption>Связи запросом: два внешних ключа заказа добавляются одной командой `ALTER TABLE`.</figcaption>
</figure>

`ADD CONSTRAINT` добавляет правило с именем. Имя помогает понять, какое ограничение нарушено.

Ниже все четырнадцать связей модели. Если таблицы уже созданы с `FOREIGN KEY` внутри `CREATE TABLE`, повторно эти команды не выполняйте. Если создавали таблицы без внешних ключей, выполняйте команды по одной.

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

### Шаг 5. Вставьте данные запросами

<details class="hint">
<summary>Шпаргалка: INSERT</summary>

```sql
INSERT INTO имя_таблицы (поле1, поле2, поле3)
VALUES (значение1, значение2, значение3);
```

`INSERT INTO` выбирает таблицу. В скобках перечислены поля в порядке значений. `VALUES` начинает список. Текст и даты в кавычках, числа без кавычек. Строки разделяют запятыми, после последней запятой нет.

</details>

Сначала заказчики из JSON:

```sql
INSERT INTO counterparty (id, name, inn, address, phone, party_type) VALUES
('000000001', 'ООО "Поставка"', '', 'г. Пятигорск', '+79198634592', 'Поставщик'),
('000000002', 'ООО "Кинотеатр Квант"', '26320045123', 'г. Железноводск, ул. Мира, 123', '+79884581555', 'Покупатель'),
('000000008', 'ООО "Новый JDTO"', '26320045111', 'г. Железноводск', '+79884581555', 'Покупатель'),
('000000003', 'ООО "Ромашка"', '4140784214', 'г. Омск, ул. Строителей, 294', '+79882584546', 'Поставщик'),
('000000009', 'ООО "Ипподром"', '5874045632', 'г. Уфа, ул. Набережная, 37', '+79627486389', 'Поставщик'),
('000000010', 'ООО "Ассоль"', '2629011278', 'г. Калуга, ул. Пушкина, 94', '+79184572398', 'Покупатель');
```

ИП Томилин из заказа и изготовитель добавляются отдельно:

```sql
INSERT INTO counterparty (id, name, inn, address, phone, party_type) VALUES
('000000004', 'ИП Томилин Александр Сергеевич', '', 'г. Пятигорск', '', 'Покупатель'),
('M-001', 'ООО ТД "Вершина"', '', 'г. Пятигорск', '', 'Изготовитель');
```

<figure class="diagram">
<img src="reports/screens/mysql/t2-customers.png" alt="Таблица counterparty после вставки: заказчики и изготовитель">
<figcaption>Результат вставки: шесть записей JSON, ИП Томилин и изготовитель. Коды сохранили ведущие нули.</figcaption>
</figure>

### Шаг 6. Загрузите заказ, спецификацию и цены

Перед вставкой сопоставьте файлы и таблицы.

| Файл | Поля | Таблица |
|---|---|---|
| `Заказ покупателя.xlsx` | номер, дата, срок, код заказчика, изделие, количество, цена, скидка | `customer_order`, `customer_order_line` |
| `Спецификация.xlsx` | материал, операция, единица, норма, часы | `item`, `specification`, `specification_component` |
| `Цены.xlsx` | ресурс, цена | `price` |
| `Заказ на производство.xlsx` | заказ, дата запуска, изделие, расход | `production_order`, `production_product`, `production_resource` |

<figure class="diagram">
<img src="reports/screens/prep/V01_order_xlsx.png" alt="Заказ покупателя: шапка и строка продукции">
<figcaption>Заказ покупателя: номер, дата, срок, код заказчика, изделие, количество, цена и скидка.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/mysql/t2-order.png" alt="Шапка заказа V01-01 в таблице customer_order">
<figcaption>Результат: шапка заказа в `customer_order`.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/prep/V01_spec_xlsx.png" alt="Спецификация: материалы, операции и нормы">
<figcaption>Спецификация: строки материалов и операций с нормами и часами.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/mysql/t2-spec.png" alt="Состав спецификации в таблице specification_component">
<figcaption>Результат: состав в `specification_component`.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/prep/V01_prices_xlsx.png" alt="Цены: ресурс и цена">
<figcaption>Цены: ресурс и цена. Дата начала действия задана условием варианта.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/mysql/t2-price-table.png" alt="Таблица price после вставки цен">
<figcaption>Результат: цены в `price`, дата записана как `2026-04-01`.</figcaption>
</figure>

Данные из Excel вставляются тем же запросом `INSERT`. Сначала создайте изделие и ресурсы в `item`, затем цены, спецификацию, состав, заказ и строку заказа. Порядок важен: строка заказа ссылается на заказ и изделие, цена ссылается на ресурс.

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

INSERT INTO price (item_id, valid_from, amount) VALUES
(2, '2026-04-01', 3250.00),
(3, '2026-04-01', 95.00),
(4, '2026-04-01', 140.00),
(5, '2026-04-01', 595.00),
(6, '2026-04-01', 245.00),
(7, '2026-04-01', 1400.00),
(8, '2026-04-01', 450.00),
(9, '2026-04-01', 950.00);

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

INSERT INTO customer_order (id, doc_no, doc_date, customer_id, executor_id)
VALUES (1, 'V01-01', '2026-04-22', '000000004', 'M-001');

INSERT INTO customer_order_line (id, order_id, product_id, qty, sale_price, discount)
VALUES (1, 1, 1, 2, 14120.00, 1412.00);
```

Производственный заказ:

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

### Шаг 7. Сделайте выгрузку и восстановите её

Откройте базу `dkip2027_course`, вкладку `Экспорт`, выберите `Быстрый` и `SQL`. Сохраните файл как `dkip2027-mysql.sql`. Затем создайте пустую базу `dkip2027_restore`, откройте `Импорт`, выберите файл и загрузите его. Если таблицы и строки появились снова, выгрузка рабочая.

## Задание 3. SQL-запрос стоимости

Полный разбор запроса находится в методичке [Задание 3. SQL-запрос стоимости](04-task-3-sql.html). Здесь короткий маршрут V01.

### Как собрать запрос стоимости

<details class="hint">
<summary>Шпаргалка: SELECT, JOIN, GROUP BY, SUM и ROUND</summary>

```sql
SELECT o.doc_no, ROUND(SUM(...), 2) AS total_cost
FROM customer_order o
JOIN customer_order_line l ON l.order_id = o.id
JOIN price p ON p.item_id = l.product_id
WHERE o.doc_no = 'V01-01'
GROUP BY o.doc_no;
```

`SELECT` выбирает столбцы, `FROM` задаёт таблицу, `JOIN ... ON` соединяет по ключу, `WHERE` фильтрует строки, `GROUP BY` собирает их в группы, `SUM` складывает, `ROUND` округляет итог. `AS` задаёт имя столбца результата.

</details>

Запрос стоимости отвечает на вопрос «сколько стоит заказ по нормам и ценам». В V01 две единицы изделия, восемь строк состава и цены от 1 апреля 2026 года.

**`JOIN ... ON`.** Соедините строки заказа с шапкой по ключу `order_id`.

<details class="hint">
<summary>Шпаргалка: JOIN</summary>

```sql
JOIN customer_order_line l ON l.order_id = o.id
```

`JOIN` добавляет таблицу, `ON` задаёт условие. Внешний ключ дочерней таблицы сравнивается с первичным ключом родительской.

</details>

**`CASE`.** Для материала берите норму `c.qty`, для операции время `c.time_norm`:

```sql
CASE WHEN i.kind = 'operation' THEN c.time_norm ELSE c.qty END
```

**`GROUP BY` и `SUM`.** Соберите строки в группы по заказу и сложите количество.

<details class="hint">
<summary>Шпаргалка: GROUP BY и SUM</summary>

```sql
SELECT o.doc_no, SUM(l.qty) AS total_qty
FROM customer_order o
JOIN customer_order_line l ON l.order_id = o.id
GROUP BY o.doc_no;
```

`GROUP BY` собирает строки в одну на группу, `SUM` складывает значения внутри группы, `AS` задаёт имя результата.

</details>

**`WITH`.** Общее табличное выражение называет промежуточный результат. В расчёте стоимости так выбирают действующую цену на дату заказа.

<details class="hint">
<summary>Шпаргалка: WITH</summary>

```sql
WITH price_on_date AS (
  SELECT item_id, amount FROM price WHERE valid_from <= '2026-04-22'
)
SELECT * FROM price_on_date;
```

`WITH имя AS (...)` создаёт временный набор строк. Его используют, чтобы вынести выбор цены отдельно и не повторять подзапрос.

</details>

Итоговый запрос:

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
WHERE o.doc_no = 'V01-01'
GROUP BY o.doc_no;
```

<figure class="diagram">
<img src="reports/screens/mysql/t3-total.png" alt="Итоговая стоимость заказа V01-01: 14374.28">
<figcaption>Итог запроса: номер заказа и нормативная стоимость 14 374,28.</figcaption>
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
WHERE o.doc_no = 'V01-01'
ORDER BY i.kind, i.id;
```

<figure class="diagram">
<img src="reports/screens/mysql/t3-detail.png" alt="Восемь строк расчёта стоимости V01 с вкладом каждого ресурса">
<figcaption>Строки расчёта: материалы и операции с нормой, ценой и вкладом. Сумма равна 14 374,28.</figcaption>
</figure>

Материалы дают `9974.28`, операции `4400.00`, вместе `14374.28`. Если получилось другое число, проверьте восемь строк состава и цену на дату `2026-04-22`, а не подгоняйте запрос.

## Проверка варианта V01

| Файл | Что проверить |
|---|---|
| `V01_ER.drawio` | двенадцать таблиц, поля, первичные и внешние ключи |
| `V01_ER.pdf` | статичная диаграмма на одном листе |
| `V01_schema.sql` | двенадцать таблиц, `PRIMARY KEY`, `FOREIGN KEY`, `CHECK` |
| `V01_import.sql` | заказчики, ресурсы, спецификация, цены и производственный заказ |
| `V01_cost.sql` | запрос стоимости и результат `14374.28` |

Перед сдачей пройдите по каждому пункту. Если пункт не выполнен, вернитесь к шагу, а не к началу задания целиком. Так быстрее найти причину.

После проверки откройте [Задание 2. База данных и импорт](03-task-2-db.html) и [Задание 3. SQL-запрос стоимости](04-task-3-sql.html): там те же действия разобраны подробнее.

## Частые ошибки V01

**Код заказчика стал числом.** `000000004` превратился в `4`. Исправление: `VARCHAR(32)` и кавычки в `INSERT`.

**В JSON поле `addres`, в таблице `address`.** Имена не совпадают автоматически. Исправление: перечислить поля в `INSERT` явно.

**В заказе ИП Томилин, а в JSON его нет.** Добавьте его отдельной строкой. Не заменяйте заказчика на первого из JSON.

**Норма материала попала в `time_norm`.** Для материала заполняйте `qty`, для операции `time_norm`. Иначе запрос задания 3 умножит не то поле.

**Дата записана как `22.04.2026`.** MySQL ждёт `2026-04-22`.

**Цена взята самая новая.** Добавьте условие `p2.valid_from <= o.doc_date`, иначе будущая цена изменит итог.

**В расчёт попала продажная цена.** `sale_price` и `discount` не участвуют в нормативной стоимости.

## Чек-лист перед сдачей

- База `dkip2027_course` создана в `utf8mb4_unicode_ci`.
- Все двенадцать таблиц используют `InnoDB`.
- У каждой таблицы есть первичный ключ.
- Внешние ключи созданы и проверены запросом.
- Коды заказчиков хранятся текстом.
- Загружены шесть записей JSON, ИП Томилин и изготовитель.
- Заказ, спецификация, состав, цены и производственный заказ загружены.
- Даты записаны в формате `ГГГГ-ММ-ДД`.
- Проверка с несуществующим заказчиком даёт ошибку 1452.
- Выгрузка содержит структуру и данные.
- База восстановлена в пустую копию.
- Итог задания 3 равен `14374.28`.
- Скриншоты показывают источник данных, таблицу и результат запроса.
