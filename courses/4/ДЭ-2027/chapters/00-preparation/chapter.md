---
title: Предварительная подготовка
dek: Три тестовых варианта, разбор первых трёх заданий в draw.io и sqliteonline, а также вариант V02 на установленных XAMPP и phpMyAdmin.
chapter: "Подготовка"
level: СПО
glyph: "00"
outcomes:
  - Строить ER-диаграмму в draw.io и сохранять её в PDF
  - Создавать таблицы и импортировать JSON в sqliteonline.com
  - Считать стоимость заказа запросом с JOIN и агрегацией
  - Выполнять задания 1-3 в XAMPP и phpMyAdmin на варианте V02
---

## Зачем этот раздел

Первые три задания проверяют модель данных, базу и расчёт. Их можно пройти без установки сервера: диаграмма собирается в draw.io, база и запросы выполняются в sqliteonline.com. Оба инструмента работают в браузере, поэтому подготовка не зависит от прав администратора и настроек учебного компьютера.

Если на компьютере установлены XAMPP, Visual Studio 2022 и Postman, те же задания выполняются в приложениях. В конце раздела добавлен вариант V02 «Пекарня Колос»: ER-диаграмма, база в XAMPP, импорт документов, выгрузка, восстановление и SQL-запрос стоимости с пошаговыми скриншотами.

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

### Что требуется

Нарисовать ER-диаграмму предприятия по документам варианта и сохранить её в PDF. На диаграмме должны быть таблицы, поля, первичные и внешние ключи, связи и кратность. Модель приводится к третьей нормальной форме.

Сдаются два файла: PDF с диаграммой и исходник `.drawio`. PDF проверяют на экране и на печати, исходник нужен, чтобы показать, что схема собрана в редакторе, а не нарисована картинкой.

В базовом наборе получается двенадцать таблиц и четырнадцать связей. В варианте другое предприятие, другая продукция и другие ресурсы, но набор сущностей тот же: контрагенты, ресурсы, цены, спецификация, состав, заказ покупателя, производственный заказ, пользователи и заметки.

### Сначала разберите исходные данные

До открытия draw.io прочитайте файлы варианта и выпишите факты. Диаграмма начинается не с прямоугольников, а с ответов на вопросы о системе.

| Файл | Что внутри | Что из него берут |
|---|---|---|
| `V01_customers.json` | заказчики: код, название, ИНН, адрес, телефон, тип | таблица `counterparty` |
| `V01_resources.csv` | ресурсы: название, вид, единица, норма, время, цена | таблицы `item`, `price`, `specification_component` |
| описание варианта | предприятие, продукция, количество, правила расчёта | `specification`, `customer_order`, `production_order` |

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

В CSV есть материалы и операции. У них разные единицы, но общая структура: код, название, вид, единица. Если сделать отдельные таблицы `material` и `operation`, появятся две почти одинаковые сущности и два внешних ключа в составе. Проще один справочник с полем `kind`.

| Поле | Тип | Ключ | Зачем |
|---|---|---|---|
| `id` | INTEGER | PK | внутренний код ресурса |
| `code` | TEXT |  | код из документа |
| `name` | TEXT |  | название материала или операции |
| `kind` | TEXT |  | `product`, `material` или `operation` |
| `unit` | TEXT |  | метр, штука, час |

<a href="reports/screens/prep/drawio-table-02.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-table-02.png" alt="Таблица item с видом ресурса и единицей измерения"></a>
<figcaption>Справочник `item`. Поле `kind` отличает продукцию, материал и операцию, не создавая три таблицы.</figcaption>

Ход мысли: «Что общего у ткани и раскроя? Оба расходуются в спецификации. Чем отличаются? Единицей и способом расчёта. Значит, общее выносим в справочник, различие в поле вида».

### Шаг 4. Таблица `price`: цена меняется во времени

Цена не принадлежит товару навсегда: с 1 марта одна, с 1 апреля другая. Если хранить цену в `item`, история потеряется. Появляется отдельная сущность с составным ключом: ресурс плюс дата, с которой цена действует.

| Поле | Тип | Ключ | Зачем |
|---|---|---|---|
| `item_id` | INTEGER | PK, FK | ссылка на ресурс |
| `valid_from` | TEXT | PK | дата начала действия цены |
| `amount` | REAL |  | цена за единицу |

