CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin BOOLEAN
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY, 
    user_id INTEGER REFERENCES users, 
    title TEXT, 
    description TEXT, 
    date TIMESTAMP, 
    due_date TEXT, 
    priority INTEGER, 
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY, 
    user_id INTEGER REFERENCES users, 
    name TEXT
);