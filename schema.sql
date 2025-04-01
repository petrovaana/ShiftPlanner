CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    start_price INTEGER,
    pvm DATE,
    user_id INTEGER REFERENCES users
);

CREATE TABLE puuttuvat (
    id INTEGER PRIMARY KEY,
    tuote TEXT,
    paiva DATE
);