<a href="reports/screens/prep/drawio-table-03.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-table-03.png" alt="Таблица price с составным ключом из ресурса и даты"></a>
<figcaption>`price` хранит историю цен. Один ресурс может иметь несколько строк с разными датами.</figcaption>

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

<a href="reports/screens/prep/drawio-table-04.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-table-04.png" alt="Таблица specification с ссылкой на изделие и изготовителя"></a>
<figcaption>`specification` это шапка: изделие, выпуск и изготовитель. Строки состава появятся отдельно.</figcaption>

Почему `product_id` отдельно, а не название изделия? Название уже есть в `item`. Повторять его в спецификации значит хранить две версии одного факта.

### Шаг 6. Таблица `specification_component`: строки состава

В одной спецификации много материалов и операций. Это типичная связь многие ко многим, её нельзя оставить двумя стрелками. Появляется промежуточная таблица, где каждая строка это один ресурс в составе.

| Поле | Тип | Ключ | Зачем |
|---|---|---|---|
| `specification_id` | INTEGER | PK, FK | ссылка на шапку |
| `item_id` | INTEGER | PK, FK | ссылка на ресурс |
| `qty` | REAL |  | норма расхода на единицу |
| `time_norm` | REAL |  | часы для операции, `1` для материала |

<a href="reports/screens/prep/drawio-table-05.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-table-05.png" alt="Таблица specification_component со ссылками на спецификацию и ресурс"></a>
<figcaption>`specification_component` связывает спецификацию и ресурс. Здесь хранятся норма и время.</figcaption>

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

<a href="reports/screens/prep/drawio-table-06.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-table-06.png" alt="Шапка customer_order с заказчиком и исполнителем"></a>
<figcaption>`customer_order` хранит шапку. Два внешних ключа ведут в `counterparty`.</figcaption>

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

<a href="reports/screens/prep/drawio-table-07.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-table-07.png" alt="Строки customer_order_line со ссылками на заказ и изделие"></a>
<figcaption>`customer_order_line` хранит по одной строке на изделие. Шапка и строки связаны `1:N`.</figcaption>

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

<a href="reports/screens/prep/drawio-table-08.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-table-08.png" alt="Шапка production_order с датой запуска и подразделением"></a>
<figcaption>`production_order` описывает запуск выпуска. Это отдельная шапка, не часть заказа покупателя.</figcaption>

### Шаг 10. Таблица `production_product`: что выпускаем

В производственном заказе может быть несколько изделий. Появляется таблица продукции к выпуску с количеством.

| Поле | Тип | Ключ | Зачем |
|---|---|---|---|
| `production_id` | INTEGER | PK, FK | ссылка на производственный заказ |
| `product_id` | INTEGER | PK, FK | ссылка на изделие |
| `qty` | INTEGER |  | сколько выпустить |

<a href="reports/screens/prep/drawio-table-09.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-table-09.png" alt="Таблица production_product с составным ключом"></a>
<figcaption>`production_product` связывает производственный заказ и изделие, хранит количество.</figcaption>

### Шаг 11. Таблица `production_resource`: плановый расход

Для производства нужно знать, сколько материалов и часов потребуется. Это отдельная таблица, потому что расход относится к производственному заказу, а не к заказу покупателя.

| Поле | Тип | Ключ | Зачем |
|---|---|---|---|
| `production_id` | INTEGER | PK, FK | ссылка на производственный заказ |
| `item_id` | INTEGER | PK, FK | ссылка на ресурс |
| `qty` | REAL |  | плановое количество |
| `time_norm` | REAL |  | плановые часы |

<a href="reports/screens/prep/drawio-table-10.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-table-10.png" alt="Таблица production_resource с плановым расходом ресурсов"></a>
<figcaption>`production_resource` хранит план расхода. Ключ составной: заказ плюс ресурс.</figcaption>

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

<a href="reports/screens/prep/drawio-table-11.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-table-11.png" alt="Таблица users с логином, ролью и блокировкой"></a>
<figcaption>`users` хранит учётные записи приложения. Пароль хранится хешем, а не открытым текстом.</figcaption>

### Шаг 13. Таблица `notes`: заметки сотрудников

Заметка принадлежит пользователю. Она не входит в заказ и не влияет на стоимость, но нужна приложению. Появляется последняя таблица с внешним ключом на `users`.

| Поле | Тип | Ключ | Зачем |
|---|---|---|---|
| `id` | INTEGER | PK | номер заметки |
| `title` | TEXT |  | заголовок |
| `content` | TEXT |  | текст |
| `id_user` | INTEGER | FK | автор |
| `created_at` | TEXT |  | дата создания |

