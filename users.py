from db import db
from flask import session, request, abort
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text


def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")  #???toimiiko
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            return True
        else:
            return False

def logout():
    del session["user_id"]

def register(username, password):    #role???
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)") #role???
        db.session.execute(sql, {"username":username, "password":hash_value}) #"role":role
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)