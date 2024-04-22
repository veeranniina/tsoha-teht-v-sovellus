from app import app
from flask import session, render_template, request, redirect, url_for, flash
#from werkzeug.security import generate_password_hash
import users
from tasks import *
from datetime import datetime
from categories import *
from reminders import *
#from helpers import generate_random_password

#tehtävänä on käsitellä sivupyynnöt

@app.route("/")
def index():
    user_id = users.user_id()
    if user_id == 0:
        return redirect("/login")

    user_reminders = get_user_reminders(user_id)
    return render_template("index.html", reminders=user_reminders)

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



@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        title = request.form["title"]    #kysyy nämä käyttäjältä
        description = request.form["description"]
        due_date = request.form["due_date"]
        priority = request.form["priority"]
        category_id = request.form["category"]

        
        date = datetime.now().strftime("%Y-%m-%d %H:%M:")

        user_id = session.get("user_id")

        if category_id == "":
            category_id = 1

        #kutsu create_task-funktiota jotta voidaan luoda uusi tehtävä tietokantaan
        if create_task(title, description, date, due_date, priority, category_id):
            return redirect(url_for('home'))
        else:
            flash("Tehtävän luominen epäonnistui.", "error")
            return redirect(url_for('new'))
        
    user_id = session.get("user_id")
    categories = get_categories_from_database(user_id)
    return render_template("new.html", categories=categories)


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
    user_reminders = get_user_reminders(user_id)
    return render_template("home.html", tasks=user_tasks, reminders=user_reminders)

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task_route(task_id):
    if request.method == "GET":
        task = get_task_from_database(task_id) 
        return render_template("edit.html", task=task, task_id=task_id)
    elif request.method == "POST":
        #käsittelee muokkauslomakkeen tiedot ja tallentaa muutokset db
        title = request.form.get("title")
        description = request.form.get("description")
        due_date = request.form.get("due_date")
        priority = request.form.get("priority")
        category_id = request.form.get("category_id")
        
        if edit_task(task_id, title, description, None, due_date, priority, category_id): #None -> ei muokata luontiaikaa
            message = "Muokkaus onnistui!"
            return render_template("home.html", message=message)
        else:
            #virheenkäsittely tarvittaessa
            flash("Muokkaus epäonnistui.", "error")
            return redirect(url_for('edit_task', task_id=task_id))
    return render_template("home.html")

@app.route("/categories", methods=["GET", "POST"])
def categories_route():
    if request.method == "GET": #hae kategoriat tietokannasta
        user_id = session.get("user_id")
        if user_id is None:
            return redirect(url_for("login"))
        categories = get_categories_from_database(user_id)
        return render_template("categories.html", categories=categories)
    elif request.method == "POST":
        name = request.form.get("name")
        if create_category(name):
            flash("Uusi kategoria luotu onnistuneesti!", "success")
        else:
            flash("Kategorian luominen epäonnistui!", "error")
        return redirect(url_for("categories_route"))

@app.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category_route(category_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login"))

    if delete_category(category_id):
        flash("Kategoria poistettiin onnistuneesti!", "success")
    else:
        flash("Kategorian poisto epäonnistui!", "error")

    return redirect(url_for("categories_route"))


@app.route('/add_reminder', methods=['GET', 'POST'])
def add_reminder_route():
    if request.method == 'GET':
        user_id = session.get("user_id")
        if user_id is None:
            return redirect(url_for("login"))

        tasks = get_task_list(user_id)  
        return render_template('add_reminder.html', tasks=tasks)
    
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login"))

    task_id = request.form.get("task_id")
    reminder_date = request.form.get("reminder_date")
    reminder_message = request.form.get("reminder_message")

    if add_reminder(user_id, task_id, reminder_date, reminder_message):
        flash("Muistutus lisättiin onnistuneesti", "success")
    else:
        flash("Muistutuksen lisääminen epäonnistui", "error")

    return redirect(url_for("home"))

@app.route("/delete_reminder/<int:reminder_id>", methods=["POST"])
def delete_reminder_route(reminder_id):
    if delete_reminder(reminder_id):
        flash("Muistutus poistettiin onnistuneesti", "success")
    else:
        flash("Muistutuksen poistaminen epäonnistui", "error")
    return redirect(url_for("home"))

@app.route("/category/<int:category_id>")
def category_tasks(category_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login"))
    
    tasks = get_tasks_by_category(user_id, category_id)
    
    return render_template("category_tasks.html", tasks=tasks)

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