<a href="reports/screens/prep/drawio-table-12.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-table-12.png" alt="Таблица notes со ссылкой на пользователя"></a>
<figcaption>`notes` связана с `users` как один ко многим: у пользователя много заметок.</figcaption>

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
2. На рабочем столе создайте личную папку по образцу `/Студент/Название предмета/ФИО студента/номер практической работы`.
3. Назовите файл `V01_ER.drawio` и сохраните.
4. Откройте `Файл`, затем `Экспорт как`, затем `PDF`.
5. Оставьте экспорт всей диаграммы, а не выделения. Проверьте, что все двенадцать таблиц попали на лист.
6. Откройте PDF и увеличьте масштаб: подписи должны читаться без догадок.

<a href="reports/screens/prep/drawio-save-menu.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-save-menu.png" alt="Меню Файл в draw.io с командами сохранения и экспорта"></a>
<figcaption>Меню `Файл`: здесь находятся `Сохранить как` и `Экспорт как`. Сначала сохраните `.drawio`, затем экспортируйте PDF.</figcaption>

<a href="reports/screens/prep/drawio-export.png" target="_blank" rel="noopener"><img src="reports/screens/prep/drawio-export.png" alt="Диалог экспорта PDF в draw.io"></a>
<figcaption>Экспорт PDF. Не выбирайте «Только выделение», иначе на листе останется одна таблица.</figcaption>

Перед сдачей проверьте: двенадцать таблиц, у каждой первичный ключ, четырнадцать подписанных связей, нет вычисляемых полей. Если таблиц девять, скорее всего шапка заказа слита со строками. Если пятнадцать, появилась лишняя таблица под каждую строку документа.


## Задание 2. База в sqliteonline.com

### Шаг 1. Откройте sqliteonline.com

Откройте `sqliteonline.com` и выберите SQLite. Слева появится список таблиц демонстрационной базы, сверху кнопки `Import` и `Export`, в центре редактор SQL, снизу результат.

<a href="reports/screens/prep/sqlite-start.png" target="_blank" rel="noopener"><img src="reports/screens/prep/sqlite-start.png" alt="sqliteonline.com: список таблиц, редактор SQL и кнопка Run"></a>
<figcaption>sqliteonline.com. Слева база, в центре редактор, сверху запуск и импорт, снизу таблица результата.</figcaption>

Демонстрационная таблица `demo` не мешает: свои таблицы создаются рядом. Перед работой закройте зелёное уведомление, чтобы оно не закрывало результат.

### Что такое база данных простыми словами

**База данных** это набор таблиц, которые хранят факты о системе. **Таблица** описывает один тип факта: контрагента, заказ, цену. **Строка** это один факт, например один заказ. **Столбец** это свойство факта, например дата заказа.

**Первичный ключ** отличает строки внутри таблицы. **Внешний ключ** ссылается на первичный ключ другой таблицы. **Ограничение** (`CHECK`, `NOT NULL`, `UNIQUE`) запрещает записывать данные, которые нарушают правило. **Скрипт** это текст команд, который можно выполнить целиком и повторить на другом компьютере.

В sqliteonline.com база живёт в памяти браузера, пока открыта страница. Чтобы результат не потерялся, скрипт сохраняют в файл `.sql`, а таблицу результата выгружают через `Export`.

### Шаг 2. Создайте рабочую базу

1. Откройте `sqliteonline.com`.
2. В левой панели нажмите `Private DB +` или откройте `SQLite`, затем `Create SQLite DB`. Назовите базу `v01_sklad`.
3. Если создать отдельную базу нельзя, работайте в `Demo.Memory`: таблицы появятся рядом с `demo`, результат всё равно можно выгрузить.
4. Верхние кнопки `Import` и `Export` служат для загрузки файлов и сохранения результата. `Import` принимает SQL, CSV и JSON, `Export` выгружает таблицу или базу.

<a href="reports/screens/prep/sqlite-export.png" target="_blank" rel="noopener"><img src="reports/screens/prep/sqlite-export.png" alt="Диалог Export в sqliteonline.com с выбором формата выгрузки"></a>
<figcaption>Кнопка `Export` открывает выбор формата. Перед выгрузкой выберите таблицу или результат запроса, который нужно сохранить.</figcaption>

Не закрывайте вкладку до сохранения скрипта: память браузера очищается вместе с сессией.

### Как читать SQL

