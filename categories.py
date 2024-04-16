from db import db
from sqlalchemy.sql import text
import users

def create_category(category_name):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        sql = text("INSERT INTO categories (user_id, name) VALUES (:user_id, :category_name)")
        db.session.execute(sql, {"user_id": user_id, "category_name": category_name})
        db.session.commit()
        return True
    except:
        return False

def edit_category(category_id, category_name):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        sql = text("UPDATE categories SET name = :category_name WHERE id = :category_id AND user_id = :user_id")
        db.session.execute(sql, {"category_name": category_name, "category_id": category_id, "user_id": user_id})
        db.session.commit()
        return True
    except:
        return False