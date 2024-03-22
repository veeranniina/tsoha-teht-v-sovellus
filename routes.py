from app import app
from flask import render_template, request, redirect
import users

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # TODO: check username and password
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")