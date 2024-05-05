from db import db
from sqlalchemy.sql import text

def get_deleted_tasks(user_id):
    try:
        sql = text("SELECT DISTINCT tasks.id, title, description, to_char(recycle_bin.deletion_timestamp, 'YYYY-MM-DD HH24:MI') AS deletion_time FROM tasks JOIN recycle_bin ON tasks.id = recycle_bin.task_id WHERE tasks.user_id=:user_id")
        result = db.session.execute(sql, {"user_id": user_id})
        deleted_tasks = result.fetchall()
        return deleted_tasks
    except:
        return []

def permanently_delete_task(task_id):
    try:
        sql_delete_reminders = text("DELETE FROM reminders WHERE task_id=:task_id")
        db.session.execute(sql_delete_reminders, {"task_id": task_id})

        sql_delete_recycle_bin = text("DELETE FROM recycle_bin WHERE task_id=:task_id")
        db.session.execute(sql_delete_recycle_bin, {"task_id": task_id})

        sql_delete_task = text("DELETE FROM tasks WHERE id=:task_id")
        db.session.execute(sql_delete_task, {"task_id": task_id})

        db.session.commit()
        return True
    except Exception as e:
        print(f"Error deleting task: {e}")
        db.session.rollback()
        return False