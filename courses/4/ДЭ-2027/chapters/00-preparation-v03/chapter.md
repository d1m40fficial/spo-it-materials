---
title: "Предварительная подготовка: вариант V03"
dek: "Керамическая мастерская «Глина»: ER-диаграмма на русском языке, таблицы и связи, импорт данных и SQL-запрос нормативной стоимости."
chapter: "Подготовка V03"
level: СПО
glyph: "00C"
outcomes:
  - Строить ER-диаграмму V03 с русскими названиями таблиц и атрибутов
  - Создавать таблицы, связи и импортировать данные V03
  - Считать нормативную стоимость заказа V03-01 запросом с JOIN и агрегацией
---

## Чем V03 отличается от V01 и V02

V03 это керамическая мастерская «Глина». Она выпускает «Кружку 300 мл» по спецификации, а магазин «Глина-1» заказал 18 единиц к сроку 22.03.2027. В модели те же двенадцать сущностей, что и в предыдущих вариантах, но все таблицы и атрибуты названы по-русски: `Заказчики`, `Цены`, `Телефон`, `Адрес`, `КоличествоВыпуска`. Так диаграмму можно читать без расшифровки, а SQL показывает, что русские имена работают в MySQL, если заключать их в обратные кавычки.

| Файл | Что внутри | Что из него берут |
|---|---|---|
| `Заказчики.json` | шесть покупателей: код, название, ИНН, адрес, телефон, тип | таблица `Заказчики` |
| `Заказ покупателя.xlsx` | шапка V03-01, заказчик, изготовитель, строка продукции | `ЗаказыПокупателя`, `СтрокиЗаказа` |
| `Спецификация.xlsx` | изделие, изготовитель, состав и операции | `Спецификации`, `СоставСпецификации`, `Номенклатура` |
| `Цены.xlsx` | ресурсы, цены и дата 01.03.2027 | `Цены` |
| `Заказ на производство.xlsx` | шапка V03-P01, продукция, материалы и операции | `ЗаказыНаПроизводство`, `ПродукцияКВыпуску`, `РесурсыПроизводства` |
| `Заметки.json` | заголовок, логин, текст, дата | `Заметки` |

В V03 материалы и операции различаются полем `Вид`: `Товар`, `Материал` или `Операция`. Время заполняется только у операций, у материалов остаётся нулём. Цены действуют с 01.03.2027, НДС, наценка и доставка не учитываются.

## Что понадобится

| Что открыть | Где найти | Зачем |
|---|---|---|
| draw.io | `https://app.diagrams.net/` | ER-диаграмма и PDF |
| XAMPP | `Пуск`, затем `XAMPP Control Panel` | MySQL и phpMyAdmin |
| phpMyAdmin | `http://localhost:4433/phpmyadmin` | таблицы, связи, импорт |
| Файлы V03 | `reports/variants/V03/` | JSON и Excel варианта |
| Скрипты V03 | `reports/prep/sql/` | готовые `CREATE TABLE`, `ALTER TABLE`, `INSERT` и запрос стоимости |

## Три задания V03

| Задание | Что делаем | Что сдаём |
|---|---|---|
| 1 | Собираем ER-диаграмму на русском языке: двенадцать таблиц и четырнадцать связей | PDF и исходник `.drawio` |
| 2 | Создаём базу `dkip2027_v03`, таблицы, связи и загружаем данные V03 | SQL-скрипт и выгрузку базы |
| 3 | Считаем нормативную стоимость заказа V03-01 запросом с `JOIN` и `SUM` | SQL-запрос и результат `10 035,00` |

## Задание 1. ER-диаграмма на русском языке

Модель собирается из документов V03. Названия таблиц и атрибутов записаны по-русски, чтобы диаграмму можно было читать без расшифровки. Каждая таблица добавляется отдельным шагом: сначала шаблон, затем первичный ключ, затем остальные атрибуты. Сразу после таблицы проводятся её связи. Справа от шагов стоит слайдер: на каждом слайде показано, как выглядит таблица после очередного шага.

Перед началом откройте `app.diagrams.net`, создайте пустую диаграмму и сохраните файл `V03_ER_Фамилия.drawio`. Включите сетку: `View` → `Grid`. Для таблиц берите фигуру `Table 1` из раздела `Отношения сущностей`.

Для каждой связи берите готовую линию `1 to Many` или `1 to 1` из раздела `Отношения сущностей`. После того как линия поставлена, выделите её, откройте `Соединение` и включите `Автоматически обходить фигуры`. Тогда линия обойдёт таблицы и не перекроет атрибуты. Линия должна выходить из правой или левой границы атрибута и входить в правую или левую границу атрибута другой таблицы.

### Шаг 1. Таблица «Заказчики»

Кто участвует в системе: покупатели, поставщики и изготовители. Одна таблица вместо трёх справочников, роль хранится в поле «Тип».

Источник: `Заказчики.json` даёт шесть покупателей. Изготовитель «Мастерская «Глина»» добавляется отдельной строкой, потому что в JSON его нет.

<ol>
<li>Создайте шаблон <code>Table 1</code> и назовите таблицу «Заказчики».</li>
<li>Добавьте первичный ключ <code>КодЗаказчика</code>. Он нужен, чтобы однозначно определить конкретного заказчика: без ключа два магазина с одинаковым названием будет невозможно различить.</li>
<li>Добавьте атрибут <code>Наименование</code>.</li>
<li>Добавьте атрибут <code>ИНН</code>. Если ИНН нет, оставьте пустую строку.</li>
<li>Добавьте атрибут <code>Адрес</code>.</li>
<li>Добавьте атрибут <code>Телефон</code>.</li>
<li>Добавьте атрибут <code>Тип</code>: покупатель или изготовитель.</li>
</ol>

<div class="schema-slider" data-slider>
<div class="schema-slider-bar">
<strong>Таблица «Заказчики»: 7 шагов</strong>
<div class="schema-slider-actions">
<button type="button" class="schema-btn" data-slider-prev aria-label="Предыдущий шаг">←</button>
<span class="schema-slider-counter" data-slider-counter>1 / 7</span>
<button type="button" class="schema-btn" data-slider-next aria-label="Следующий шаг">→</button>
</div>
</div>
<div class="schema-track" data-slider-track>
<article class="schema-slide" aria-label="Заказчики, шаг 1">
<h4>1. Шаблон таблицы</h4>
<p><img src="reports/screens/prep/v03/01-zakazchiki-01.png" alt="Таблица «Заказчики», шаг 1: Шаблон таблицы" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Заказчики, шаг 2">
<h4>2. Первичный ключ</h4>
<p><img src="reports/screens/prep/v03/01-zakazchiki-02.png" alt="Таблица «Заказчики», шаг 2: Первичный ключ" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Заказчики, шаг 3">
<h4>3. Наименование</h4>
<p><img src="reports/screens/prep/v03/01-zakazchiki-03.png" alt="Таблица «Заказчики», шаг 3: Наименование" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Заказчики, шаг 4">
<h4>4. ИНН</h4>
<p><img src="reports/screens/prep/v03/01-zakazchiki-04.png" alt="Таблица «Заказчики», шаг 4: ИНН" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Заказчики, шаг 5">
<h4>5. Адрес</h4>
<p><img src="reports/screens/prep/v03/01-zakazchiki-05.png" alt="Таблица «Заказчики», шаг 5: Адрес" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Заказчики, шаг 6">
<h4>6. Телефон</h4>
<p><img src="reports/screens/prep/v03/01-zakazchiki-06.png" alt="Таблица «Заказчики», шаг 6: Телефон" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Заказчики, шаг 7">
<h4>7. Тип</h4>
<p><img src="reports/screens/prep/v03/01-zakazchiki-07.png" alt="Таблица «Заказчики», шаг 7: Тип" style="max-width:340px"></p>
</article>
</div>
</div>

### Шаг 2. Таблица «Номенклатура»

Один справочник для изделий, материалов и операций. Вид ресурса хранится в поле «Вид», поэтому состав спецификации не раздваивается на две таблицы.

Источник: Изделие и коды берутся из `Заказ покупателя.xlsx` и `Спецификация.xlsx`, материалы и операции из `Спецификация.xlsx` и `Цены.xlsx`.

<ol>
<li>Создайте шаблон и назовите таблицу «Номенклатура».</li>
<li>Добавьте <code>КодРесурса</code>. Он различает изделие, материал и операцию.</li>
<li>Добавьте <code>Код</code> из документа: P-01, M-01, O-01. Код объявляется уникальным.</li>
<li>Добавьте <code>Наименование</code>.</li>
<li>Добавьте <code>Вид</code>: товар, материал или операция.</li>
<li>Добавьте <code>Единица</code>: ед., кг, шт или ч.</li>
</ol>

