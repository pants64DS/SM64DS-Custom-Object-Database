from flask import Flask, request, redirect

app = Flask(__name__)

def stringOrNone(string):
	if string:
		return string
	else:
		return None

def integerOrNone(string, radix = 10):
	if string:
		try:
			return int(string, radix)
		except:
			return -1
	else:
		return -1

class Object:
	def __init__(self, form):
		self.name        = stringOrNone(form["name"])
		self.creator     = stringOrNone(form["creator"])
		self.romHack     = stringOrNone(form["romHack"])
		self.category    = stringOrNone(form["category"])
		self.objectID    = integerOrNone(form["objectID"])
		self.actorID     = integerOrNone(form["actorID"])
		self.description = stringOrNone(form["description"])

objects = []

head = '''
<head>
	<style>
		table, th, td { border: 1px solid #c08080; }
		body {background-color: #202040; color: #ffe0e0}
		input {background-color: #202040; color: #ffe0e0;}
		textarea {background-color: #202040; color: #ffe0e0;}
		select {background-color: #202040; color: #ffe0e0;}
	</style>
	<title>
		SM64DS Custom Object Database
	</title>
</head>
'''

tableHeader = '''
<th>Name</th>
<th>Creator</th>
<th>ROM Hack</th>
<th>Category</th>
<th>Object ID</th>
<th>Actor ID</th>
<th>Description</th>'''

newObjectButton = '''
<form action="/add" method="GET">
<input type="submit" value="Add new object">
</form>
'''

def getDisplayID(x):
	if x == -1:
		return '–'
	else:
		return x

def getDisplayString(s):
	if s:
		return s
	else:
		return '–'

@app.route("/")
def index():
	res = "<!DOCTYPE html><table><html>"
	res += "<h1>SM64DS Custom Object Database</h1>"
	res += head
	res += "<body>"
	res += tableHeader

	for i, obj in enumerate(objects):
		res += "<tr>"
		res += f"<td>{getDisplayString(obj.name)}</td>"
		res += f"<td>{getDisplayString(obj.creator)}</td>"
		res += f"<td>{getDisplayString(obj.romHack)}</td>"
		res += f"<td>{getDisplayString(obj.category)}</td>"
		res += f"<td>{getDisplayID(obj.objectID)}</td>"
		res += f"<td>{getDisplayID(obj.actorID)}</td>"
		res += f"<td>{getDisplayString(obj.description)}</td>"

		res += f'''
			<td>
			<form action="/remove={i}" method="GET">
			<input type=\"submit\" value=\"Remove\" onclick=\"return confirm('Are you sure you want to remove \\'{obj.name}\\'?')\">
			</form>
			</td></tr>
		'''

	res += "</table><br>"
	res += newObjectButton
	res += "</body></html>"

	return res

newObjectForm = "<!DOCTYPE html>" + head + '''
<h3>New Object</h3>
<form action="/send" method="POST">

Name:
<input type="text" name="name" required>
<br><br>
Creator:
<input type="text" name="creator">
<br><br>
ROM Hack:
<input type="text" name="romHack">
<br><br>
<label>Category:</label>
<select name="category">
	<option>Enemy</option>
	<option>Platform</option>
	<option>Item</option>
	<option selected>Misc.</option>
</select>
<br><br>
Object ID:
<input type="number" name="objectID">
<br><br>
Actor ID:
<input type="number" name="actorID">
<br><br>
Description:
<br>
<textarea rows = "5" cols = "60" name="description">
</textarea>
<br><br>
<input type="submit" value="Add">
</form>
'''

@app.route("/add")
def addCommand():
	return newObjectForm

@app.route("/send", methods=["GET", "POST"])
def send():
	newObject = Object(request.form)
	if newObject.name:
		objects.append(newObject)

	return redirect("/")

@app.route("/remove=<i>")
def removeCommand(i):
	if objects: objects.pop(int(i))
	return redirect("/")
