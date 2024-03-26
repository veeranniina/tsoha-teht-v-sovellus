from app import app
from flask import render_template, request, redirect, url_for, flash
#from werkzeug.security import generate_password_hash
import users
import tasks
#from helpers import generate_random_password
from db import db

#tehtävänä on käsitellä sivupyynnöt

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=["get", "post"])#kirjaudu sisään
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            return render_template("error.html", message="Väärä tunnus tai salasana")
        return redirect("/")

@app.route("/logout")#kirjaudu ulos
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])#rekisteröidy
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 15:
            return render_template("error.html", message="Tunnuksessa tulee olla 1-15 merkkiä")
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat toisistaan")
        if password1 == "":
            return render_template("error.html", message="Salasana on tyhjä")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")


@app.route("/new")#luo uusi task
def new():
    return render_template("new.html")

@app.route("/delete", methods=["get", "post"])#poista task
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

#@app.route("/forgot_password", methods=["GET", "POST"])
#def forgot_password():
    #if request.method == 'POST':
        #email = request.form['email'] 
        #tarkista onko sposti olemassa tietokannassa käyttäjän kohdalla -> LISÄÄ sarake EMAIL TIETOKANTAAN USERS
        #user = users.query.filter_by(email=email).first()   #<-----onko oikein??
        #if user:
            #luodaan uusi salasana, joka lähetetään sähköpostitse käyttäjälle
            #new_password = generate_random_password() #luodaan random salasana
            #user.password = generate_password_hash(new_password) #tallennetaan salasana tietokantaan
            #db.session.commit()
            #send_password_reset_email(user.email, new_password) #lähetetään spostia uudesta salasanasta
            #flash('Salasanan palautuslinkki lähetettiin sähköpostiisi.')
            #return redirect(url_for('login'))
        #else:
            #flash('Sähköpostiosoite ei ole rekisteröity.')

    #return render_template('forgot_password.html')