<div class="schema-slider" data-slider>
<div class="schema-slider-bar">
<strong>Таблица «Номенклатура»: 6 шагов</strong>
<div class="schema-slider-actions">
<button type="button" class="schema-btn" data-slider-prev aria-label="Предыдущий шаг">←</button>
<span class="schema-slider-counter" data-slider-counter>1 / 6</span>
<button type="button" class="schema-btn" data-slider-next aria-label="Следующий шаг">→</button>
</div>
</div>
<div class="schema-track" data-slider-track>
<article class="schema-slide" aria-label="Номенклатура, шаг 1">
<h4>1. Шаблон таблицы</h4>
<p><img src="reports/screens/prep/v03/02-nomenklatura-01.png" alt="Таблица «Номенклатура», шаг 1: Шаблон таблицы" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Номенклатура, шаг 2">
<h4>2. Первичный ключ</h4>
<p><img src="reports/screens/prep/v03/02-nomenklatura-02.png" alt="Таблица «Номенклатура», шаг 2: Первичный ключ" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Номенклатура, шаг 3">
<h4>3. Код</h4>
<p><img src="reports/screens/prep/v03/02-nomenklatura-03.png" alt="Таблица «Номенклатура», шаг 3: Код" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Номенклатура, шаг 4">
<h4>4. Наименование</h4>
<p><img src="reports/screens/prep/v03/02-nomenklatura-04.png" alt="Таблица «Номенклатура», шаг 4: Наименование" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Номенклатура, шаг 5">
<h4>5. Вид</h4>
<p><img src="reports/screens/prep/v03/02-nomenklatura-05.png" alt="Таблица «Номенклатура», шаг 5: Вид" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Номенклатура, шаг 6">
<h4>6. Единица</h4>
<p><img src="reports/screens/prep/v03/02-nomenklatura-06.png" alt="Таблица «Номенклатура», шаг 6: Единица" style="max-width:340px"></p>
</article>
</div>
</div>

### Шаг 3. Таблица «Цены»

Цена не принадлежит ресурсу навсегда: с 1 марта 2027 года действует одна цена, позже может появиться другая. Поэтому цена хранится вместе с датой начала действия.

Источник: `Цены.xlsx`: пять строк, у каждой ресурс, единица, цена и дата 01.03.2027.

<ol>
<li>Создайте шаблон и назовите таблицу «Цены».</li>
<li>Добавьте <code>КодРесурса</code> и <code>ДатаНачала</code>. Пара задаёт цену ресурса на конкретную дату и не даёт записать одну и ту же цену дважды.</li>
<li>Добавьте <code>Цена</code>.</li>
</ol>

<div class="schema-slider" data-slider>
<div class="schema-slider-bar">
<strong>Таблица «Цены»: 3 шагов</strong>
<div class="schema-slider-actions">
<button type="button" class="schema-btn" data-slider-prev aria-label="Предыдущий шаг">←</button>
<span class="schema-slider-counter" data-slider-counter>1 / 3</span>
<button type="button" class="schema-btn" data-slider-next aria-label="Следующий шаг">→</button>
</div>
</div>
<div class="schema-track" data-slider-track>
<article class="schema-slide" aria-label="Цены, шаг 1">
<h4>1. Шаблон таблицы</h4>
<p><img src="reports/screens/prep/v03/03-ceny-01.png" alt="Таблица «Цены», шаг 1: Шаблон таблицы" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Цены, шаг 2">
<h4>2. Составной ключ</h4>
<p><img src="reports/screens/prep/v03/03-ceny-02.png" alt="Таблица «Цены», шаг 2: Составной ключ" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Цены, шаг 3">
<h4>3. Цена</h4>
<p><img src="reports/screens/prep/v03/03-ceny-03.png" alt="Таблица «Цены», шаг 3: Цена" style="max-width:340px"></p>
</article>
</div>
</div>

**Связи**

<ol>
<li>Проведите связь <code>Цены.КодРесурса</code> → <code>Номенклатура.КодРесурса</code>. Возьмите линию <code>1 to Many</code>: простой конец к родительской таблице, конец с маркером к дочерней. Включите <code>Соединение</code> → <code>Автоматически обходить фигуры</code>.
<figure class="diagram">
<img src="reports/screens/prep/v03/link-01.png" alt="Связь Цены.КодРесурса → Номенклатура.КодРесурса" style="max-width:520px">
<figcaption>Связь <code>Цены.КодРесурса</code> → <code>Номенклатура.КодРесурса</code>. На линии она идёт от родительской таблицы <code>Номенклатура</code> к дочерней <code>Цены</code>, маркер кратности стоит у дочерней таблицы <code>Цены</code>. Линия обходит таблицы и не перекрывает атрибуты.</figcaption>
</figure>
</li>
</ol>

### Шаг 4. Таблица «Спецификации»

Шапка рецепта изделия: номер спецификации, изделие, название, количество выпуска и изготовитель. Строки состава появятся в следующей таблице.

Источник: Шапка `Спецификация.xlsx`: изделие «Кружка 300 мл», изготовитель «Мастерская «Глина»».

<ol>
<li>Создайте шаблон и назовите таблицу «Спецификации».</li>
<li>Добавьте <code>КодСпецификации</code>.</li>
<li>Добавьте <code>КодИзделия</code> и пометьте уникальность: у изделия одна спецификация.</li>
<li>Добавьте <code>Наименование</code>.</li>
<li>Добавьте <code>КоличествоВыпуска</code>: нормы заданы на одну единицу готовой продукции.</li>
<li>Добавьте <code>КодИзготовителя</code>.</li>
</ol>

<div class="schema-slider" data-slider>
<div class="schema-slider-bar">
<strong>Таблица «Спецификации»: 6 шагов</strong>
<div class="schema-slider-actions">
<button type="button" class="schema-btn" data-slider-prev aria-label="Предыдущий шаг">←</button>
<span class="schema-slider-counter" data-slider-counter>1 / 6</span>
<button type="button" class="schema-btn" data-slider-next aria-label="Следующий шаг">→</button>
</div>
</div>
<div class="schema-track" data-slider-track>
<article class="schema-slide" aria-label="Спецификации, шаг 1">
<h4>1. Шаблон таблицы</h4>
<p><img src="reports/screens/prep/v03/04-specifikacii-01.png" alt="Таблица «Спецификации», шаг 1: Шаблон таблицы" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Спецификации, шаг 2">
<h4>2. Первичный ключ</h4>
<p><img src="reports/screens/prep/v03/04-specifikacii-02.png" alt="Таблица «Спецификации», шаг 2: Первичный ключ" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Спецификации, шаг 3">
<h4>3. Код изделия</h4>
<p><img src="reports/screens/prep/v03/04-specifikacii-03.png" alt="Таблица «Спецификации», шаг 3: Код изделия" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Спецификации, шаг 4">
<h4>4. Наименование</h4>
<p><img src="reports/screens/prep/v03/04-specifikacii-04.png" alt="Таблица «Спецификации», шаг 4: Наименование" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Спецификации, шаг 5">
<h4>5. Количество выпуска</h4>
<p><img src="reports/screens/prep/v03/04-specifikacii-05.png" alt="Таблица «Спецификации», шаг 5: Количество выпуска" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Спецификации, шаг 6">
<h4>6. Код изготовителя</h4>
<p><img src="reports/screens/prep/v03/04-specifikacii-06.png" alt="Таблица «Спецификации», шаг 6: Код изготовителя" style="max-width:340px"></p>
</article>
</div>
</div>

**Связи**

<ol>
<li>Проведите связь <code>Спецификации.КодИзделия</code> → <code>Номенклатура.КодРесурса (линия 1 to 1)</code>. Возьмите линию <code>1 to 1</code>, черты должны быть на обоих концах. Включите <code>Соединение</code> → <code>Автоматически обходить фигуры</code>.
<figure class="diagram">
<img src="reports/screens/prep/v03/link-02.png" alt="Связь Спецификации.КодИзделия → Номенклатура.КодРесурса (линия 1 to 1)" style="max-width:520px">
<figcaption>Связь <code>Спецификации.КодИзделия</code> → <code>Номенклатура.КодРесурса (линия 1 to 1)</code>. На линии она идёт от родительской таблицы <code>Номенклатура</code> к дочерней <code>Спецификации</code>, черты стоят на обоих концах. Линия обходит таблицы и не перекрывает атрибуты.</figcaption>
</figure>
</li>
<li>Проведите связь <code>Спецификации.КодИзготовителя</code> → <code>Заказчики.КодЗаказчика</code>. Возьмите линию <code>1 to Many</code>: простой конец к родительской таблице, конец с маркером к дочерней. Включите <code>Соединение</code> → <code>Автоматически обходить фигуры</code>.
<figure class="diagram">
<img src="reports/screens/prep/v03/link-03.png" alt="Связь Спецификации.КодИзготовителя → Заказчики.КодЗаказчика" style="max-width:520px">
<figcaption>Связь <code>Спецификации.КодИзготовителя</code> → <code>Заказчики.КодЗаказчика</code>. На линии она идёт от родительской таблицы <code>Заказчики</code> к дочерней <code>Спецификации</code>, маркер кратности стоит у дочерней таблицы <code>Спецификации</code>. Линия обходит таблицы и не перекрывает атрибуты.</figcaption>
</figure>
</li>
</ol>

### Шаг 5. Таблица «СоставСпецификации»

Строки состава: какой ресурс и в каком количестве входит в спецификацию. Пара «спецификация и ресурс» уникальна, поэтому ключ составной.

Источник: Таблицы «Состав» и «Технологические операции» в `Спецификация.xlsx`: глина, глазурь, коробка, формовка, глазурование и обжиг.

<ol>
<li>Создайте шаблон и назовите таблицу «СоставСпецификации».</li>
<li>Добавьте <code>КодСпецификации</code> и <code>КодРесурса</code>. Один ресурс не может входить в спецификацию дважды.</li>
<li>Добавьте <code>Количество</code>: норма расхода на единицу продукции.</li>
<li>Добавьте <code>НормаВремени</code>: часы операции на единицу продукции. Для материала оставьте 0.</li>
</ol>

