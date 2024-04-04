from db import db
import users
from sqlalchemy.sql import text

def get_task_list(user_id):
    #if user_id == 0:
        #return []
    sql = text("SELECT * FROM tasks WHERE user_id=:user_id ORDER BY id DESC")
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()

def create_task(title, description, date, due_date, priority):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO tasks (user_id, title, description, date, due_date, priority) VALUES (:user_id, :title, :description, :date, :due_date, :priority)")
    db.session.execute(sql, {"user_id": user_id, "title": title, "description": description, "date": date, "due_date": due_date, "priority": priority})
    db.session.commit()
    return True

def update_task(task_id, title, description, date, due_date, priority):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try: #jos arvo on 'None', käytetään tehtävän nykyistä arvoa tietokannassa
        sql = text("UPDATE tasks SET title = COALESCE(:title, title), description = COALESCE(:description, description), due_date = COALESCE(:due_date, due_date), priority = COALESCE(:priority, priority) WHERE id = :task_id AND user_id = :user_id")
        db.session.execute(sql, {"title": title, "description": description, "date": date, "due_date": due_date, "priority": priority, "task_id": task_id, "user_id": user_id})
        db.session.commit()
        return True
    except:
        return False

def delete_task(task_id, user_id):
    sql = text("DELETE FROM tasks WHERE id=:task_id AND user_id=:user_id")
    db.session.execute(sql, {"task_id": task_id, "user_id": user_id})
    db.session.commit()
