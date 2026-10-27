INSERT INTO users (email, password_hash) VALUES
  ('ana@example.com', 'hash1'),
  ('ivan@example.com', 'hash2');

INSERT INTO categories (user_id, name) VALUES
  (1, 'Hrana'), (1, 'Prijevoz'), (1, 'Zabava'), (1, 'Stanarina'),
  (2, 'Hrana'), (2, 'Prijevoz');

INSERT INTO expenses (user_id, category_id, amount, description, spent_on) VALUES
  (1, 1,  45.30, 'Tjedna nabava',   '2026-09-03'),
  (1, 1,  12.50, 'Ručak',           '2026-09-10'),
  (1, 2,  30.00, 'Mjesečna karta',  '2026-09-01'),
  (1, 3,  18.00, 'Kino',            '2026-09-14'),
  (1, 4, 400.00, 'Stanarina',       '2026-09-05'),
  (1, 1,  52.10, 'Tjedna nabava',   '2026-10-02'),
  (1, 2,  30.00, 'Mjesečna karta',  '2026-10-01'),
  (1, 4, 400.00, 'Stanarina',       '2026-10-05'),
  (2, 5,  38.70, 'Nabava',          '2026-10-04'),
  (2, 6,  25.00, 'Gorivo',          '2026-10-06');