<div class="schema-slider" data-slider>
<div class="schema-slider-bar">
<strong>Таблица «СоставСпецификации»: 4 шагов</strong>
<div class="schema-slider-actions">
<button type="button" class="schema-btn" data-slider-prev aria-label="Предыдущий шаг">←</button>
<span class="schema-slider-counter" data-slider-counter>1 / 4</span>
<button type="button" class="schema-btn" data-slider-next aria-label="Следующий шаг">→</button>
</div>
</div>
<div class="schema-track" data-slider-track>
<article class="schema-slide" aria-label="СоставСпецификации, шаг 1">
<h4>1. Шаблон таблицы</h4>
<p><img src="reports/screens/prep/v03/05-sostav-01.png" alt="Таблица «СоставСпецификации», шаг 1: Шаблон таблицы" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="СоставСпецификации, шаг 2">
<h4>2. Составной ключ</h4>
<p><img src="reports/screens/prep/v03/05-sostav-02.png" alt="Таблица «СоставСпецификации», шаг 2: Составной ключ" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="СоставСпецификации, шаг 3">
<h4>3. Количество</h4>
<p><img src="reports/screens/prep/v03/05-sostav-03.png" alt="Таблица «СоставСпецификации», шаг 3: Количество" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="СоставСпецификации, шаг 4">
<h4>4. Норма времени</h4>
<p><img src="reports/screens/prep/v03/05-sostav-04.png" alt="Таблица «СоставСпецификации», шаг 4: Норма времени" style="max-width:340px"></p>
</article>
</div>
</div>

**Связи**

<ol>
<li>Проведите связь <code>СоставСпецификации.КодСпецификации</code> → <code>Спецификации.КодСпецификации</code>. Возьмите линию <code>1 to Many</code>: простой конец к родительской таблице, конец с маркером к дочерней. Включите <code>Соединение</code> → <code>Автоматически обходить фигуры</code>.
<figure class="diagram">
<img src="reports/screens/prep/v03/link-04.png" alt="Связь СоставСпецификации.КодСпецификации → Спецификации.КодСпецификации" style="max-width:520px">
<figcaption>Связь <code>СоставСпецификации.КодСпецификации</code> → <code>Спецификации.КодСпецификации</code>. На линии она идёт от родительской таблицы <code>Спецификации</code> к дочерней <code>СоставСпецификации</code>, маркер кратности стоит у дочерней таблицы <code>СоставСпецификации</code>. Линия обходит таблицы и не перекрывает атрибуты.</figcaption>
</figure>
</li>
<li>Проведите связь <code>СоставСпецификации.КодРесурса</code> → <code>Номенклатура.КодРесурса</code>. Возьмите линию <code>1 to Many</code>: простой конец к родительской таблице, конец с маркером к дочерней. Включите <code>Соединение</code> → <code>Автоматически обходить фигуры</code>.
<figure class="diagram">
<img src="reports/screens/prep/v03/link-05.png" alt="Связь СоставСпецификации.КодРесурса → Номенклатура.КодРесурса" style="max-width:520px">
<figcaption>Связь <code>СоставСпецификации.КодРесурса</code> → <code>Номенклатура.КодРесурса</code>. На линии она идёт от родительской таблицы <code>Номенклатура</code> к дочерней <code>СоставСпецификации</code>, маркер кратности стоит у дочерней таблицы <code>СоставСпецификации</code>. Линия обходит таблицы и не перекрывает атрибуты.</figcaption>
</figure>
</li>
</ol>

### Шаг 6. Таблица «ЗаказыПокупателя»

Шапка заказа покупателя: номер, дата, заказчик и исполнитель. Строки заказа появятся в следующей таблице.

Источник: Шапка `Заказ покупателя.xlsx`: V03-01 от 15.03.2027, заказчик 003000001, изготовитель «Мастерская «Глина»».

<ol>
<li>Создайте шаблон и назовите таблицу «ЗаказыПокупателя».</li>
<li>Добавьте <code>КодЗаказа</code>.</li>
<li>Добавьте <code>НомерДокумента</code> и объявите его уникальным.</li>
<li>Добавьте <code>ДатаДокумента</code>.</li>
<li>Добавьте <code>КодЗаказчика</code>.</li>
<li>Добавьте <code>КодИсполнителя</code>.</li>
</ol>

<div class="schema-slider" data-slider>
<div class="schema-slider-bar">
<strong>Таблица «ЗаказыПокупателя»: 6 шагов</strong>
<div class="schema-slider-actions">
<button type="button" class="schema-btn" data-slider-prev aria-label="Предыдущий шаг">←</button>
<span class="schema-slider-counter" data-slider-counter>1 / 6</span>
<button type="button" class="schema-btn" data-slider-next aria-label="Следующий шаг">→</button>
</div>
</div>
<div class="schema-track" data-slider-track>
<article class="schema-slide" aria-label="ЗаказыПокупателя, шаг 1">
<h4>1. Шаблон таблицы</h4>
<p><img src="reports/screens/prep/v03/06-zakazy-01.png" alt="Таблица «ЗаказыПокупателя», шаг 1: Шаблон таблицы" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="ЗаказыПокупателя, шаг 2">
<h4>2. Первичный ключ</h4>
<p><img src="reports/screens/prep/v03/06-zakazy-02.png" alt="Таблица «ЗаказыПокупателя», шаг 2: Первичный ключ" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="ЗаказыПокупателя, шаг 3">
<h4>3. Номер документа</h4>
<p><img src="reports/screens/prep/v03/06-zakazy-03.png" alt="Таблица «ЗаказыПокупателя», шаг 3: Номер документа" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="ЗаказыПокупателя, шаг 4">
<h4>4. Дата документа</h4>
<p><img src="reports/screens/prep/v03/06-zakazy-04.png" alt="Таблица «ЗаказыПокупателя», шаг 4: Дата документа" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="ЗаказыПокупателя, шаг 5">
<h4>5. Код заказчика</h4>
<p><img src="reports/screens/prep/v03/06-zakazy-05.png" alt="Таблица «ЗаказыПокупателя», шаг 5: Код заказчика" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="ЗаказыПокупателя, шаг 6">
<h4>6. Код исполнителя</h4>
<p><img src="reports/screens/prep/v03/06-zakazy-06.png" alt="Таблица «ЗаказыПокупателя», шаг 6: Код исполнителя" style="max-width:340px"></p>
</article>
</div>
</div>

**Связи**

<ol>
<li>Проведите связь <code>ЗаказыПокупателя.КодЗаказчика</code> → <code>Заказчики.КодЗаказчика</code>. Возьмите линию <code>1 to Many</code>: простой конец к родительской таблице, конец с маркером к дочерней. Включите <code>Соединение</code> → <code>Автоматически обходить фигуры</code>.
<figure class="diagram">
<img src="reports/screens/prep/v03/link-06.png" alt="Связь ЗаказыПокупателя.КодЗаказчика → Заказчики.КодЗаказчика" style="max-width:520px">
<figcaption>Связь <code>ЗаказыПокупателя.КодЗаказчика</code> → <code>Заказчики.КодЗаказчика</code>. На линии она идёт от родительской таблицы <code>Заказчики</code> к дочерней <code>ЗаказыПокупателя</code>, маркер кратности стоит у дочерней таблицы <code>ЗаказыПокупателя</code>. Линия обходит таблицы и не перекрывает атрибуты.</figcaption>
</figure>
</li>
<li>Проведите связь <code>ЗаказыПокупателя.КодИсполнителя</code> → <code>Заказчики.КодЗаказчика</code>. Возьмите линию <code>1 to Many</code>: простой конец к родительской таблице, конец с маркером к дочерней. Включите <code>Соединение</code> → <code>Автоматически обходить фигуры</code>.
<figure class="diagram">
<img src="reports/screens/prep/v03/link-07.png" alt="Связь ЗаказыПокупателя.КодИсполнителя → Заказчики.КодЗаказчика" style="max-width:520px">
<figcaption>Связь <code>ЗаказыПокупателя.КодИсполнителя</code> → <code>Заказчики.КодЗаказчика</code>. На линии она идёт от родительской таблицы <code>Заказчики</code> к дочерней <code>ЗаказыПокупателя</code>, маркер кратности стоит у дочерней таблицы <code>ЗаказыПокупателя</code>. Линия обходит таблицы и не перекрывает атрибуты.</figcaption>
</figure>
</li>
</ol>

### Шаг 7. Таблица «СтрокиЗаказа»

Строки заказа: изделие, количество, продажная цена и скидка. В заказе может быть несколько строк.

Источник: Строка продукции в `Заказ покупателя.xlsx`: «Кружка 300 мл», 18 ед., цена 700, скидка 0.

<ol>
<li>Создайте шаблон и назовите таблицу «СтрокиЗаказа».</li>
<li>Добавьте <code>КодСтроки</code>.</li>
<li>Добавьте <code>КодЗаказа</code>.</li>
<li>Добавьте <code>КодТовара</code>.</li>
<li>Добавьте <code>Количество</code>.</li>
<li>Добавьте <code>ЦенаПродажи</code>.</li>
<li>Добавьте <code>Скидка</code>.</li>
</ol>

