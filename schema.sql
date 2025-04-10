CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    pax INTEGER,
    maksutapa TEXT,
    start_price INTEGER,
    pvm DATE,
    user_id INTEGER REFERENCES users
);

CREATE TABLE muokkaukset (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    user_id INTEGER REFERENCES users,
    description TEXT
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE item_classes (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    title TEXT,
    value TEXT
);