SQL читается сверху вниз, но выполняется не в том порядке, в котором записан. Сначала база находит таблицы в `FROM`, соединяет их в `JOIN`, отбирает строки в `WHERE`, собирает группы в `GROUP BY`, считает агрегаты в `SELECT` и только потом сортирует результат.

| Команда | Что делает | Пример |
|---|---|---|
| `SELECT` | выбирает столбцы результата | `SELECT doc_no, doc_date FROM customer_order;` |
| `FROM` | указывает таблицу | `FROM customer_order` |
| `WHERE` | отбирает строки до группировки | `WHERE doc_date >= '2027-03-01'` |
| `ORDER BY` | сортирует результат | `ORDER BY doc_no` |
| `JOIN ... ON` | соединяет строки по ключу | `JOIN customer_order_line l ON l.order_id = o.id` |
| `GROUP BY` | собирает строки в группы | `GROUP BY o.doc_no` |
| `SUM` | складывает значения группы | `SUM(l.qty)` |
| `ROUND` | округляет число | `ROUND(total, 2)` |
| `WITH` | называет промежуточный запрос | `WITH price_on_date AS (...)` |

Схема для примеров:

```text
counterparty(id, name, party_type)
item(id, name, kind, unit)
price(item_id, valid_from, amount)
specification(id, product_id, output_qty)
specification_component(specification_id, item_id, qty, time_norm)
customer_order(id, doc_no, doc_date, customer_id, executor_id)
customer_order_line(id, order_id, product_id, qty, sale_price)
```

Простые запросы:

```sql
-- все строки таблицы
SELECT * FROM counterparty;

-- только нужные столбцы
SELECT doc_no, doc_date FROM customer_order;

-- фильтр по дате
SELECT doc_no FROM customer_order WHERE doc_date >= '2027-03-01';

-- соединение заказа и строк
SELECT o.doc_no, l.qty
FROM customer_order o
JOIN customer_order_line l ON l.order_id = o.id;
```

`o` и `l` это псевдонимы таблиц. Они сокращают запись и позволяют обращаться к полям двух таблиц без путаницы: `o.doc_no`, `l.qty`. Если убрать псевдонимы, придётся писать полные имена таблиц в каждом столбце.

`SELECT *` удобен для первого знакомства, но в отчёт его не ставят: он выводит лишние столбцы и ломается при изменении схемы. Перечисляйте поля явно.

### Шаг 3. Создайте таблицы

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

<a href="reports/screens/prep/sqlite-schema.png" target="_blank" rel="noopener"><img src="reports/screens/prep/sqlite-schema.png" alt="Список созданных таблиц в sqliteonline.com: все двенадцать, включая item"></a>
<figcaption>Схема создана. Слева двенадцать таблиц, в результате проверочный список имён.</figcaption>

Составной ключ записывается двумя строками `PK` или одной строкой `PRIMARY KEY (item_id, valid_from)` в конце таблицы. Внешний ключ всегда ссылается на первичный ключ другой таблицы.

### Шаг 4. Импортируйте JSON

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

### Шаг 5. Проверьте данные и ограничения

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

### Шаг 6. Сохраните скрипты

Скачайте готовые файлы и сохраните их в папку занятия:

- [Схема V01, SQL](reports/prep/sql/V01_schema.sql)
- [Импорт JSON V01, SQL](reports/prep/sql/V01_import.sql)
- [Расчёт стоимости V01, SQL](reports/prep/sql/V01_cost.sql)

В sqliteonline.com скрипт можно хранить в истории запросов, но на защите нужен файл. История браузера не считается артефактом.

## Задание 3. Стоимость заказа

### Как собрать запрос стоимости

Запрос стоимости отвечает на вопрос «сколько стоит заказ по нормам и ценам». Он не берёт продажную цену из строки заказа: та включает наценку и скидку, а нормативная стоимость считается по спецификации.

Понадобятся пять таблиц:

```text
customer_order(id, doc_no, doc_date)
customer_order_line(id, order_id, product_id, qty)
specification(id, product_id, output_qty)
specification_component(specification_id, item_id, qty, time_norm)
price(item_id, valid_from, amount)
```

Сначала разберите каждую команду отдельно.

**`SELECT` и `FROM`.** Выберите нужные столбцы и таблицу. Звёздочку не используйте: в отчёт идут только номер заказа и итог.

```sql
SELECT doc_no, doc_date FROM customer_order;
```

