from db import db
from sqlalchemy.sql import text
import users

def create_category(name):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        #tarkistetaan että poistettava kategoria kuuluu käyttäjälle
        sql_check = text("SELECT id FROM categories WHERE user_id = :user_id AND name = :name")
        result = db.session.execute(sql_check, {"user_id": user_id, "name": name})
        existing_category = result.fetchone()
        if existing_category:
            return False  
        
        #lisätään tietokantaan
        sql_insert = text("INSERT INTO categories (user_id, name) VALUES (:user_id, :name)")
        db.session.execute(sql_insert, {"user_id": user_id, "name": name})
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
    
def get_categories_from_database(user_id):
    sql = text("SELECT id, user_id, name FROM categories WHERE user_id = :user_id")
    result = db.session.execute(sql, {"user_id": user_id})
    categories = result.fetchall()
    return categories
    

def delete_category(category_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        #tarkistetaan että poistettava kategoria kuuluu käyttäjälle
        sql_check = text("SELECT id FROM categories WHERE id = :category_id AND user_id = :user_id")
        result = db.session.execute(sql_check, {"category_id": category_id, "user_id": user_id})
        existing_category = result.fetchone()
        if not existing_category:
            return False  

        #poistetaan kategoria
        sql_delete = text("DELETE FROM categories WHERE id = :category_id")
        db.session.execute(sql_delete, {"category_id": category_id})
        db.session.commit()
        return True
    except:
        return False
    
def get_tasks_by_category(user_id, category_id):
    sql = text("SELECT title, description FROM tasks WHERE user_id = :user_id AND category_id = :category_id")
    result = db.session.execute(sql, {"user_id": user_id, "category_id": category_id})
    tasks = result.fetchall()
    return tasks