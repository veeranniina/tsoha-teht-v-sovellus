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
    category_id REFERENCES categories,
    status_id INTEGER REFERENCES status
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

CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE recurrence (
    id SERIAL PRIMARY KEY, 
    task_id INTEGER REFERENCES tasks, 
    frequency INTERVAL, 
    start_date TIMESTAMP, 
    end_date TIMESTAMP, 
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);


INSERT INTO categories (user_id, name) VALUES (NULL, 'Ei kategoriaa');       <----Tämä luo tauluun oman rivin edustamaan "ei kategoriaa" -tilaa.
INSERT INTO status (id, name) VALUES (1, 'valmis'), (2, 'kesken'), (3, 'ei statusta');