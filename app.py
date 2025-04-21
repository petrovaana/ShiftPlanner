import sqlite3
import secrets
import re
from datetime import datetime

from flask import Flask
from flask import abort, redirect, render_template, request, session, make_response, flash


import db
import config
import items
import missing_items
import users


app = Flask(__name__)
app.secret_key = config.secret_key

today = datetime.today().date()

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    all_items = items.get_items_indexpage()
    all_missing = missing_items.get_missing_indexpage()
    return render_template("index.html", items=all_items, missing_items=all_missing)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=user_items)

@app.route("/missing/<int:missing_id>")
def show_missing(missing_id):
    missing = missing_items.get_missings(missing_id)
    if not missing:
        abort(404)
    return render_template("show_missing.html", missing=missing)

@app.route("/new_missing")
def new_missing():
    require_login()
    if request.method == "POST":
        title = request.form["title"]
        date = request.form["date"]
        user_id = session["user_id"]
        missing_items.add_missing(title, date, user_id)
        return redirect("/")
    
    return render_template("new_missing.html")

@app.route("/create_missing", methods=["POST"])
def create_missing():
    require_login()
    check_csrf()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    date = request.form["date"]
    if not date:
        abort(403)
    try:
        input_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        abort(403)
    if input_date > today:
        abort(403)
    user_id = session["user_id"]

    missing_items.add_missing(title, date, user_id)

    return redirect("/")

@app.route("/edit_missing/<int:missing_id>")
def edit_missing(missing_id):
    require_login()
    missing = missing_items.get_missings(missing_id)
    if not missing:
        abort(404)
    if missing["user_id"] != session["user_id"]:
        abort(403)

    return render_template("edit_item.html", missing=missing)

@app.route("/remove_missing/<int:missing_id>", methods=["GET", "POST"])
def remove_missing(missing_id):
    require_login()
    missing = missing_items.get_missings(missing_id)
    if not missing:
        abort(404)
    if missing["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_missing.html", missing=missing)

    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            missing_items.remove_missing(missing_id)
            return redirect("/")
        else:
            return redirect("/missing/" + str(missing_id))

@app.route("/find_missing")
def find_missing():
    query = request.args.get("query")
    if query:
        results = missing_items.find_missing(query)
    else:
        query = ""
        results = []

    all_missing = missing_items.get_missing()
    return render_template("find_missing.html", query=query, results=results, missing_items=all_missing)

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    edits = items.get_information(item_id)
    return render_template("show_item.html", item=item, edits=edits)

@app.route("/new_item")
def new_item():
    require_login()
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        booked_space = request.form["booked_space"]
        guests = request.form["guests"]
        payment = request.form["payment"]
        start_price = request.form["start_price"]
        date = request.form["date"]
        user_id = session["user_id"]

        items.add_item(title, description, booked_space, guests, payment, start_price, date, user_id)

        return redirect("/")
    else:
        return render_template("new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
    check_csrf()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    booked_space = request.form["booked_space"]
    if not booked_space or len(booked_space) > 50:
        abort(403)
    guests = request.form["guests"]
    if not guests or int(guests) < 0:
        abort(403)
    payment = request.form["payment"]
    if not payment or len(payment) > 50:
        abort(403)
    start_price = request.form["start_price"]
    if not re.search("^[1-9][0-9]{0,4}$", start_price):
        abort(403)
    date = request.form["date"]
    if not date:
        abort(403)
    try:
        input_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        abort(403)
    if input_date < today:
        abort(403)
    user_id = session["user_id"]

    items.add_item(title, description, booked_space, guests, payment, start_price, date, user_id)

    return redirect("/")


@app.route("/create_information", methods=["POST"])
def create_information():
    require_login()
    check_csrf()

    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(403)
    user_id = session["user_id"]

    items.add_information(item_id, user_id, description)

    return redirect("/item/" + str(item_id))

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    return render_template("edit_item.html", item=item)

@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
    check_csrf()

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
    booked_space = request.form["booked_space"]
    if not booked_space or len(booked_space) > 50:
        abort(403)
    guests = request.form["guests"]
    if not guests or int(guests) < 0:
        abort(403)
    payment = request.form["payment"]
    if not payment or len(payment) > 50:
        abort(403)
    start_price = request.form["start_price"]
    if not re.search("^[1-9][0-9]{0,4}$", start_price):
        abort(403)
    date = request.form["date"]
    if not date:
        abort(403)

    items.update_item(item_id, title, description, booked_space, guests, payment, start_price, date)

    return redirect("/item/" + str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()

    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_item.html", item=item)

    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))
        
@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = items.find_items(query)
    else:
        query = ""
        results = []
    
    all_items = items.get_items()
    return render_template("find_item.html", query=query, results=results, items=all_items)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("ERROR: passwords aren't the same!")
        return redirect("/register")
    
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "ERROR: username is taken"
    flash("Account made")
    return redirect("/login")

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
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("ERROR: wrong password or username")
            return redirect("/login")
        
@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