**`WHERE`.** Отберите строки до группировки. Например, только заказы за март.

```sql
SELECT doc_no FROM customer_order WHERE doc_date >= '2027-03-01';
```

**`JOIN ... ON`.** Соедините строки заказа с шапкой по ключу `order_id`.

```sql
SELECT o.doc_no, l.product_id, l.qty
FROM customer_order o
JOIN customer_order_line l ON l.order_id = o.id;
```

**`GROUP BY` и `SUM`.** Соберите строки в группы по заказу и сложите количество.

```sql
SELECT o.doc_no, SUM(l.qty) AS total_qty
FROM customer_order o
JOIN customer_order_line l ON l.order_id = o.id
GROUP BY o.doc_no;
```

**`ROUND`.** Округляйте один раз, после суммы. Если округлить каждую строку, итог разойдётся с проверкой.

```sql
SELECT ROUND(SUM(l.qty * 640.0), 2) AS total_cost
FROM customer_order_line l
WHERE l.order_id = 1;
```

**`WITH`.** Общее табличное выражение называет промежуточный результат. В расчёте стоимости так выбирают действующую цену на дату заказа.

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
SELECT item_id, amount FROM price_on_date;
```

Почему нельзя соединить `price` и `specification_component` напрямую? У одного ресурса несколько цен, у одной спецификации несколько строк. Прямое соединение размножит строки: каждая строка состава получит каждую цену. Сначала оставьте одну действующую цену на ресурс, потом соединяйте.

Формула читается так:

```text
количество в заказе / выпуск по спецификации × норма × коэффициент времени × цена
```

Для материала `time_norm` равно `1`, для операции это часы. Поэтому одна формула считает и материалы, и операции.

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

<a href="reports/screens/prep/sqlite-query.png" target="_blank" rel="noopener"><img src="reports/screens/prep/sqlite-query.png" alt="Начало запроса стоимости заказа и результат 7680"></a>
<figcaption>Запрос с общим табличным выражением. В результате одна строка V01-01 со стоимостью 7680.</figcaption>

Если соединить `price` и `specification_component` без подготовки, строки начнут размножаться: каждая строка состава получит несколько цен. Общее табличное выражение `price_on_date` оставляет одну действующую цену на ресурс.

### Шаг 3. Проверьте результат

<a href="reports/screens/prep/sqlite-cost.png" target="_blank" rel="noopener"><img src="reports/screens/prep/sqlite-cost.png" alt="Итоговая стоимость заказа V01-01: 7680"></a>
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

## Вариант V02: задания 1-3 на установленных приложениях

На компьютерах появились XAMPP, Visual Studio 2022 и Postman. Ниже разобран второй вариант, пекарня «Колос», на тех же инструментах: XAMPP и phpMyAdmin для базы, SQL для расчёта. Приложение и Postman понадобятся в заданиях 4-6, но подготовка базы для них уже начинается здесь.

В варианте другие данные, структура документов та же. Шесть заказчиков, изделие «Хлеб ржаной 500 г», три материала, две операции, цены с 01.03.2027, заказ V02-01 на 40 единиц и производственный заказ V02-P01. Коды заказчиков начинаются с `002`, поэтому их нельзя хранить целыми числами.

### Задание 1. ER-модель пекарни

Сначала выпишите документы и повторяющиеся строки. Заказ покупателя содержит шапку и строку с изделием. Спецификация содержит шапку и строки материалов и операций. Цены это история по ресурсу и дате. Производственный заказ содержит изделие к выпуску и плановый расход ресурсов.

Получается десять таблиц:

| Таблица | Первичный ключ | Внешние ключи | Что хранит |
|---|---|---|---|
| `counterparty` | `id` | нет | заказчиков и изготовителя |
| `item` | `id` | нет | изделие, материалы и операции |
| `price` | `item_id`, `valid_from` | `item_id` | историю цен ресурса |
| `specification` | `id` | `product_id`, `manufacturer_id` | шапку спецификации |
| `specification_component` | `specification_id`, `item_id` | `specification_id`, `item_id` | нормы материалов и часы операций |
| `customer_order` | `id` | `customer_id`, `executor_id` | шапку заказа |
| `customer_order_line` | `id` | `order_id`, `product_id` | строку заказа |
| `production_order` | `id` | `order_id` | шапку производственного заказа |
| `production_product` | `production_id`, `product_id` | `production_id`, `product_id` | изделие к выпуску |
| `production_resource` | `production_id`, `item_id` | `production_id`, `item_id` | плановый расход ресурсов |

Третья нормальная форма проверяется по трём вопросам. В ячейке нет списка значений. Неключевое поле зависит от всего составного ключа, а не от его части. Неключевое поле не зависит от другого неключевого поля.

Нормы материалов и часы операций хранятся в `specification_component`, а не в `item`: один и тот же ресурс входит в разные изделия с разной нормой. Цена хранится в `price` с датой начала действия, а не в `item`: у ресурса может быть несколько цен за разные периоды. Стоимость заказа и сумма строки не хранятся: они считаются запросом. Код изготовителя `V02-MAKER` добавлен отдельно, потому что в Excel есть название пекарни, но нет её кода.

<figure class="diagram">
<img src="reports/v02/er-v02.png" alt="ER-диаграмма V02: десять таблиц пекарни и их связи">
<figcaption>ER-диаграмма V02: десять таблиц, составные ключи и связи 1:N. Изготовитель хранится в counterparty с кодом V02-MAKER.</figcaption>
</figure>

Скачать схему в PDF: [er-v02.pdf](reports/v02/er-v02.pdf). В PDF та же диаграмма на листе A3, удобно приложить к отчёту.

### Задание 2. База данных и загрузка документов

**Шаг 1. Запустите XAMPP.** Откройте XAMPP Control Panel и нажмите `Start` у Apache и MySQL. На учебных компьютерах Apache слушает порт `4433`, MySQL слушает `3306`. Если Apache не запускается, проверьте, какая программа заняла `4433`, командой `netstat -ano | findstr :4433`.

<figure class="diagram">
<img src="reports/screens/v02/00-xampp.png" alt="XAMPP Control Panel: Apache на порту 4433, MySQL на порту 3306">
<figcaption>XAMPP Control Panel: Apache и MySQL запущены, Apache занимает 4433, MySQL занимает 3306.</figcaption>
</figure>

**Шаг 2. Откройте phpMyAdmin.** Перейдите по адресу `http://localhost:4433/phpmyadmin`. В учебной сборке пользователь `root`, пароль пустой. Слева виден список баз, сверху вкладки `Structure`, `SQL`, `Export`, `Import`.

