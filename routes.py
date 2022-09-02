from flask import request, redirect, render_template, flash
from flask import session, abort
from app import app
import objects
import users

def __get_display_string(x):
    if x is None or (type(x) is str and not x):
        return '–'
    return x

@app.route("/")
def index():
    return render_template(
        "index.html",
        objects=objects.get_all(),
        columns=objects.columns,
        get_display_string=__get_display_string
    )

@app.route("/add", methods=["GET", "POST"])
def add_object():
    if "username" not in session:
        abort(403)

    if request.method == "GET":
        return render_template("new_object.html")

    objects.add_object(request.form)
    return redirect("/")

@app.route("/remove=<id>")
def remove_object(id):
    if not session["is_admin"]:
        abort(403)

    objects.remove_object(id)
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if users.register(request.form["username"], request.form["password"]):
        return redirect("/")

    flash("Could not create account. Please try again with a different username.")

    return redirect("/register")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if users.login(request.form["username"], request.form["password"]):
        return redirect("/")

    flash("Could not log in. Please make sure the username and password are correct.")

    return redirect("/login")

@app.route("/logout")
def logout():
    users.logout()

    return redirect("/")
