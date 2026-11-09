-- V02. Нормативная стоимость заказа V02-01.
USE dkip2027_v02;

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
