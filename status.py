from db import db
from sqlalchemy.sql import text
import users

def create_status(user_id, name):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO status (user_id, name) VALUES (:user_id, :name)")
    db.session.execute(sql, {"user_id": user_id, "name": name})
    db.session.commit()
    return True

def edit_status(status_id, name):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try: #jos arvo on 'None', käytetään tehtävän nykyistä arvoa tietokannassa
        sql = text("UPDATE status SET name = :name WHERE id = :status_id")
        db.session.execute(sql, {"status_id": status_id, "name": name})
        db.session.commit()
        return True
    except:
        return False
    
def delete_status(status_id, user_id):
    sql = text("DELETE FROM status WHERE id=:status_id AND user_id=:user_id")
    db.session.execute(sql, {"status_id": status_id, "user_id": user_id})
    db.session.commit()