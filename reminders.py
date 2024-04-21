from db import db
from sqlalchemy.sql import text
import users

def add_reminder(user_id, task_id, reminder_date, reminder_message):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        sql = text("INSERT INTO reminders (user_id, task_id, reminder_date, reminder_message) VALUES (:user_id, :task_id, :reminder_date, :reminder_message)")
        db.session.execute(sql, {"user_id": user_id, "task_id": task_id, "reminder_date": reminder_date, "reminder_message": reminder_message})
        db.session.commit()
        return True
    except:
        return False

def delete_reminder(reminder_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        sql = text("DELETE FROM reminders WHERE id = :reminder_id")
        db.session.execute(sql, {"reminder_id": reminder_id})
        db.session.commit()
        return True
    except:
        return False

def get_user_reminders(user_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        sql = text("SELECT id, user_id, task_id, reminder_date, reminder_message FROM reminders WHERE user_id = :user_id")
        result = db.session.execute(sql, {"user_id": user_id})
        reminders = result.fetchall()
        return reminders
    except:
        return []