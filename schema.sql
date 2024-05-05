CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY, 
    user_id INTEGER REFERENCES users, 
    title TEXT, 
    description TEXT, 
    date TIMESTAMP, 
    due_date TEXT, 
    priority INTEGER, 
    category_id REFERENCES categories
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

CREATE TABLE recycle_bin ( 
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    task_id INTEGER REFERENCES tasks, 
    deletion_timestamp TIMESTAMP 
);


INSERT INTO categories (user_id, name) VALUES (NULL, 'Ei kategoriaa');       <----Tämä luo tauluun oman rivin edustamaan "ei kategoriaa" -tilaa.
