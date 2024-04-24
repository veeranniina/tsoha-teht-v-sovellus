from db import db
from sqlalchemy.sql import text
import users

def get_statuses():
    sql = text("SELECT id, name FROM status")
    result = db.session.execute(sql)
    return [{"id": row[0], "name": row[1]} for row in result]

def edit_status(status_id, name):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try: 
        sql = text("UPDATE status SET name = :name WHERE id = :status_id")
        db.session.execute(sql, {"status_id": status_id, "name": name})
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error editing status: {e}")
        return False
    
#def delete_status(status_id, user_id):
 #   try:
  #      sql = text("DELETE FROM status WHERE id=:status_id AND user_id=:user_id")
   #     db.session.execute(sql, {"status_id": status_id, "user_id": user_id})
    #    db.session.commit()
     #   return True
    #except Exception as e:
     #   print(f"Error deleting status: {e}")
      #  return False