**Шаг 3. Создайте базу.** Нажмите `New` или откройте вкладку `Databases`. В поле имени введите `dkip2027_v02`, выберите сравнение `utf8mb4_unicode_ci` и нажмите `Create`. Кодировка важна: в именах есть кириллица и кавычки «».

<figure class="diagram">
<img src="reports/screens/v02/01-databases.png" alt="Создание базы dkip2027_v02 в phpMyAdmin">
<figcaption>Создание базы: имя dkip2027_v02, сравнение utf8mb4_unicode_ci. Ниже база уже появилась в списке.</figcaption>
</figure>

**Шаг 4. Выполните схему.** Откройте базу, вкладку `SQL`, вставьте скрипт [schema.sql](reports/v02/schema.sql) и нажмите `Go`. Скрипт создаёт десять таблиц в порядке от справочников к зависимым.

<figure class="diagram">
<img src="reports/screens/v02/06-schema-sql.png" alt="Скрипт схемы V02 во вкладке SQL">
<figcaption>Скрипт схемы во вкладке SQL: база, кодировка и создание первой таблицы counterparty.</figcaption>
</figure>

Разбор ключевых решений схемы:

- `counterparty.id` это `VARCHAR(32)`, потому что код `002000001` должен сохранить ведущие нули. Для изготовителя используется `V02-MAKER`.
- `item.kind` принимает только `product`, `material` или `operation`. Проверка `CHECK` не даст записать опечатку.
- `price` имеет составной ключ `(item_id, valid_from)`: у одного ресурса одна цена на дату, но история цен сохраняется.
- `specification.product_id` объявлен `UNIQUE`: у изделия одна действующая спецификация, это связь один к одному.
- `specification_component` имеет составной ключ `(specification_id, item_id)`: один ресурс входит в спецификацию один раз. Для материалов заполняется `qty`, для операций `time_norm`, а `qty` остаётся равным единице.
- `customer_order` содержит два внешних ключа в `counterparty`: заказчик и исполнитель. Это разные роли одной таблицы.
- `production_resource` хранит плановый расход, а не норматив на единицу. Плановые значения уже умножены на 40.

**Шаг 5. Проверьте таблицы.** Обновите левую панель. В базе должно быть десять таблиц, все `InnoDB`, сравнение `utf8mb4_unicode_ci`. Проверить это можно запросом:

