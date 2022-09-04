from flask import request, redirect, render_template, flash
from flask import session, abort
from app import app
import objects
import users

def __check_crsf_token(form):
    try:
        if session["csrf_token"] == form["csrf_token"]:
            return
    except:
        pass

    abort(403)

def __is_null(x):
    if type(x) is str:
        return not x

    return x is None

@app.route("/")
def index():
    if "sortby" in request.args:
        sortby = request.args["sortby"]
    else:
        sortby = "name"

    return render_template(
        "index.html",
        objects=objects.get_all(sortby),
        columns=objects.columns,
        sortable_columns=objects.sortable_columns,
        column_display_names=objects.column_display_names,
        is_null=__is_null,
        sortby=sortby
    )

@app.route("/view=<id>")
def view_object(id):
    return render_template("view_object.html", obj=objects.get_by_id(id), is_null=__is_null)

@app.route("/add", methods=["GET", "POST"])
def add_object():
    if "username" not in session:
        abort(403)

    if request.method == "GET":
        return render_template("new_object.html")

    __check_crsf_token(request.form)

    objects.add_object(request.form)
    return redirect("/")

@app.route("/remove=<id>", methods=["POST"])
def remove_object(id):
    __check_crsf_token(request.form)

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