<div class="schema-slider" data-slider>
<div class="schema-slider-bar">
<strong>Таблица «СтрокиЗаказа»: 7 шагов</strong>
<div class="schema-slider-actions">
<button type="button" class="schema-btn" data-slider-prev aria-label="Предыдущий шаг">←</button>
<span class="schema-slider-counter" data-slider-counter>1 / 7</span>
<button type="button" class="schema-btn" data-slider-next aria-label="Следующий шаг">→</button>
</div>
</div>
<div class="schema-track" data-slider-track>
<article class="schema-slide" aria-label="СтрокиЗаказа, шаг 1">
<h4>1. Шаблон таблицы</h4>
<p><img src="reports/screens/prep/v03/07-stroki-01.png" alt="Таблица «СтрокиЗаказа», шаг 1: Шаблон таблицы" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="СтрокиЗаказа, шаг 2">
<h4>2. Первичный ключ</h4>
<p><img src="reports/screens/prep/v03/07-stroki-02.png" alt="Таблица «СтрокиЗаказа», шаг 2: Первичный ключ" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="СтрокиЗаказа, шаг 3">
<h4>3. Код заказа</h4>
<p><img src="reports/screens/prep/v03/07-stroki-03.png" alt="Таблица «СтрокиЗаказа», шаг 3: Код заказа" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="СтрокиЗаказа, шаг 4">
<h4>4. Код товара</h4>
<p><img src="reports/screens/prep/v03/07-stroki-04.png" alt="Таблица «СтрокиЗаказа», шаг 4: Код товара" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="СтрокиЗаказа, шаг 5">
<h4>5. Количество</h4>
<p><img src="reports/screens/prep/v03/07-stroki-05.png" alt="Таблица «СтрокиЗаказа», шаг 5: Количество" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="СтрокиЗаказа, шаг 6">
<h4>6. Цена продажи</h4>
<p><img src="reports/screens/prep/v03/07-stroki-06.png" alt="Таблица «СтрокиЗаказа», шаг 6: Цена продажи" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="СтрокиЗаказа, шаг 7">
<h4>7. Скидка</h4>
<p><img src="reports/screens/prep/v03/07-stroki-07.png" alt="Таблица «СтрокиЗаказа», шаг 7: Скидка" style="max-width:340px"></p>
</article>
</div>
</div>

**Связи**

<ol>
<li>Проведите связь <code>СтрокиЗаказа.КодЗаказа</code> → <code>ЗаказыПокупателя.КодЗаказа</code>. Возьмите линию <code>1 to Many</code>: простой конец к родительской таблице, конец с маркером к дочерней. Включите <code>Соединение</code> → <code>Автоматически обходить фигуры</code>.
<figure class="diagram">
<img src="reports/screens/prep/v03/link-08.png" alt="Связь СтрокиЗаказа.КодЗаказа → ЗаказыПокупателя.КодЗаказа" style="max-width:520px">
<figcaption>Связь <code>СтрокиЗаказа.КодЗаказа</code> → <code>ЗаказыПокупателя.КодЗаказа</code>. На линии она идёт от родительской таблицы <code>ЗаказыПокупателя</code> к дочерней <code>СтрокиЗаказа</code>, маркер кратности стоит у дочерней таблицы <code>СтрокиЗаказа</code>. Линия обходит таблицы и не перекрывает атрибуты.</figcaption>
</figure>
</li>
<li>Проведите связь <code>СтрокиЗаказа.КодТовара</code> → <code>Номенклатура.КодРесурса</code>. Возьмите линию <code>1 to Many</code>: простой конец к родительской таблице, конец с маркером к дочерней. Включите <code>Соединение</code> → <code>Автоматически обходить фигуры</code>.
<figure class="diagram">
<img src="reports/screens/prep/v03/link-09.png" alt="Связь СтрокиЗаказа.КодТовара → Номенклатура.КодРесурса" style="max-width:520px">
<figcaption>Связь <code>СтрокиЗаказа.КодТовара</code> → <code>Номенклатура.КодРесурса</code>. На линии она идёт от родительской таблицы <code>Номенклатура</code> к дочерней <code>СтрокиЗаказа</code>, маркер кратности стоит у дочерней таблицы <code>СтрокиЗаказа</code>. Линия обходит таблицы и не перекрывает атрибуты.</figcaption>
</figure>
</li>
</ol>

### Шаг 8. Таблица «ЗаказыНаПроизводство»

Шапка производственного заказа: номер, дата, дата запуска и подразделение. Это отдельный документ, поэтому отдельная шапка.

Источник: `Заказ на производство.xlsx`: V03-P01, связан с заказом V03-01, запуск 16.03.2027, подразделение «Основное производство».

<ol>
<li>Создайте шаблон и назовите таблицу «ЗаказыНаПроизводство».</li>
<li>Добавьте <code>КодПроизводственногоЗаказа</code>.</li>
<li>Добавьте <code>НомерДокумента</code> и объявите его уникальным.</li>
<li>Добавьте <code>ДатаДокумента</code>.</li>
<li>Добавьте <code>ДатаЗапуска</code>.</li>
<li>Добавьте <code>Подразделение</code>.</li>
</ol>

<div class="schema-slider" data-slider>
<div class="schema-slider-bar">
<strong>Таблица «ЗаказыНаПроизводство»: 6 шагов</strong>
<div class="schema-slider-actions">
<button type="button" class="schema-btn" data-slider-prev aria-label="Предыдущий шаг">←</button>
<span class="schema-slider-counter" data-slider-counter>1 / 6</span>
<button type="button" class="schema-btn" data-slider-next aria-label="Следующий шаг">→</button>
</div>
</div>
<div class="schema-track" data-slider-track>
<article class="schema-slide" aria-label="ЗаказыНаПроизводство, шаг 1">
<h4>1. Шаблон таблицы</h4>
<p><img src="reports/screens/prep/v03/08-proizvodstvo-01.png" alt="Таблица «ЗаказыНаПроизводство», шаг 1: Шаблон таблицы" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="ЗаказыНаПроизводство, шаг 2">
<h4>2. Первичный ключ</h4>
<p><img src="reports/screens/prep/v03/08-proizvodstvo-02.png" alt="Таблица «ЗаказыНаПроизводство», шаг 2: Первичный ключ" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="ЗаказыНаПроизводство, шаг 3">
<h4>3. Номер документа</h4>
<p><img src="reports/screens/prep/v03/08-proizvodstvo-03.png" alt="Таблица «ЗаказыНаПроизводство», шаг 3: Номер документа" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="ЗаказыНаПроизводство, шаг 4">
<h4>4. Дата документа</h4>
<p><img src="reports/screens/prep/v03/08-proizvodstvo-04.png" alt="Таблица «ЗаказыНаПроизводство», шаг 4: Дата документа" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="ЗаказыНаПроизводство, шаг 5">
<h4>5. Дата запуска</h4>
<p><img src="reports/screens/prep/v03/08-proizvodstvo-05.png" alt="Таблица «ЗаказыНаПроизводство», шаг 5: Дата запуска" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="ЗаказыНаПроизводство, шаг 6">
<h4>6. Подразделение</h4>
<p><img src="reports/screens/prep/v03/08-proizvodstvo-06.png" alt="Таблица «ЗаказыНаПроизводство», шаг 6: Подразделение" style="max-width:340px"></p>
</article>
</div>
</div>

### Шаг 9. Таблица «ПродукцияКВыпуску»

Что выпускаем по производственному заказу. В заказе может быть несколько изделий, поэтому ключ составной.

Источник: Раздел «Продукция к выпуску» в `Заказ на производство.xlsx`: «Кружка 300 мл», 18 ед.

<ol>
<li>Создайте шаблон и назовите таблицу «ПродукцияКВыпуску».</li>
<li>Добавьте <code>КодПроизводственногоЗаказа</code> и <code>КодТовара</code>.</li>
<li>Добавьте <code>Количество</code>.</li>
</ol>

<div class="schema-slider" data-slider>
<div class="schema-slider-bar">
<strong>Таблица «ПродукцияКВыпуску»: 3 шагов</strong>
<div class="schema-slider-actions">
<button type="button" class="schema-btn" data-slider-prev aria-label="Предыдущий шаг">←</button>
<span class="schema-slider-counter" data-slider-counter>1 / 3</span>
<button type="button" class="schema-btn" data-slider-next aria-label="Следующий шаг">→</button>
</div>
</div>
<div class="schema-track" data-slider-track>
<article class="schema-slide" aria-label="ПродукцияКВыпуску, шаг 1">
<h4>1. Шаблон таблицы</h4>
<p><img src="reports/screens/prep/v03/09-produkciya-01.png" alt="Таблица «ПродукцияКВыпуску», шаг 1: Шаблон таблицы" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="ПродукцияКВыпуску, шаг 2">
<h4>2. Составной ключ</h4>
<p><img src="reports/screens/prep/v03/09-produkciya-02.png" alt="Таблица «ПродукцияКВыпуску», шаг 2: Составной ключ" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="ПродукцияКВыпуску, шаг 3">
<h4>3. Количество</h4>
<p><img src="reports/screens/prep/v03/09-produkciya-03.png" alt="Таблица «ПродукцияКВыпуску», шаг 3: Количество" style="max-width:340px"></p>
</article>
</div>
</div>

**Связи**

