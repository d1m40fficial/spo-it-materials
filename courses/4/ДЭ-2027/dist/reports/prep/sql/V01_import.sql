CREATE TABLE json_import (payload TEXT);

INSERT INTO json_import(payload) VALUES ('[{"id": "001000001", "name": "Магазин «Стежок-1»", "inn": "", "addres": "Учебный город, улица Производственная, 1, офис 1", "phone": "+79990010001", "type": "Покупатель"}, {"id": "001000002", "name": "Торговый дом «Стежок-2»", "inn": "", "addres": "Учебный город, улица Производственная, 1, офис 2", "phone": "+79990010002", "type": "Покупатель"}, {"id": "001000003", "name": "Студия «Стежок-3»", "inn": "", "addres": "Учебный город, улица Производственная, 1, офис 3", "phone": "+79990010003", "type": "Покупатель"}, {"id": "001000004", "name": "Магазин подарков «Стежок-4»", "inn": "", "addres": "Учебный город, улица Производственная, 1, офис 4", "phone": "+79990010004", "type": "Покупатель"}, {"id": "001000005", "name": "Мастерская «Стежок-5»", "inn": "", "addres": "Учебный город, улица Производственная, 1, офис 5", "phone": "+79990010005", "type": "Покупатель"}, {"id": "001000006", "name": "Оптовый склад «Стежок-6»", "inn": "", "addres": "Учебный город, улица Производственная, 1, офис 6", "phone": "+79990010006", "type": "Покупатель"}]');

INSERT INTO counterparty (id, name, inn, address, phone, party_type)
SELECT json_extract(value, '$.id'),
       json_extract(value, '$.name'),
       json_extract(value, '$.inn'),
       json_extract(value, '$.addres'),
       json_extract(value, '$.phone'),
       json_extract(value, '$.type')
FROM json_import, json_each(json_import.payload);

SELECT id, name, phone, party_type FROM counterparty ORDER BY id;
