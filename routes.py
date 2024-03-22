from app import app
from flask import render_template, request, redirect
import users
import tasks

#tehtävänä on käsitellä sivupyynnöt

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Väärä tunnus tai salasana")
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="Tunnuksessa tulee olla 1-15 merkkiä")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if password1 == "":
            return render_template("error.html", message="Salasana on tyhjä")

        role = request.form["role"]
        if role not in ("1", "2"):
            return render_template("error.html", message="Tuntematon käyttäjärooli")

        if not users.register(username, password1, role):
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
        return redirect("/")


@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/delete", methods=["get", "post"])
def remove_deck():
    users.require_role(2)

    if request.method == "GET":
        my_tasks = tasks.get_task_list(users.user_id())  
        return render_template("remove.html", list=my_tasks) 

    if request.method == "POST":
        users.check_csrf()

        if "deck" in request.form:
            deck = request.form["deck"]
            tasks.delete_task(deck, users.user_id())   

        return redirect("/")