<ol>
<li>Проведите связь <code>ПродукцияКВыпуску.КодПроизводственногоЗаказа</code> → <code>ЗаказыНаПроизводство.КодПроизводственногоЗаказа</code>. Возьмите линию <code>1 to Many</code>: простой конец к родительской таблице, конец с маркером к дочерней. Включите <code>Соединение</code> → <code>Автоматически обходить фигуры</code>.
<figure class="diagram">
<img src="reports/screens/prep/v03/link-10.png" alt="Связь ПродукцияКВыпуску.КодПроизводственногоЗаказа → ЗаказыНаПроизводство.КодПроизводственногоЗаказа" style="max-width:520px">
<figcaption>Связь <code>ПродукцияКВыпуску.КодПроизводственногоЗаказа</code> → <code>ЗаказыНаПроизводство.КодПроизводственногоЗаказа</code>. На линии она идёт от родительской таблицы <code>ЗаказыНаПроизводство</code> к дочерней <code>ПродукцияКВыпуску</code>, маркер кратности стоит у дочерней таблицы <code>ПродукцияКВыпуску</code>. Линия обходит таблицы и не перекрывает атрибуты.</figcaption>
</figure>
</li>
<li>Проведите связь <code>ПродукцияКВыпуску.КодТовара</code> → <code>Номенклатура.КодРесурса</code>. Возьмите линию <code>1 to Many</code>: простой конец к родительской таблице, конец с маркером к дочерней. Включите <code>Соединение</code> → <code>Автоматически обходить фигуры</code>.
<figure class="diagram">
<img src="reports/screens/prep/v03/link-11.png" alt="Связь ПродукцияКВыпуску.КодТовара → Номенклатура.КодРесурса" style="max-width:520px">
<figcaption>Связь <code>ПродукцияКВыпуску.КодТовара</code> → <code>Номенклатура.КодРесурса</code>. На линии она идёт от родительской таблицы <code>Номенклатура</code> к дочерней <code>ПродукцияКВыпуску</code>, маркер кратности стоит у дочерней таблицы <code>ПродукцияКВыпуску</code>. Линия обходит таблицы и не перекрывает атрибуты.</figcaption>
</figure>
</li>
</ol>

### Шаг 10. Таблица «РесурсыПроизводства»

Плановый расход материалов и времени по производственному заказу. Ключ составной: заказ и ресурс.

Источник: Разделы «Потребность в материалах» и «Технологические операции» в `Заказ на производство.xlsx`: глина 8,1 кг, глазурь 0,54 кг, коробка 18 шт, формовка 7,2 ч, глазурование и обжиг 2,7 ч.

<ol>
<li>Создайте шаблон и назовите таблицу «РесурсыПроизводства».</li>
<li>Добавьте <code>КодПроизводственногоЗаказа</code> и <code>КодРесурса</code>.</li>
<li>Добавьте <code>Количество</code>: плановый расход материала.</li>
<li>Добавьте <code>НормаВремени</code>: плановые часы операции.</li>
</ol>

<div class="schema-slider" data-slider>
<div class="schema-slider-bar">
<strong>Таблица «РесурсыПроизводства»: 4 шагов</strong>
<div class="schema-slider-actions">
<button type="button" class="schema-btn" data-slider-prev aria-label="Предыдущий шаг">←</button>
<span class="schema-slider-counter" data-slider-counter>1 / 4</span>
<button type="button" class="schema-btn" data-slider-next aria-label="Следующий шаг">→</button>
</div>
</div>
<div class="schema-track" data-slider-track>
<article class="schema-slide" aria-label="РесурсыПроизводства, шаг 1">
<h4>1. Шаблон таблицы</h4>
<p><img src="reports/screens/prep/v03/10-resursy-01.png" alt="Таблица «РесурсыПроизводства», шаг 1: Шаблон таблицы" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="РесурсыПроизводства, шаг 2">
<h4>2. Составной ключ</h4>
<p><img src="reports/screens/prep/v03/10-resursy-02.png" alt="Таблица «РесурсыПроизводства», шаг 2: Составной ключ" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="РесурсыПроизводства, шаг 3">
<h4>3. Количество</h4>
<p><img src="reports/screens/prep/v03/10-resursy-03.png" alt="Таблица «РесурсыПроизводства», шаг 3: Количество" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="РесурсыПроизводства, шаг 4">
<h4>4. Норма времени</h4>
<p><img src="reports/screens/prep/v03/10-resursy-04.png" alt="Таблица «РесурсыПроизводства», шаг 4: Норма времени" style="max-width:340px"></p>
</article>
</div>
</div>

**Связи**

<ol>
<li>Проведите связь <code>РесурсыПроизводства.КодПроизводственногоЗаказа</code> → <code>ЗаказыНаПроизводство.КодПроизводственногоЗаказа</code>. Возьмите линию <code>1 to Many</code>: простой конец к родительской таблице, конец с маркером к дочерней. Включите <code>Соединение</code> → <code>Автоматически обходить фигуры</code>.
<figure class="diagram">
<img src="reports/screens/prep/v03/link-12.png" alt="Связь РесурсыПроизводства.КодПроизводственногоЗаказа → ЗаказыНаПроизводство.КодПроизводственногоЗаказа" style="max-width:520px">
<figcaption>Связь <code>РесурсыПроизводства.КодПроизводственногоЗаказа</code> → <code>ЗаказыНаПроизводство.КодПроизводственногоЗаказа</code>. На линии она идёт от родительской таблицы <code>ЗаказыНаПроизводство</code> к дочерней <code>РесурсыПроизводства</code>, маркер кратности стоит у дочерней таблицы <code>РесурсыПроизводства</code>. Линия обходит таблицы и не перекрывает атрибуты.</figcaption>
</figure>
</li>
<li>Проведите связь <code>РесурсыПроизводства.КодРесурса</code> → <code>Номенклатура.КодРесурса</code>. Возьмите линию <code>1 to Many</code>: простой конец к родительской таблице, конец с маркером к дочерней. Включите <code>Соединение</code> → <code>Автоматически обходить фигуры</code>.
<figure class="diagram">
<img src="reports/screens/prep/v03/link-13.png" alt="Связь РесурсыПроизводства.КодРесурса → Номенклатура.КодРесурса" style="max-width:520px">
<figcaption>Связь <code>РесурсыПроизводства.КодРесурса</code> → <code>Номенклатура.КодРесурса</code>. На линии она идёт от родительской таблицы <code>Номенклатура</code> к дочерней <code>РесурсыПроизводства</code>, маркер кратности стоит у дочерней таблицы <code>РесурсыПроизводства</code>. Линия обходит таблицы и не перекрывает атрибуты.</figcaption>
</figure>
</li>
</ol>

### Шаг 11. Таблица «Пользователи»

Учётные записи приложения: логин, хеш пароля, соль, роль, число ошибок и блокировка. Таблица нужна заданиям 4 и 5.

Источник: Требования заданий 4 и 5. В Excel и JSON этих данных нет, кроме логинов manager, technologist и master в `Заметки.json`.

<ol>
<li>Создайте шаблон и назовите таблицу «Пользователи».</li>
<li>Добавьте <code>КодПользователя</code>.</li>
<li>Добавьте <code>Логин</code> и объявите его уникальным.</li>
<li>Добавьте <code>ХешПароля</code>: хранится хеш, а не сам пароль.</li>
<li>Добавьте <code>Соль</code> для хеширования пароля.</li>
<li>Добавьте <code>Роль</code>: администратор или пользователь.</li>
<li>Добавьте <code>ЧислоОшибок</code>.</li>
<li>Добавьте <code>Заблокирован</code>.</li>
</ol>

<div class="schema-slider" data-slider>
<div class="schema-slider-bar">
<strong>Таблица «Пользователи»: 8 шагов</strong>
<div class="schema-slider-actions">
<button type="button" class="schema-btn" data-slider-prev aria-label="Предыдущий шаг">←</button>
<span class="schema-slider-counter" data-slider-counter>1 / 8</span>
<button type="button" class="schema-btn" data-slider-next aria-label="Следующий шаг">→</button>
</div>
</div>
<div class="schema-track" data-slider-track>
<article class="schema-slide" aria-label="Пользователи, шаг 1">
<h4>1. Шаблон таблицы</h4>
<p><img src="reports/screens/prep/v03/11-polzovateli-01.png" alt="Таблица «Пользователи», шаг 1: Шаблон таблицы" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Пользователи, шаг 2">
<h4>2. Первичный ключ</h4>
<p><img src="reports/screens/prep/v03/11-polzovateli-02.png" alt="Таблица «Пользователи», шаг 2: Первичный ключ" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Пользователи, шаг 3">
<h4>3. Логин</h4>
<p><img src="reports/screens/prep/v03/11-polzovateli-03.png" alt="Таблица «Пользователи», шаг 3: Логин" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Пользователи, шаг 4">
<h4>4. Хеш пароля</h4>
<p><img src="reports/screens/prep/v03/11-polzovateli-04.png" alt="Таблица «Пользователи», шаг 4: Хеш пароля" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Пользователи, шаг 5">
<h4>5. Соль</h4>
<p><img src="reports/screens/prep/v03/11-polzovateli-05.png" alt="Таблица «Пользователи», шаг 5: Соль" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Пользователи, шаг 6">
<h4>6. Роль</h4>
<p><img src="reports/screens/prep/v03/11-polzovateli-06.png" alt="Таблица «Пользователи», шаг 6: Роль" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Пользователи, шаг 7">
<h4>7. Число ошибок</h4>
<p><img src="reports/screens/prep/v03/11-polzovateli-07.png" alt="Таблица «Пользователи», шаг 7: Число ошибок" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Пользователи, шаг 8">
<h4>8. Блокировка</h4>
<p><img src="reports/screens/prep/v03/11-polzovateli-08.png" alt="Таблица «Пользователи», шаг 8: Блокировка" style="max-width:340px"></p>
</article>
</div>
</div>