```sql
SELECT table_name, engine, table_collation
FROM information_schema.tables
WHERE table_schema = 'dkip2027_v02'
ORDER BY table_name;
```

<figure class="diagram">
<img src="reports/screens/v02/02-tables.png" alt="Список десяти таблиц базы dkip2027_v02">
<figcaption>Список таблиц: десять объектов InnoDB, у каждой видно число строк. Служебных таблиц в базе нет.</figcaption>
</figure>

**Шаг 6. Загрузите заказчиков из JSON.** В файле `Заказчики.json` шесть записей. Поле `addres` переименовывается в `address`, `type` в `party_type`. Пустой ИНН допустим, поэтому `inn` имеет `DEFAULT ''`. Коды загружаются текстом, ведущие нули сохраняются.

На стенде удобно выполнить [data.sql](reports/v02/data.sql): он содержит те же шесть записей и служебную запись изготовителя. При импорте через phpMyAdmin выберите таблицу `counterparty`, вкладку `Import`, формат CSV или SQL и проверьте кодировку `utf-8`. Не выбирайте базу целиком: CSV вставляется в таблицу, а не в базу.

<figure class="diagram">
<img src="reports/screens/v02/04-counterparty.png" alt="Таблица counterparty: шесть заказчиков и изготовитель, коды с ведущими нулями">
<figcaption>Таблица counterparty: шесть заказчиков с кодами 002000001…002000006 и изготовитель V02-MAKER. Ведущие нули и кириллица сохранены.</figcaption>
</figure>

**Шаг 7. Загрузите заказ, спецификацию и цены.** Из Excel переносятся шапка заказа, строка заказа, шапка спецификации, пять строк состава и пять цен. Даты записываются в формате `2027-03-15`. Количество 40 хранится в строке заказа, нормы 0,32 и 0,08 в составе, часы 0,04 и 0,02 в поле `time_norm`.

<figure class="diagram">
<img src="reports/screens/v02/10-order.png" alt="Заказ V02-01: дата, срок, заказчик и изготовитель">
<figcaption>Шапка заказа V02-01: дата 15.03.2027, срок 22.03.2027, заказчик 002000001, изготовитель V02-MAKER.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/v02/11-spec-component.png" alt="Состав спецификации: материалы и операции с нормами и часами">
<figcaption>Состав спецификации: у материалов заполнено qty, у операций time_norm. Нормы даны на одну буханку.</figcaption>
</figure>

**Шаг 8. Проверьте ключи.** Откройте `price`, вкладку `Structure`. Оба поля `item_id` и `valid_from` помечены ключом, ниже объявлен внешний ключ на `item.id`. Для `specification_component` проверьте составной ключ и два внешних ключа. Запрос к `information_schema` покажет все связи:

```sql
SELECT table_name, constraint_name, referenced_table_name
FROM information_schema.KEY_COLUMN_USAGE
WHERE table_schema = 'dkip2027_v02'
  AND referenced_table_name IS NOT NULL
ORDER BY table_name, constraint_name;
```

<figure class="diagram">
<img src="reports/screens/v02/03-price-structure.png" alt="Структура price: составной первичный ключ item_id и valid_from">
<figcaption>Структура price: item_id и valid_from образуют составной первичный ключ, amount хранится в DECIMAL(14,2).</figcaption>
</figure>

**Шаг 9. Сделайте выгрузку и восстановите её.** Откройте вкладку `Export`, выберите быстрый метод и формат SQL, нажмите `Export`. Получится файл [v02-export.sql](reports/v02/v02-export.sql). Создайте пустую базу `dkip2027_v02_restore`, откройте её вкладку `Import`, загрузите файл и выполните. Проверьте число таблиц и строк, а не только сообщение об успехе.

<figure class="diagram">
<img src="reports/screens/v02/08-export.png" alt="Экспорт базы dkip2027_v02 в SQL">
<figcaption>Экспорт базы: быстрый метод, формат SQL, структура и данные всех десяти таблиц.</figcaption>
</figure>

<figure class="diagram">
<img src="reports/screens/v02/09-restore.png" alt="Восстановленная база dkip2027_v02_restore: десять таблиц">
<figcaption>Восстановленная база dkip2027_v02_restore: те же десять таблиц и то же число строк, что в исходной базе.</figcaption>
</figure>

### Задание 3. Нормативная стоимость заказа

