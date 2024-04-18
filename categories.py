from db import db
from sqlalchemy.sql import text
import users

def create_category(name):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        sql = text("INSERT INTO categories (user_id, name) VALUES (:user_id, :name)")
        db.session.execute(sql, {"user_id": user_id, "name": name})
        db.session.commit()
        return True
    except:
        return False

def edit_category(id, name):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        sql = text("UPDATE categories SET name = :name WHERE id = :id AND user_id = :user_id")
        db.session.execute(sql, {"name": name, "id": id, "user_id": user_id})
        db.session.commit()
        return True
    except:
        return False
    
def get_categories_from_database():
    sql = text("SELECT id, user_id, name FROM categories")  #muokkaa tätä
    result = db.session.execute(sql)
    categories = result.fetchall()
    return categories