### Шаг 12. Таблица «Заметки»

Заметки сотрудников. Автор хранится ссылкой на таблицу «Пользователи».

Источник: `Заметки.json`: пять записей, у каждой заголовок, логин автора, текст и дата.

<ol>
<li>Создайте шаблон и назовите таблицу «Заметки».</li>
<li>Добавьте <code>КодЗаметки</code>.</li>
<li>Добавьте <code>Заголовок</code>.</li>
<li>Добавьте <code>Содержание</code>.</li>
<li>Добавьте <code>КодПользователя</code>.</li>
<li>Добавьте <code>ДатаСоздания</code>.</li>
</ol>

<div class="schema-slider" data-slider>
<div class="schema-slider-bar">
<strong>Таблица «Заметки»: 6 шагов</strong>
<div class="schema-slider-actions">
<button type="button" class="schema-btn" data-slider-prev aria-label="Предыдущий шаг">←</button>
<span class="schema-slider-counter" data-slider-counter>1 / 6</span>
<button type="button" class="schema-btn" data-slider-next aria-label="Следующий шаг">→</button>
</div>
</div>
<div class="schema-track" data-slider-track>
<article class="schema-slide" aria-label="Заметки, шаг 1">
<h4>1. Шаблон таблицы</h4>
<p><img src="reports/screens/prep/v03/12-zametki-01.png" alt="Таблица «Заметки», шаг 1: Шаблон таблицы" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Заметки, шаг 2">
<h4>2. Первичный ключ</h4>
<p><img src="reports/screens/prep/v03/12-zametki-02.png" alt="Таблица «Заметки», шаг 2: Первичный ключ" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Заметки, шаг 3">
<h4>3. Заголовок</h4>
<p><img src="reports/screens/prep/v03/12-zametki-03.png" alt="Таблица «Заметки», шаг 3: Заголовок" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Заметки, шаг 4">
<h4>4. Содержание</h4>
<p><img src="reports/screens/prep/v03/12-zametki-04.png" alt="Таблица «Заметки», шаг 4: Содержание" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Заметки, шаг 5">
<h4>5. Код пользователя</h4>
<p><img src="reports/screens/prep/v03/12-zametki-05.png" alt="Таблица «Заметки», шаг 5: Код пользователя" style="max-width:340px"></p>
</article>
<article class="schema-slide" aria-label="Заметки, шаг 6">
<h4>6. Дата создания</h4>
<p><img src="reports/screens/prep/v03/12-zametki-06.png" alt="Таблица «Заметки», шаг 6: Дата создания" style="max-width:340px"></p>
</article>
</div>
</div>

**Связи**

<ol>
<li>Проведите связь <code>Заметки.КодПользователя</code> → <code>Пользователи.КодПользователя</code>. Возьмите линию <code>1 to Many</code>: простой конец к родительской таблице, конец с маркером к дочерней. Включите <code>Соединение</code> → <code>Автоматически обходить фигуры</code>.
<figure class="diagram">
<img src="reports/screens/prep/v03/link-14.png" alt="Связь Заметки.КодПользователя → Пользователи.КодПользователя" style="max-width:520px">
<figcaption>Связь <code>Заметки.КодПользователя</code> → <code>Пользователи.КодПользователя</code>. На линии она идёт от родительской таблицы <code>Пользователи</code> к дочерней <code>Заметки</code>, маркер кратности стоит у дочерней таблицы <code>Заметки</code>. Линия обходит таблицы и не перекрывает атрибуты.</figcaption>
</figure>
</li>
</ol>

### Связи, которые должны получиться

Всего в модели четырнадцать связей. Они уже проведены по шагам выше. Ниже сводная таблица для проверки: для всех связей, кроме одной, линия `1 to Many`, у `Спецификации.КодИзделия` линия `1 to 1`.

| № | Откуда | Куда | Линия |
|---:|---|---|---|
| 1 | `Цены.КодРесурса` | `Номенклатура.КодРесурса` | `1 to Many` |
| 2 | `Спецификации.КодИзделия` | `Номенклатура.КодРесурса` | `1 to 1` |
| 3 | `Спецификации.КодИзготовителя` | `Заказчики.КодЗаказчика` | `1 to Many` |
| 4 | `СоставСпецификации.КодСпецификации` | `Спецификации.КодСпецификации` | `1 to Many` |
| 5 | `СоставСпецификации.КодРесурса` | `Номенклатура.КодРесурса` | `1 to Many` |
| 6 | `ЗаказыПокупателя.КодЗаказчика` | `Заказчики.КодЗаказчика` | `1 to Many` |
| 7 | `ЗаказыПокупателя.КодИсполнителя` | `Заказчики.КодЗаказчика` | `1 to Many` |
| 8 | `СтрокиЗаказа.КодЗаказа` | `ЗаказыПокупателя.КодЗаказа` | `1 to Many` |
| 9 | `СтрокиЗаказа.КодТовара` | `Номенклатура.КодРесурса` | `1 to Many` |
| 10 | `ПродукцияКВыпуску.КодПроизводственногоЗаказа` | `ЗаказыНаПроизводство.КодПроизводственногоЗаказа` | `1 to Many` |
| 11 | `ПродукцияКВыпуску.КодТовара` | `Номенклатура.КодРесурса` | `1 to Many` |
| 12 | `РесурсыПроизводства.КодПроизводственногоЗаказа` | `ЗаказыНаПроизводство.КодПроизводственногоЗаказа` | `1 to Many` |
| 13 | `РесурсыПроизводства.КодРесурса` | `Номенклатура.КодРесурса` | `1 to Many` |
| 14 | `Заметки.КодПользователя` | `Пользователи.КодПользователя` | `1 to Many` |

Связь многие ко многим напрямую не рисуют: между таблицами стоит промежуточная таблица. В V03 это `СоставСпецификации`: она связывает `Спецификации` и `Номенклатура` двумя связями `1:N`.

<figure class="diagram">
<a href="reports/screens/prep/v03/er-v03.png" target="_blank" rel="noopener"><img src="reports/screens/prep/v03/er-v03.png" alt="Итоговая ER-диаграмма V03 с русскими названиями таблиц и атрибутов"></a>
<figcaption>Итоговая ER-диаграмма V03: двенадцать таблиц с русскими названиями и четырнадцать связей. У всех связей включено «Автоматически обходить фигуры», линии выходят из правой или левой границы атрибута и не перекрывают таблицы.</figcaption>
</figure>

## Задание 2. База данных и импорт

База называется `dkip2027_v03` и создаётся в XAMPP. Все таблицы и поля названы по-русски, поэтому в SQL они заключаются в обратные кавычки: `` `Заказчики` ``, `` `КодЗаказчика` ``. MySQL принимает такие имена, если база и соединение используют `utf8mb4`.

### Шаг 1. Запустите Apache и MySQL

Откройте XAMPP Control Panel и нажмите `Start` у Apache и MySQL. На учебных компьютерах Apache слушает порт `4433`, MySQL слушает `3306`. Обе строки должны стать зелёными.

### Шаг 2. Создайте базу

Перейдите по адресу `http://localhost:4433/phpmyadmin`. Пользователь `root`, пароль пустой. В левой панели нажмите `Создать БД`, введите имя `dkip2027_v03`, выберите сравнение `utf8mb4_unicode_ci` и нажмите `Создать`.

### Шаг 3. Создайте таблицы

Откройте вкладку `SQL` и выполните скрипт `V03_mysql_tables.sql` целиком. Он создаёт базу и двенадцать таблиц. Если phpMyAdmin не принимает несколько запросов сразу, выполняйте по одному `CREATE TABLE`. Ниже слайдер: на каждом слайде одна таблица и её полный `CREATE TABLE`.

