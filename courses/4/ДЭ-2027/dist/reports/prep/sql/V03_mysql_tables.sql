CREATE DATABASE IF NOT EXISTS `dkip2027_v03`
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `dkip2027_v03`;

CREATE TABLE `Заказчики` (
  `КодЗаказчика` VARCHAR(32) NOT NULL,
  `Наименование` VARCHAR(255) NOT NULL,
  `ИНН` VARCHAR(20) NOT NULL DEFAULT '',
  `Адрес` VARCHAR(500) NOT NULL,
  `Телефон` VARCHAR(64) NOT NULL,
  `Тип` VARCHAR(24) NOT NULL,
  PRIMARY KEY (`КодЗаказчика`),
  CONSTRAINT `ck_zakazchiki_tip`
    CHECK (`Тип` IN ('Покупатель', 'Поставщик', 'Изготовитель'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Номенклатура` (
  `КодРесурса` VARCHAR(32) NOT NULL,
  `Код` VARCHAR(32) NOT NULL,
  `Наименование` VARCHAR(255) NOT NULL,
  `Вид` VARCHAR(24) NOT NULL,
  `Единица` VARCHAR(16) NOT NULL,
  PRIMARY KEY (`КодРесурса`),
  UNIQUE KEY `uq_nomenklatura_kod` (`Код`),
  CONSTRAINT `ck_nomenklatura_vid`
    CHECK (`Вид` IN ('Товар', 'Материал', 'Операция'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Цены` (
  `КодРесурса` VARCHAR(32) NOT NULL,
  `ДатаНачала` DATE NOT NULL,
  `Цена` DECIMAL(14,2) NOT NULL,
  PRIMARY KEY (`КодРесурса`, `ДатаНачала`),
  CONSTRAINT `ck_ceny` CHECK (`Цена` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Спецификации` (
  `КодСпецификации` VARCHAR(32) NOT NULL,
  `КодИзделия` VARCHAR(32) NOT NULL,
  `Наименование` VARCHAR(255) NOT NULL,
  `КоличествоВыпуска` DECIMAL(14,3) NOT NULL,
  `КодИзготовителя` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`КодСпецификации`),
  UNIQUE KEY `uq_spec_izdelie` (`КодИзделия`),
  CONSTRAINT `ck_spec_vyput` CHECK (`КоличествоВыпуска` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `СоставСпецификации` (
  `КодСпецификации` VARCHAR(32) NOT NULL,
  `КодРесурса` VARCHAR(32) NOT NULL,
  `Количество` DECIMAL(14,3) NOT NULL DEFAULT 0,
  `НормаВремени` DECIMAL(14,3) NOT NULL DEFAULT 0,
  PRIMARY KEY (`КодСпецификации`, `КодРесурса`),
  CONSTRAINT `ck_sostav`
    CHECK (`Количество` >= 0 AND `НормаВремени` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `ЗаказыПокупателя` (
  `КодЗаказа` VARCHAR(32) NOT NULL,
  `НомерДокумента` VARCHAR(32) NOT NULL,
  `ДатаДокумента` DATE NOT NULL,
  `КодЗаказчика` VARCHAR(32) NOT NULL,
  `КодИсполнителя` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`КодЗаказа`),
  UNIQUE KEY `uq_zakaz_nomer` (`НомерДокумента`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `СтрокиЗаказа` (
  `КодСтроки` VARCHAR(32) NOT NULL,
  `КодЗаказа` VARCHAR(32) NOT NULL,
  `КодТовара` VARCHAR(32) NOT NULL,
  `Количество` DECIMAL(14,3) NOT NULL,
  `ЦенаПродажи` DECIMAL(14,2) NOT NULL,
  `Скидка` DECIMAL(14,2) NOT NULL DEFAULT 0,
  PRIMARY KEY (`КодСтроки`),
  CONSTRAINT `ck_stroka`
    CHECK (`Количество` > 0 AND `ЦенаПродажи` >= 0 AND `Скидка` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `ЗаказыНаПроизводство` (
  `КодПроизводственногоЗаказа` VARCHAR(32) NOT NULL,
  `НомерДокумента` VARCHAR(32) NOT NULL,
  `ДатаДокумента` DATE NOT NULL,
  `ДатаЗапуска` DATE NOT NULL,
  `Подразделение` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`КодПроизводственногоЗаказа`),
  UNIQUE KEY `uq_proizv_nomer` (`НомерДокумента`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `ПродукцияКВыпуску` (
  `КодПроизводственногоЗаказа` VARCHAR(32) NOT NULL,
  `КодТовара` VARCHAR(32) NOT NULL,
  `Количество` DECIMAL(14,3) NOT NULL,
  PRIMARY KEY (`КодПроизводственногоЗаказа`, `КодТовара`),
  CONSTRAINT `ck_produkciya` CHECK (`Количество` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `РесурсыПроизводства` (
  `КодПроизводственногоЗаказа` VARCHAR(32) NOT NULL,
  `КодРесурса` VARCHAR(32) NOT NULL,
  `Количество` DECIMAL(14,3) NOT NULL DEFAULT 0,
  `НормаВремени` DECIMAL(14,3) NOT NULL DEFAULT 0,
  PRIMARY KEY (`КодПроизводственногоЗаказа`, `КодРесурса`),
  CONSTRAINT `ck_resursy`
    CHECK (`Количество` >= 0 AND `НормаВремени` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Пользователи` (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Заметки` (
  `КодЗаметки` INT NOT NULL AUTO_INCREMENT,
  `Заголовок` VARCHAR(255) NOT NULL,
  `Содержание` TEXT NOT NULL,
  `КодПользователя` INT NOT NULL,
  `ДатаСоздания` DATE NOT NULL,
  PRIMARY KEY (`КодЗаметки`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
