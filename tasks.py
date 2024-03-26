from db import db
import users

def get_task_list():
    user_id = users.user_id()
    if user_id == 0:
        return []
    sql = "SELECT * FROM tasks WHERE user_id=:user_id ORDER BY id DESC"
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()

def create_task(title, description, due_date, priority, status):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO tasks (user_id, title, description, due_date, priority, status) VALUES (:user_id, :title, :description, :due_date, :priority, :status)"
    db.session.execute(sql, {"user_id": user_id, "title": title, "description": description, "due_date": due_date, "priority": priority, "status": status})
    db.session.commit()
    return True

def update_task(task_id, title, description, due_date, priority, status):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try: #jos arvo on 'None', käytetään tehtävän nykyistä arvoa tietokannassa
        sql = "UPDATE tasks SET title = COALESCE(:title, title), description = COALESCE(:description, description), due_date = COALESCE(:due_date, due_date), priority = COALESCE(:priority, priority), status = COALESCE(:status, status) WHERE id = :task_id AND user_id = :user_id"
        db.session.execute(sql, {"title": title, "description": description, "due_date": due_date, "priority": priority, "status": status, "task_id": task_id, "user_id": user_id})
        db.session.commit()
        return True
    except:
        return False

def delete_task(task_id, user_id):
    sql = "UPDATE tasks SET visible=0 WHERE id=:task_id and user_id=:user_id"  #tässä mättäää
    db.session.execute(sql, {"task_id":task_id, "user_id":user_id})
    db.session.commit()
