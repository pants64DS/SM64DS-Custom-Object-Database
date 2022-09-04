from db import db
from flask import abort

columns = ["name", "creator", "rom_hack", "category", "object_id", "actor_id", "description"]
sortable_columns = ["name", "creator", "rom_hack", "object_id", "actor_id"]

column_display_names = {
    "name": "Name",
    "creator": "Creator",
    "rom_hack": "ROM Hack",
    "object_id": "Object ID",
    "actor_id": "Actor ID",
    "category": "Category",
    "description": "Description"
}

def get_all(sortby):
    # Check if the column name is valid to prevent SQL injection
    if sortby not in sortable_columns:
        abort(403)

    # Since there doesn't seem to be a way to pass a column name to
    # ORDER BY using a dictionary, a format string is used instead
    if sortby.endswith("_id"):
        sql = f"SELECT * FROM objects ORDER BY {sortby}"
    else:
        sql = f"SELECT * FROM objects ORDER BY CASE WHEN {sortby}='' THEN 1 ELSE 0 END, {sortby}"

    return db.session.execute(sql).fetchall()

def get_by_id(id):
    sql = "SELECT * FROM objects WHERE id=:id"

    return db.session.execute(sql, {"id": id}).fetchone()

def __get_form_value(form, key):
    value = form[key]

    if not key.endswith("_id"):
        return value

    if value:
        try:
            return int(value)
        except:
            pass
    return None

def add_object(form):
    sql = f"""
        INSERT INTO objects ({','.join(columns)})
        VALUES ({','.join([':' + p for p in columns])})
    """

    newObject = {key : __get_form_value(form, key) for key in columns}

    db.session.execute(sql, newObject)
    db.session.commit()

def remove_object(id):
    db.session.execute("DELETE FROM objects WHERE id=:id", {"id": id})
    db.session.commit()
