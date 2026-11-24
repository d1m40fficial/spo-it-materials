-- Схема данных учебного продукта «Заявки колледжа».
-- Дополните таблицы и ограничения. Одна таблица дана как образец.

PRAGMA foreign_keys = ON;

CREATE TABLE employee (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    room TEXT NOT NULL
);

-- Добавьте таблицы request, executor, comment.
-- У каждой таблицы должен быть первичный ключ.
-- Связи оформите внешними ключами.
-- Статус заявки ограничьте допустимыми значениями.