Стоимость считается по правилам варианта. Материалы: количество выпуска × норма расхода × цена. Операции: количество выпуска × часы × тариф за час. Цена берётся действующая на дату заказа, то есть последняя с `valid_from` не позже 15.03.2027. Промежуточные суммы не округляются, итог округляется до копеек.

Запрос [cost-query.sql](reports/v02/cost-query.sql) состоит из трёх частей. `o` выбирает строку заказа V02-01. `p` находит последнюю цену каждого ресурса на дату заказа. `calc` соединяет заказ, спецификацию, состав, ресурс и цену и считает сумму строки. Внешний `SELECT` добавляет строку `Итого`.

```sql
WITH o AS (
  SELECT co.id AS order_id, co.doc_date, col.product_id, col.qty
  FROM customer_order co
  JOIN customer_order_line col ON col.order_id = co.id
  WHERE co.doc_no = 'V02-01'
),
p AS (
  SELECT pr.item_id, pr.amount
  FROM price pr
  JOIN (
    SELECT item_id, MAX(valid_from) AS vf
    FROM price
    WHERE valid_from <= (SELECT doc_date FROM o)
    GROUP BY item_id
  ) last ON last.item_id = pr.item_id AND last.vf = pr.valid_from
),
calc AS (
  SELECT
    CASE i.kind WHEN 'material' THEN 'Материал' ELSE 'Операция' END AS section,
    i.name,
    o.qty AS product_qty,
    CASE i.kind WHEN 'material' THEN sc.qty ELSE sc.time_norm END AS norm,
    p.amount AS price,
    o.qty * CASE i.kind WHEN 'material' THEN sc.qty ELSE sc.time_norm END * p.amount AS amount
  FROM o
  JOIN specification s ON s.product_id = o.product_id
  JOIN specification_component sc ON sc.specification_id = s.id
  JOIN item i ON i.id = sc.item_id
  JOIN p ON p.item_id = i.id
)
SELECT section, name, product_qty, norm, price, ROUND(amount, 2) AS amount
FROM (
  SELECT section, name, product_qty, norm, price, amount,
         CASE section WHEN 'Материал' THEN 1 ELSE 2 END AS sort
  FROM calc
  UNION ALL
  SELECT 'Итого', '', NULL, NULL, NULL, ROUND(SUM(amount), 2), 3
  FROM calc
) t
ORDER BY sort, name;
```

<figure class="diagram">
<img src="reports/screens/v02/07-cost-result.png" alt="Результат запроса стоимости V02-01: материалы, операции и итог 2672.00">
<figcaption>Результат запроса: три материала, две операции и итог 2672.00. Строки не удвоены, цена взята одна.</figcaption>
</figure>

Проверка вручную:

| Строка | Расчёт | Сумма |
|---|---|---|
| Мука ржаная | 40 × 0,32 × 65 | 832,00 |
| Закваска | 40 × 0,08 × 100 | 320,00 |
| Пакет | 40 × 1 × 4 | 160,00 |
| Замес и формование | 40 × 0,04 × 500 | 800,00 |
| Выпечка | 40 × 0,02 × 700 | 560,00 |
| Материалы | 832 + 320 + 160 | 1312,00 |
| Операции | 800 + 560 | 1360,00 |
| Итого | 1312 + 1360 | 2672,00 |

Если итог отличается, проверьте три места. Норма материалов должна быть 0,32 и 0,08, а не 12,8 и 3,2: плановый расход на 40 единиц хранится в `production_resource`, а в составе остаётся норма на одну буханку. Для операций используется `time_norm`, а `qty` равно единице. Цена должна быть одна, иначе соединение с `price` размножит строки.

### Что сдать по варианту V02

- ER-диаграмму в PDF и исходник схемы.
- `schema.sql`, `data.sql`, `v02-export.sql` и запрос `cost-query.sql`.
- Скриншоты списка таблиц, состава, заказчиков и результата запроса.
- Короткий протокол: действие, команда, ожидаемый и фактический результат.

<div class="files"><b class="label">Файлы варианта V02</b>
<a href="reports/v02/er-v02.pdf">ER-диаграмма · PDF</a>
<a href="reports/v02/schema.sql">Схема базы · SQL</a>
<a href="reports/v02/data.sql">Данные варианта · SQL</a>
<a href="reports/v02/cost-query.sql">Запрос стоимости · SQL</a>
<a href="reports/v02/v02-export.sql">Выгрузка базы · SQL</a>
</div>
