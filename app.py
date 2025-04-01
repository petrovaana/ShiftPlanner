import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import db
import config
import items
import puuttuvat


app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_items = items.get_yksarit()
    return render_template("index.html", items=all_items)

#Puuttuvien tuotteiden kirjaus
#Mikä tos pitäis olla?
@app.route("/item/<int:item_id>")
def show_puuttuva(item_id):
    item = puuttuvat.get_puuttuva(item_id)
    return render_template("show_puuttuva.html", item=item)

@app.route("/new_puuttuva")
def new_puuttuva():
    return render_template("new_puuttuva.html")

@app.route("/create_puuttuva", methods=["POST"])
def create_puuttuva():
    tuote = request.form["tuote"]
    paiva = request.form["paiva"]

    puuttuvat.add_puuttuva(tuote, paiva)

    return redirect("/")

#Yksärien kirjaus
@app.route("/item/<int:item_id>")
def show_yksari(item_id):
    item = items.get_yksari(item_id)
    return render_template("show_item.html", item=item)

@app.route("/new_yksari")
def new_yksari():
    return render_template("new_item.html")

@app.route("/create_yksari", methods=["POST"])
def create_yksari():
    title = request.form["title"]
    description = request.form["description"]
    start_price = request.form["start_price"]
    pvm = request.form["pvm"]
    user_id = session["user_id"]

    items.add_yksari(title, description, start_price, pvm, user_id)

    return redirect("/")

#yksarin muokkaukseen
@app.route("/edit_yksari/<int:item_id>")
def edit_yksari(item_id):
    item = items.get_yksari(item_id)
    return render_template("edit_yksari.html", item=item)

@app.route("/update_yksari", methods=["POST"])
def update_yksari():
    item_id = request.form["item_id"]
    title = request.form["title"]
    description = request.form["description"]
    start_price = request.form["start_price"]
    pvm = request.form["pvm"]

    items.update_yksari(item_id, title, description, start_price, pvm)

    return redirect("/item/" + str(item_id))

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
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus on luotu!"

#sisään kirjautuminen
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"
        
#uloskirjautuminen
@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")