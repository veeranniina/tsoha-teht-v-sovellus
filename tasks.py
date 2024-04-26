from db import db
import users
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

def get_task_list(user_id):
    try:
        if user_id == 0:
            return []
        sql = text("SELECT * FROM tasks WHERE user_id=:user_id ORDER BY id DESC")
        result = db.session.execute(sql, {"user_id": user_id})
        return result.fetchall()
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")
        return []

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
    try:
        sql = text("UPDATE tasks SET title = COALESCE(:title, title), description = COALESCE(:description, description), due_date = COALESCE(:due_date, due_date), priority = COALESCE(:priority, priority), category_id = :category_id WHERE id = :task_id AND user_id = :user_id") 
        db.session.execute(sql, {"title": title, "description": description, "date": date, "due_date": due_date, "priority": priority, "category_id": category_id, "task_id": task_id, "user_id": user_id})
        db.session.commit()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False

def delete_task_to_recycle_bin(task_id, user_id):
    try:
        #poistetaan ensin muistutukset
        sql_delete_reminders = text("DELETE FROM reminders WHERE task_id=:task_id")
        db.session.execute(sql_delete_reminders, {"task_id": task_id})
        db.session.commit()

        #haetaan poistettava muistiinpano
        sql_select_task = text("SELECT id, title, description, date, due_date, priority, category_id FROM tasks WHERE id=:task_id AND user_id=:user_id")
        result = db.session.execute(sql_select_task, {"task_id": task_id, "user_id": user_id})
        task = result.fetchone()

        if task:
            #lisätään poistettu tehtävä recycle_bin-tauluun
            deletion_timestamp = datetime.now()
            sql_insert_recycle_bin = text("INSERT INTO recycle_bin (user_id, task_id, deletion_timestamp) VALUES (:user_id, :task_id, :deletion_timestamp)")
            db.session.execute(sql_insert_recycle_bin, {"user_id": user_id, "task_id": task_id, "deletion_timestamp": deletion_timestamp})
            db.session.commit()

            #poistetaan tehtävä tasks-taulusta
            sql_delete_task = text("DELETE FROM tasks WHERE id=:task_id AND user_id=:user_id")
            db.session.execute(sql_delete_task, {"task_id": task_id, "user_id": user_id})
            db.session.commit()
            
            return True
        else:
            return False
    except Exception as e:
        print(f"Database error: {e}")
        return False

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
