-- 1. Svi troškovi korisnika 1 s imenom kategorije (JOIN)
SELECT e.spent_on, c.name AS category, e.amount, e.description
FROM expenses e
JOIN categories c ON c.id = e.category_id
WHERE e.user_id = 1
ORDER BY e.spent_on DESC;

-- 2. Ukupno po kategoriji za određeni mjesec (GROUP BY)
SELECT c.name, SUM(e.amount) AS total
FROM expenses e
JOIN categories c ON c.id = e.category_id
WHERE e.user_id = 1
  AND e.spent_on >= '2026-09-01' AND e.spent_on < '2026-10-01'
GROUP BY c.name
ORDER BY total DESC;

-- 3. Ukupno po mjesecima
SELECT date_trunc('month', spent_on)::date AS month, SUM(amount) AS total
FROM expenses
WHERE user_id = 1
GROUP BY month
ORDER BY month;

-- 4. Kategorije u kojima je potrošeno više od 100 EUR (HAVING)
SELECT c.name, SUM(e.amount) AS total
FROM expenses e
JOIN categories c ON c.id = e.category_id
WHERE e.user_id = 1
GROUP BY c.name
HAVING SUM(e.amount) > 100;

-- 5. Kategorije bez ijednog troška (LEFT JOIN)
SELECT c.name
FROM categories c
LEFT JOIN expenses e ON e.category_id = c.id
WHERE c.user_id = 1 AND e.id IS NULL;

-- 6. Prosječni trošak i broj troškova po kategoriji
SELECT c.name, COUNT(*) AS num, ROUND(AVG(e.amount), 2) AS avg_amount
FROM expenses e
JOIN categories c ON c.id = e.category_id
WHERE e.user_id = 1
GROUP BY c.name;

-- 7. Postotak ukupne potrošnje po kategoriji (window funkcija)
SELECT c.name,
       SUM(e.amount) AS total,
       ROUND(100 * SUM(e.amount) / SUM(SUM(e.amount)) OVER (), 1) AS percent
FROM expenses e
JOIN categories c ON c.id = e.category_id
WHERE e.user_id = 1
GROUP BY c.name;

-- 8. Najskuplji pojedinačni trošak svakog korisnika
SELECT user_id, MAX(amount) AS max_amount
FROM expenses
GROUP BY user_id;

