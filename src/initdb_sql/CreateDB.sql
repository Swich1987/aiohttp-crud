CREATE TABLE clients(
    id SERIAL PRIMARY KEY,
    name VARCHAR (150),
    address VARCHAR (200)
);

CREATE TABLE distributors(
    id SERIAL PRIMARY KEY,
    name VARCHAR (150),
    address VARCHAR (200)
);

CREATE TABLE goods(
    id SERIAL PRIMARY KEY,
    name VARCHAR (150),
    client_id INT REFERENCES clients(id),
    distributor_id INT REFERENCES distributors(id)
);

INSERT INTO clients (name, address) VALUES
    ('Иванов', 'г.Москва'),
    ('Петров', 'г.Белгород'),
    ('Сидоров', 'г.Санкт-Петербург');

INSERT INTO distributors (name, address) VALUES
    ('Пятерочка', 'г.Москва'),
    ('Магнит', 'г.Белгород'),
    ('Линия', 'г.Санкт-Петербург');

INSERT INTO goods (name, client_id, distributor_id) VALUES
    ('Snickers', 2, 2),
    ('Bounty', 1, 3),
    ('KitKat', 1, 2),
    ('Nestle', 3, 3),
    ('AlpenGold', 3, 1);
