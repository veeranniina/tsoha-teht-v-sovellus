from app import app
from flask import session, render_template, request, redirect, url_for, flash
#from werkzeug.security import generate_password_hash
from users import *
from tasks import *
from datetime import datetime
from categories import *
from reminders import *
from recycle_bin import *
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

@app.route('/profile')
def profile():
    if user_id():
        return render_template('profile.html')
    else:
        return render_template("error.html", message="Kirjaudu sisään nähdäksesi profiili")


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

@app.route("/task/<int:task_id>")
def view_task(task_id):
    task = get_task_from_database(task_id)
    return render_template("task.html", task=task)

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
            return render_template("error.html", message="Tehtävän luominen epäonnistui!")
        
    user_id = session.get("user_id")
    categories = get_categories_from_database(user_id)
    return render_template("new.html", categories=categories)


@app.route("/delete", methods=["GET", "POST"])
def delete_task_route():
    if request.method == "GET":
        my_tasks = get_task_list(users.user_id())
        return render_template("delete.html", list=my_tasks)
    if request.method == "POST":
        users.check_csrf()
        message = ""
        if "task" in request.form:
            task = request.form["task"]
            if delete_task_to_recycle_bin(task, users.user_id()):  #siirretään muistiinpano roskakoriin
                message = "Muistiinpanon poistaminen onnistui!"  
                my_tasks = get_task_list(users.user_id())
                return render_template("home.html", tasks=my_tasks, message=message)
        else:
            message = "Tehtävää ei valittu poistettavaksi."
        
        my_tasks = get_task_list(users.user_id())  #päivitetään muistiinpanot
        return render_template("home.html", tasks=my_tasks, message=message)
    
@app.route("/home", methods=["GET", "POST"])
def home():
    user_id = users.user_id()
    if user_id == 0:
        return redirect("/")
    
    if request.method == "POST":
        sort_by = request.form.get("sort_by")
        if sort_by == "priority":
            user_tasks = get_sorted_tasks_by_priority(user_id)
        elif sort_by == "date":
            user_tasks = get_sorted_tasks_by_date(user_id)
        else:
            user_tasks = get_task_list(user_id)
    else:
        user_tasks = get_task_list(user_id)

    #tarkista, onko poistetut tehtävät roskakorissa ja poista ne näkymästä
    deleted_tasks = get_deleted_tasks(user_id)
    updated_tasks = [task for task in user_tasks if task.id not in [deleted_task.id for deleted_task in deleted_tasks]]

    user_reminders = get_user_reminders(user_id)
    return render_template("home.html", tasks=updated_tasks, reminders=user_reminders)

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task_route(task_id):
    if request.method == "GET":
        task = get_task_from_database(task_id) 
        user_id = session.get("user_id")
        categories = get_categories_from_database(user_id)
        return render_template("edit.html", task=task, task_id=task_id, categories=categories)
    elif request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        due_date = request.form.get("due_date")
        priority = request.form.get("priority")
        category_id = request.form.get("category_id")

        
        if edit_task(task_id, title, description, None, due_date, priority, category_id): #None -> ei muokata luontiaikaa
            return redirect(url_for("home")) 
        else:
            return render_template("error.html", message="Muokkaus ei onnistunut", task_id=task_id)
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
            return redirect(url_for("categories_route"))
        else:
            return render_template("error.html", message="Kategorian luominen epäonnistui!")

@app.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category_route(category_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login"))

    if delete_category(category_id):
        return redirect(url_for("categories_route"))
    else:
        return render_template("error.html", message="Kategorian poisto epäonnistui!")


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
        return redirect(url_for("home"))
    else:
        render_template("error.html", message="Muistutuksen lisääminen epäonnistui!")
    return redirect(url_for("home"))

@app.route("/delete_reminder/<int:reminder_id>", methods=["POST"])
def delete_reminder_route(reminder_id):
    if delete_reminder(reminder_id):
        return redirect(url_for("home"))
    else:
        return render_template("error.html", message="Muistutuksen poistaminen epäonnistui!")
    

@app.route("/category/<int:category_id>")
def category_tasks(category_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login"))
    
    tasks = get_tasks_by_category(user_id, category_id)
    
    return render_template("category_tasks.html", tasks=tasks)

@app.route("/sort_tasks", methods=["POST"])
def sort_tasks():
    sort_by = request.form.get("sort_by")
    user_id = users.user_id()
    if user_id == 0:
        return redirect("/")
    
    if sort_by == "priority":
        tasks = get_sorted_tasks_by_priority(user_id)
    elif sort_by == "date":
        tasks = get_sorted_tasks_by_date(user_id)
    else:
        tasks = get_task_list(user_id)

    user_reminders = get_user_reminders(user_id)
    return render_template("home.html", tasks=tasks, reminders=user_reminders)

@app.route("/delete_profile", methods=["GET", "POST"])
def delete_profile_route():
    if request.method == "POST":
        user_id = session.get("user_id")
        if user_id:
            if delete_profile(user_id):
                flash("Profiilisi on poistettu.", "success")
                session.clear()  
                return redirect(url_for("index"))
            else:
                flash("Profiilin poistaminen epäonnistui.", "error")
                return redirect(url_for("profile"))
        else:
            flash("Kirjaudu sisään ennen profiilin poistamista.", "error")
            return redirect(url_for("login"))
    else:
        return redirect(url_for("index"))
    
@app.route('/recycle_bin')
def recycle_bin_view():
    user_id = session.get("user_id")
    deleted_tasks = get_deleted_tasks(user_id)
    return render_template('recycle_bin.html', deleted_tasks=deleted_tasks)

@app.route('/permanently_delete_task/<int:task_id>', methods=['POST'])
def permanently_delete_task_route(task_id):
    if request.method == 'POST':
        if permanently_delete_task(task_id):
            return redirect(url_for("recycle_bin_view"))
        else:
            return render_template("error.html", message="Muistiinpanon poistaminen pysyvästi epäonnistui.")




