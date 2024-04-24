import os
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
import secrets


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
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False
        

def logout():
    session.pop("user_id", None)  
    session.pop("username", None)  
    session.pop("csrf_token", None)

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

def generate_csrf_token():
    session["csrf_token"] = secrets.token_hex(16)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
        # jos csrf_token on väärä, sivun käsittely katkeaa ja tuloksena on HTTP-virhekoodi 
        #403 (Forbidden). Koska hyökkääjä ei tiedä, mikä csrf_token liittyy käyttäjän istuntoon, 
        #tämä estää tehokkaasti CSRF-haavoittuvuuden.

def delete_profile(user_id):
    user_id = session.get("user_id")
    if user_id:
        try:
            sql = text("DELETE FROM users WHERE id=:user_id")
            db.session.execute(sql, {"user_id": user_id})
            db.session.commit()
            session.clear()  
            return True
        except:
            return False
    return False