from app import app
from flask import session, render_template, request, redirect, url_for, flash
#from werkzeug.security import generate_password_hash
import users
from tasks import *
from datetime import datetime
#from helpers import generate_random_password

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
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")
        

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
            return render_template("error.html", message="Tunnuksessa on oltava 1-15 merkkiä")
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat toisistaan")
        if password1 == "":
            return render_template("error.html", message="Salasana on tyhjä")
        if not users.register(username, password1):
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
        return redirect("/")



@app.route("/new", methods=["GET", "POST"])#luo uusi task
def new():
    if request.method == "POST":
        title = request.form["title"]    #kysyy nämä käyttäjältä
        description = request.form["description"]
        due_date = request.form["due_date"]
        priority = request.form["priority"]
        
        date = datetime.now().strftime("%Y-%m-%d %H:%M:")

        #kutsu create_task-funktiota jotta voidaan luoda uusi tehtävä tietokantaan
        if create_task(title, description, date, due_date, priority):
            # Ohjaa käyttäjä home-sivulle uuden tehtävän luomisen jälkeen
            return redirect(url_for('home'))
        else:
            #jos tehtävän luominen epäonnistuu, ohjataan käyttäjä takaisin new-sivulle
            flash("Tehtävän luominen epäonnistui.", "error")
            return redirect(url_for('new'))

    #jos HTTP-metodi on GET, renderöidään new.html-sivu
    return render_template("new.html")


@app.route("/delete", methods=["GET", "POST"])
def delete_task_route():
    #user_id = session.get("user_id")
    if request.method == "GET":
        my_tasks = get_task_list(users.user_id())
        return render_template("delete.html", list=my_tasks)
    if request.method == "POST":
        users.check_csrf()
        if "task" in request.form:
            task = request.form["task"]
            delete_task(task, users.user_id())
            message = "Muistiinpanon poistaminen onnistui!"  #asetetaan viesti
        my_tasks = get_task_list(users.user_id())  #päivitetään tehtävälista/muistiinpanot
        return render_template("home.html", tasks=my_tasks, message=message)  #lisätään viesti templateen
        #"return redirect("/") ??
    
@app.route("/home")
def home():
    user_id = users.user_id()
    if user_id == 0:
        return redirect("/")
    user_tasks = get_task_list(user_id)
    return render_template("home.html", tasks=user_tasks)

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    if request.method == "GET":
        task = get_task_from_database(task_id) 
        return render_template("edit.html", task=task)
    elif request.method == "POST":
        #käsittelee muokkauslomakkeen tiedot ja tallentaa muutokset db
        title = request.form.get("title")
        description = request.form.get("description")
        due_date = request.form.get("due_date")
        priority = request.form.get("priority")
        
        if edit_task(task_id, title, description, None, due_date, priority): #None -> ei muokata luontiaikaa
            return redirect(url_for('home')) 
        else:
            #virheenkäsittely tarvittaessa
            flash("Muokkaus epäonnistui.", "error")
            return redirect(url_for('edit'))
    return render_template("home.html")


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


