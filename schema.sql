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

CREATE TABLE reminders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    task_id INTEGER REFERENCES tasks,
    reminder_date TIMESTAMP,
    reminder_message TEXT
);




<-------INSERT INTO categories (user_id, name) VALUES (NULL, 'Ei kategoriaa');       Tämä luo tauluun oman rivin edustamaan "ei kategoriaa" -tilaa.