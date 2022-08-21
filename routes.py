from flask import request, redirect, render_template
from app import app
import objects

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

@app.route("/add")
def add_object():
    return render_template("new_object.html")

@app.route("/send", methods=["GET", "POST"])
def send():
    objects.add_object(request.form)
    return redirect("/")

@app.route("/remove=<id>")
def remove_object(id):
    objects.remove_object(id)

    return redirect("/")
