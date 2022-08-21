from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

def getDisplayString(x):
	if x is None or (type(x) is str and not x):
		return '–'
	else:
		return x

columns = ["name", "creator", "rom_hack", "category", "object_id", "actor_id", "description"]

@app.route("/")
def index():
	objects = db.session.execute("SELECT * FROM objects").fetchall()

	return render_template("index.html", objects=objects, columns=columns, getDisplayString=getDisplayString)

@app.route("/add")
def addCommand():
	return render_template("new_object.html")

def getFormValue(key):
	value = request.form[key]

	if not key.endswith("_id"):
		return value

	if value:
		try:
			return int(value)
		except:
			pass
	return None

@app.route("/send", methods=["GET", "POST"])
def send():
	insert = f"INSERT INTO objects ({','.join(columns)}) VALUES ({','.join([':' + p for p in columns])})"
	newObject = {key : getFormValue(key) for key in columns}

	db.session.execute(insert, newObject)
	db.session.commit()

	return redirect("/")

@app.route("/remove=<id>")
def removeCommand(id):
	db.session.execute(f"DELETE FROM objects WHERE id={id}")
	db.session.commit()

	return redirect("/")