<div class="schema-slider" data-slider>
<div class="schema-slider-bar">
<strong>Создание таблиц V03: 12 слайдов</strong>
<div class="schema-slider-actions">
<button type="button" class="schema-btn" data-slider-prev aria-label="Предыдущая таблица">←</button>
<span class="schema-slider-counter" data-slider-counter>1 / 12</span>
<button type="button" class="schema-btn" data-slider-next aria-label="Следующая таблица">→</button>
</div>
</div>
<div class="schema-track" data-slider-track>
<article class="schema-slide" aria-label="Заказчики">
<h4>1. <code>Заказчики</code></h4>
<p>Покупатели, поставщики и изготовители. Роль хранится в поле «Тип».</p>
<pre><code>CREATE TABLE `Заказчики` (
  `КодЗаказчика` VARCHAR(32) NOT NULL,
  `Наименование` VARCHAR(255) NOT NULL,
  `ИНН` VARCHAR(20) NOT NULL DEFAULT '',
  `Адрес` VARCHAR(500) NOT NULL,
  `Телефон` VARCHAR(64) NOT NULL,
  `Тип` VARCHAR(24) NOT NULL,
  PRIMARY KEY (`КодЗаказчика`),
  CONSTRAINT `ck_zakazchiki_tip`
    CHECK (`Тип` IN ('Покупатель', 'Поставщик', 'Изготовитель'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="Номенклатура">
<h4>2. <code>Номенклатура</code></h4>
<p>Изделия, материалы и операции. Вид ресурса хранится в поле «Вид».</p>
<pre><code>CREATE TABLE `Номенклатура` (
  `КодРесурса` VARCHAR(32) NOT NULL,
  `Код` VARCHAR(32) NOT NULL,
  `Наименование` VARCHAR(255) NOT NULL,
  `Вид` VARCHAR(24) NOT NULL,
  `Единица` VARCHAR(16) NOT NULL,
  PRIMARY KEY (`КодРесурса`),
  UNIQUE KEY `uq_nomenklatura_kod` (`Код`),
  CONSTRAINT `ck_nomenklatura_vid`
    CHECK (`Вид` IN ('Товар', 'Материал', 'Операция'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="Цены">
<h4>3. <code>Цены</code></h4>
<p>Цена ресурса на дату. Ключ составной: ресурс и дата начала действия.</p>
<pre><code>CREATE TABLE `Цены` (
  `КодРесурса` VARCHAR(32) NOT NULL,
  `ДатаНачала` DATE NOT NULL,
  `Цена` DECIMAL(14,2) NOT NULL,
  PRIMARY KEY (`КодРесурса`, `ДатаНачала`),
  CONSTRAINT `ck_ceny` CHECK (`Цена` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="Спецификации">
<h4>4. <code>Спецификации</code></h4>
<p>Шапка рецепта изделия: изделие, изготовитель и количество выпуска.</p>
<pre><code>CREATE TABLE `Спецификации` (
  `КодСпецификации` VARCHAR(32) NOT NULL,
  `КодИзделия` VARCHAR(32) NOT NULL,
  `Наименование` VARCHAR(255) NOT NULL,
  `КоличествоВыпуска` DECIMAL(14,3) NOT NULL,
  `КодИзготовителя` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`КодСпецификации`),
  UNIQUE KEY `uq_spec_izdelie` (`КодИзделия`),
  CONSTRAINT `ck_spec_vyput` CHECK (`КоличествоВыпуска` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="СоставСпецификации">
<h4>5. <code>СоставСпецификации</code></h4>
<p>Строки состава: ресурс, норма расхода и норма времени.</p>
<pre><code>CREATE TABLE `СоставСпецификации` (
  `КодСпецификации` VARCHAR(32) NOT NULL,
  `КодРесурса` VARCHAR(32) NOT NULL,
  `Количество` DECIMAL(14,3) NOT NULL DEFAULT 0,
  `НормаВремени` DECIMAL(14,3) NOT NULL DEFAULT 0,
  PRIMARY KEY (`КодСпецификации`, `КодРесурса`),
  CONSTRAINT `ck_sostav`
    CHECK (`Количество` >= 0 AND `НормаВремени` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="ЗаказыПокупателя">
<h4>6. <code>ЗаказыПокупателя</code></h4>
<p>Шапка заказа покупателя: номер, дата, заказчик и исполнитель.</p>
<pre><code>CREATE TABLE `ЗаказыПокупателя` (
  `КодЗаказа` VARCHAR(32) NOT NULL,
  `НомерДокумента` VARCHAR(32) NOT NULL,
  `ДатаДокумента` DATE NOT NULL,
  `КодЗаказчика` VARCHAR(32) NOT NULL,
  `КодИсполнителя` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`КодЗаказа`),
  UNIQUE KEY `uq_zakaz_nomer` (`НомерДокумента`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="СтрокиЗаказа">
<h4>7. <code>СтрокиЗаказа</code></h4>
<p>Строки заказа: товар, количество, цена продажи и скидка.</p>
<pre><code>CREATE TABLE `СтрокиЗаказа` (
  `КодСтроки` VARCHAR(32) NOT NULL,
  `КодЗаказа` VARCHAR(32) NOT NULL,
  `КодТовара` VARCHAR(32) NOT NULL,
  `Количество` DECIMAL(14,3) NOT NULL,
  `ЦенаПродажи` DECIMAL(14,2) NOT NULL,
  `Скидка` DECIMAL(14,2) NOT NULL DEFAULT 0,
  PRIMARY KEY (`КодСтроки`),
  CONSTRAINT `ck_stroka`
    CHECK (`Количество` > 0 AND `ЦенаПродажи` >= 0 AND `Скидка` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="ЗаказыНаПроизводство">
<h4>8. <code>ЗаказыНаПроизводство</code></h4>
<p>Шапка производственного заказа: номер, даты и подразделение.</p>
<pre><code>CREATE TABLE `ЗаказыНаПроизводство` (
  `КодПроизводственногоЗаказа` VARCHAR(32) NOT NULL,
  `НомерДокумента` VARCHAR(32) NOT NULL,
  `ДатаДокумента` DATE NOT NULL,
  `ДатаЗапуска` DATE NOT NULL,
  `Подразделение` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`КодПроизводственногоЗаказа`),
  UNIQUE KEY `uq_proizv_nomer` (`НомерДокумента`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="ПродукцияКВыпуску">
<h4>9. <code>ПродукцияКВыпуску</code></h4>
<p>Что выпускаем по производственному заказу.</p>
<pre><code>CREATE TABLE `ПродукцияКВыпуску` (
  `КодПроизводственногоЗаказа` VARCHAR(32) NOT NULL,
  `КодТовара` VARCHAR(32) NOT NULL,
  `Количество` DECIMAL(14,3) NOT NULL,
  PRIMARY KEY (`КодПроизводственногоЗаказа`, `КодТовара`),
  CONSTRAINT `ck_produkciya` CHECK (`Количество` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="РесурсыПроизводства">
<h4>10. <code>РесурсыПроизводства</code></h4>
<p>Плановый расход материалов и времени по заказу.</p>
<pre><code>CREATE TABLE `РесурсыПроизводства` (
  `КодПроизводственногоЗаказа` VARCHAR(32) NOT NULL,
  `КодРесурса` VARCHAR(32) NOT NULL,
  `Количество` DECIMAL(14,3) NOT NULL DEFAULT 0,
  `НормаВремени` DECIMAL(14,3) NOT NULL DEFAULT 0,
  PRIMARY KEY (`КодПроизводственногоЗаказа`, `КодРесурса`),
  CONSTRAINT `ck_resursy`
    CHECK (`Количество` >= 0 AND `НормаВремени` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="Пользователи">
<h4>11. <code>Пользователи</code></h4>
<p>Учётные записи приложения: логин, хеш, соль, роль и блокировка.</p>
<pre><code>CREATE TABLE `Пользователи` (
  `КодПользователя` INT NOT NULL AUTO_INCREMENT,
  `Логин` VARCHAR(64) NOT NULL,
  `ХешПароля` VARCHAR(128) NOT NULL,
  `Соль` VARCHAR(64) NOT NULL,
  `Роль` VARCHAR(24) NOT NULL DEFAULT 'Пользователь',
  `ЧислоОшибок` INT NOT NULL DEFAULT 0,
  `Заблокирован` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`КодПользователя`),
  UNIQUE KEY `uq_polzovateli_login` (`Логин`),
  CONSTRAINT `ck_polzovateli_rol`
    CHECK (`Роль` IN ('Администратор', 'Пользователь'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
<article class="schema-slide" aria-label="Заметки">
<h4>12. <code>Заметки</code></h4>
<p>Заметки сотрудников со ссылкой на автора.</p>
<pre><code>CREATE TABLE `Заметки` (
  `КодЗаметки` INT NOT NULL AUTO_INCREMENT,
  `Заголовок` VARCHAR(255) NOT NULL,
  `Содержание` TEXT NOT NULL,
  `КодПользователя` INT NOT NULL,
  `ДатаСоздания` DATE NOT NULL,
  PRIMARY KEY (`КодЗаметки`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;</code></pre>
</article>
</div>
</div>

После выполнения проверьте левую панель: в базе `dkip2027_v03` должно появиться двенадцать таблиц.

### Шаг 4. Добавьте связи

Выполните `V03_mysql_fk.sql`. Скрипт добавляет четырнадцать внешних ключей. Если MySQL сообщает об ошибке, сравните тип и имя поля с `CREATE TABLE`: внешний ключ и первичный ключ должны иметь одинаковый тип.

| Связь | Откуда | Куда |
|---:|---|---|
| 1 | `Цены.КодРесурса` | `Номенклатура.КодРесурса` |
| 2 | `Спецификации.КодИзделия` | `Номенклатура.КодРесурса` |
| 3 | `Спецификации.КодИзготовителя` | `Заказчики.КодЗаказчика` |
| 4 | `СоставСпецификации.КодСпецификации` | `Спецификации.КодСпецификации` |
| 5 | `СоставСпецификации.КодРесурса` | `Номенклатура.КодРесурса` |
| 6 | `ЗаказыПокупателя.КодЗаказчика` | `Заказчики.КодЗаказчика` |
| 7 | `ЗаказыПокупателя.КодИсполнителя` | `Заказчики.КодЗаказчика` |
| 8 | `СтрокиЗаказа.КодЗаказа` | `ЗаказыПокупателя.КодЗаказа` |
| 9 | `СтрокиЗаказа.КодТовара` | `Номенклатура.КодРесурса` |
| 10 | `ПродукцияКВыпуску.КодПроизводственногоЗаказа` | `ЗаказыНаПроизводство.КодПроизводственногоЗаказа` |
| 11 | `ПродукцияКВыпуску.КодТовара` | `Номенклатура.КодРесурса` |
| 12 | `РесурсыПроизводства.КодПроизводственногоЗаказа` | `ЗаказыНаПроизводство.КодПроизводственногоЗаказа` |
| 13 | `РесурсыПроизводства.КодРесурса` | `Номенклатура.КодРесурса` |
| 14 | `Заметки.КодПользователя` | `Пользователи.КодПользователя` |

### Шаг 5. Загрузите заказчиков из JSON

В `Заказчики.json` шесть записей. Коды начинаются с нулей, поэтому `КодЗаказчика` имеет тип `VARCHAR(32)`, а не число. Импортируйте JSON в таблицу `Заказчики`, затем добавьте изготовителя «Мастерская «Глина»» отдельной строкой с кодом `M-001`, потому что в JSON его нет. Если импорт JSON в phpMyAdmin неудобен, выполните `V03_mysql_customers.sql`: в нём те же шесть покупателей и изготовитель.

Проверка:

```sql
SELECT COUNT(*) AS `Заказчиков` FROM `Заказчики`;
-- 7: шесть покупателей и изготовитель
SELECT `КодЗаказчика`
FROM `Заказчики`
WHERE `КодЗаказчика` LIKE '003%'
ORDER BY `КодЗаказчика`;
-- коды сохранили ведущие нули
```

### Шаг 6. Загрузите остальные данные

Выполните `V03_mysql_data.sql`. Скрипт вставляет остальные данные: номенклатуру, цены, спецификацию, состав, заказ, строку заказа, производственный заказ, продукцию, ресурсы, пользователей и заметки. Заказчиков в нём нет: они уже загружены на предыдущем шаге.

| Таблица | Строк | Что внутри |
|---|---:|---|
| `Номенклатура` | 6 | изделие, три материала, две операции |
| `Цены` | 5 | цены на 01.03.2027 |
| `Спецификации` | 1 | «Кружка 300 мл» |
| `СоставСпецификации` | 5 | три материала и две операции |
| `ЗаказыПокупателя` | 1 | V03-01 |
| `СтрокиЗаказа` | 1 | 18 единиц по 700 |
| `ЗаказыНаПроизводство` | 1 | V03-P01 |
| `ПродукцияКВыпуску` | 1 | 18 единиц |
| `РесурсыПроизводства` | 5 | материалы и операции |
| `Пользователи` | 4 | admin, manager, technologist, master |
| `Заметки` | 5 | записи из `Заметки.json` |

### Шаг 7. Проверьте данные

Сверьте количество строк и ссылки. Эти запросы должны вернуть указанные числа и ноль «сиротских» строк.

```sql
SELECT COUNT(*) AS `Номенклатура` FROM `Номенклатура`;        -- 6
SELECT COUNT(*) AS `Цены` FROM `Цены`;                        -- 5
SELECT COUNT(*) AS `Состав` FROM `СоставСпецификации`;        -- 5
SELECT COUNT(*) AS `Ресурсы` FROM `РесурсыПроизводства`;      -- 5

SELECT COUNT(*) AS `СтрокиБезТовара`
FROM `СтрокиЗаказа` ст
LEFT JOIN `Номенклатура` н ON н.`КодРесурса` = ст.`КодТовара`
WHERE н.`КодРесурса` IS NULL;                                  -- 0

SELECT COUNT(*) AS `СтрокиБезЗаказа`
FROM `СтрокиЗаказа` ст
LEFT JOIN `ЗаказыПокупателя` з ON з.`КодЗаказа` = ст.`КодЗаказа`
WHERE з.`КодЗаказа` IS NULL;                                   -- 0
```

### Шаг 8. Сделайте выгрузку и восстановите её

В phpMyAdmin выберите базу `dkip2027_v03`, откройте `Экспорт`, формат `SQL`, и сохраните файл `V03_выгрузка.sql`. Затем создайте пустую базу `dkip2027_v03_check`, импортируйте в неё файл и проверьте, что появились двенадцать таблиц и все строки. Это доказывает, что база переносится на другой компьютер.

## Задание 3. SQL-запрос стоимости

Нормативная стоимость заказа V03-01 считается по формуле из условия:

- материал: количество выпуска × норма расхода × цена;
- операция: количество выпуска × норма времени × тариф за час;
- промежуточные суммы не округляются, итог округляется до копеек.

Количество выпуска берётся из строки заказа: 18 единиц. Норма расхода и норма времени лежат в `СоставСпецификации`, цена на 01.03.2027 в `Цены`. Запрос соединяет заказ, строку, спецификацию, состав, номенклатуру и цены.

```sql
SELECT
  н.`Наименование` AS `Ресурс`,
  н.`Вид` AS `Вид`,
  сс.`Количество` AS `Норма`,
  сс.`НормаВремени` AS `Часы`,
  ц.`Цена` AS `Цена`,
  ROUND(
    CASE
      WHEN н.`Вид` = 'Материал'
        THEN ст.`Количество` * сс.`Количество` * ц.`Цена`
      ELSE ст.`Количество` * сс.`НормаВремени` * ц.`Цена`
    END,
    2
  ) AS `Стоимость`
FROM `ЗаказыПокупателя` з
JOIN `СтрокиЗаказа` ст
  ON ст.`КодЗаказа` = з.`КодЗаказа`
JOIN `Спецификации` сп
  ON сп.`КодИзделия` = ст.`КодТовара`
JOIN `СоставСпецификации` сс
  ON сс.`КодСпецификации` = сп.`КодСпецификации`
JOIN `Номенклатура` н
  ON н.`КодРесурса` = сс.`КодРесурса`
JOIN `Цены` ц
  ON ц.`КодРесурса` = сс.`КодРесурса`
 AND ц.`ДатаНачала` = '2027-03-01'
WHERE з.`НомерДокумента` = 'V03-01'
ORDER BY н.`Вид` DESC, н.`Наименование`;
```

`CASE` выбирает формулу: для материала умножает норму расхода, для операции норму времени. `ROUND(..., 2)` округляет только стоимость строки, а итог считается отдельным запросом.

Результат по строкам:

| Ресурс | Вид | Норма | Часы | Цена | Стоимость |
|---|---|---:|---:|---:|---:|
| Глина | Материал | 0,450 | 0,000 | 120,00 | 972,00 |
| Глазурь | Материал | 0,030 | 0,000 | 950,00 | 513,00 |
| Коробка | Материал | 1,000 | 0,000 | 40,00 | 720,00 |
| Формовка | Операция | 0,000 | 0,400 | 750,00 | 5 400,00 |
| Глазурование и обжиг | Операция | 0,000 | 0,150 | 900,00 | 2 430,00 |
| **Итого** |  |  |  |  | **10 035,00** |

Итоговый запрос:

```sql
SELECT
  ROUND(SUM(
    CASE
      WHEN н.`Вид` = 'Материал'
        THEN ст.`Количество` * сс.`Количество` * ц.`Цена`
      ELSE ст.`Количество` * сс.`НормаВремени` * ц.`Цена`
    END
  ), 2) AS `Итого`
FROM `ЗаказыПокупателя` з
JOIN `СтрокиЗаказа` ст
  ON ст.`КодЗаказа` = з.`КодЗаказа`
JOIN `Спецификации` сп
  ON сп.`КодИзделия` = ст.`КодТовара`
JOIN `СоставСпецификации` сс
  ON сс.`КодСпецификации` = сп.`КодСпецификации`
JOIN `Номенклатура` н
  ON н.`КодРесурса` = сс.`КодРесурса`
JOIN `Цены` ц
  ON ц.`КодРесурса` = сс.`КодРесурса`
 AND ц.`ДатаНачала` = '2027-03-01'
WHERE з.`НомерДокумента` = 'V03-01';
```

Запрос возвращает `10035.00`. Если получилось другое число, проверьте дату цены, количество в строке заказа и то, что у материалов `НормаВремени` равна нулю, а у операций `Количество` равна нулю.

## Файлы решения V03

<div class="files">
<b class="label">Скрипты V03</b>
<a href="reports/prep/sql/V03_mysql_tables.sql">V03_mysql_tables.sql</a>
<a href="reports/prep/sql/V03_mysql_fk.sql">V03_mysql_fk.sql</a>
<a href="reports/prep/sql/V03_mysql_customers.sql">V03_mysql_customers.sql</a>
<a href="reports/prep/sql/V03_mysql_data.sql">V03_mysql_data.sql</a>
<a href="reports/prep/sql/V03_cost.sql">V03_cost.sql</a>
</div>

## Чек-лист V03

- На диаграмме двенадцать таблиц с русскими названиями и четырнадцать связей.
- У каждой таблицы есть первичный ключ, у связей стоят маркеры кратности.
- В базе `dkip2027_v03` двенадцать таблиц и четырнадцать внешних ключей.
- Шесть заказчиков из JSON сохранили ведущие нули, изготовитель добавлен отдельной строкой.
- Заказ V03-01, строка на 18 единиц, спецификация и цены загружены.
- SQL-запрос показывает материалы и операции отдельными строками и итог `10 035,00`.
- Выгрузка базы восстанавливается в пустую базу без ошибок.
