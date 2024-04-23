from db import db
import users
from sqlalchemy.sql import text

def get_task_list(user_id):
    if user_id == 0:
        return []
    sql = text("SELECT * FROM tasks WHERE user_id=:user_id ORDER BY id DESC") #muokkaa kyselyä
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()

def create_task(title, description, date, due_date, priority, category_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO tasks (user_id, title, description, date, due_date, priority, category_id) VALUES (:user_id, :title, :description, :date, :due_date, :priority, :category_id)")
    db.session.execute(sql, {"user_id": user_id, "title": title, "description": description, "date": date, "due_date": due_date, "priority": priority, "category_id": category_id})
    db.session.commit()
    return True

def edit_task(task_id, title, description, date, due_date, priority, category_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try: #jos arvo on 'None', käytetään tehtävän nykyistä arvoa tietokannassa
        sql = text("UPDATE tasks SET title = COALESCE(:title, title), description = COALESCE(:description, description), due_date = COALESCE(:due_date, due_date), priority = COALESCE(:priority, priority), category_id = :category_id WHERE id = :task_id AND user_id = :user_id")
        db.session.execute(sql, {"title": title, "description": description, "date": date, "due_date": due_date, "priority": priority, "category_id": category_id, "task_id": task_id, "user_id": user_id})
        db.session.commit()
        return True
    except:
        return False

def delete_task(task_id, user_id):
    sql = text("DELETE FROM tasks WHERE id=:task_id AND user_id=:user_id")
    db.session.execute(sql, {"task_id": task_id, "user_id": user_id})
    db.session.commit()

def get_task_from_database(task_id):
    sql = text("SELECT * FROM tasks WHERE id=:task_id")
    result = db.session.execute(sql, {"task_id": task_id})
    task = result.fetchone()
    return task

def get_sorted_tasks_by_priority(user_id):
    sql = text("SELECT id, title, description, date, due_date, priority, category_id FROM tasks WHERE user_id=:user_id ORDER BY priority ASC")
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()

def get_sorted_tasks_by_date(user_id):
    sql = text("SELECT id, title, description, date, due_date, priority, category_id FROM tasks WHERE user_id=:user_id ORDER BY due_date ASC")
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()
