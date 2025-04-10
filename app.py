import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import db
import config
import items
import re
import users


app = Flask(__name__)
app.secret_key = config.secret_key


def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_items = items.get_item()
    return render_template("index.html", items=[all_items])

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(403)
    items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=items)

#Yksärien kirjaus
@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    classes = items.get_classes(item_id)
    muokkaukset = items.get_tiedot(item_id)
    return render_template("show_item.html", item=item, classes=classes, muokkaukset=muokkaukset)

@app.route("/new_item")
def new_item():
    require_login()
    classes = items.get_all_classes()
    return render_template("new_item.html", classes=classes)

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    start_price = request.form["start_price"]
    if not re.search("^[1-9][0-9]{0,4}$", start_price):
        abort(403)
    pvm = request.form["pvm"]
    if not pvm:
        abort(403)
    user_id = session["user_id"]

    all_classes = items.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    items.add_item(title, description, start_price, pvm, user_id, classes)

    return redirect("/")


@app.route("/create_tiedot", methods=["POST"])
def create_tiedot():
    require_login()

    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(403)
    user_id = session["user_id"]

    items.add_tiedot(item_id, user_id, description)

    return redirect("/item/" + str(item_id))


#yksarin muokkaukseen
@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    all_classes = items.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in items.get_classes(item_id):
        classes[entry["title"]] = entry["value"]
    return render_template("edit_item.html", item=item, classes=classes, all_classes=all_classes)

@app.route("/update_item", methods=["POST"])
def update_item():
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    tila = request.form["tila"]
    if not tila or len(tila) > 50:
        abort(403)
    pax = request.form["pax"]
    if not pax:
        abort(403)
    maksutapa = request.form["maksutapa"]
    if not maksutapa or len(maksutapa) > 50:
        abort(403)
    start_price = request.form["start_price"]
    if not re.search("^[1-9][0-9]{0,4}$", start_price):
        abort(403)
    pvm = request.form["pvm"]
    if not pvm:
        abort(403)

    classes = []
    all_classes = items.get_all_classes()
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

            

    items.update_item(item_id, title, description, tila, pax, maksutapa, start_price, pvm, classes)

    return redirect("/item/" + str(item_id))

#Yksärin poisto:
@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()
    #Tarkistaa käyttäjän
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_item.html", item=item)

    if request.method == "POST":
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))
        
#yksärin etsiminen:
@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = items.find_items(query)
    else:
        query = ""
        results = []
    return render_template("index.html", query=query, results=results)

#Rekisteröinti
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"
    return "Tunnus on luotu"

#sisään kirjautuminen
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"
        
#uloskirjautuminen
@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")