CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    booked_space TEXT,
    guests INTEGER,
    payment TEXT,
    start_price INTEGER,
    date DATE,
    user_id INTEGER REFERENCES users
);

CREATE TABLE edits (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    user_id INTEGER REFERENCES users,
    description TEXT
);

CREATE TABLE missing_items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    date DATE,
    user_id INTEGER REFERENCES users
);

CREATE TABLE wastage (
    id INTEGER PRIMARY KEY,
    title TEXT
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE wastage_classes (
    id INTEGER PRIMARY KEY,
    wastage_id INTEGER REFERENCES wastage,
    title TEXT,
    value TEXT
);
