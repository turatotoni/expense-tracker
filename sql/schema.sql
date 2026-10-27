DROP TABLE IF EXISTS expenses, categories, users CASCADE;

CREATE TABLE users (
    id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE categories (
    id      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name    VARCHAR(100) NOT NULL,
    UNIQUE (user_id, name)
);

CREATE TABLE expenses (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id BIGINT NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    amount      NUMERIC(12,2) NOT NULL CHECK (amount > 0),
    currency    CHAR(3) NOT NULL DEFAULT 'EUR',
    description VARCHAR(255),
    spent_on    DATE NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_expenses_user_date ON expenses (user_id, spent_on);
CREATE INDEX idx_expenses_category  ON expenses (category_id);