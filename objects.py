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

def __make_comparison(column, regex_enabled, case_sensitive):
    if regex_enabled:
        if case_sensitive:
            return f"{column} ~ :search_term"
        else:
            return f"LOWER({column}) ~ LOWER(:search_term)"

    if case_sensitive:
        return f"POSITION(:search_term in {column}) > 0"
    else:
        return f"POSITION(LOWER(:search_term) in LOWER({column})) > 0"

def get_all(sortby, search_term, regex_enabled, case_sensitive):
    # Check if the column name is valid to prevent SQL injection
    if sortby not in sortable_columns:
        abort(403)

    sql = "SELECT * FROM objects "

    if search_term:
        sql += f"""
            WHERE {__make_comparison("name", regex_enabled, case_sensitive)}
            OR    {__make_comparison("creator", regex_enabled, case_sensitive)}
            OR    {__make_comparison("rom_hack", regex_enabled, case_sensitive)}
            OR CAST (object_id AS TEXT) {"~" if regex_enabled else "=" } :search_term
            OR CAST (actor_id  AS TEXT) {"~" if regex_enabled else "=" } :search_term
            OR    {__make_comparison("description", regex_enabled, case_sensitive)}
        """

    sql += "ORDER BY "
    if sortby.endswith("_id"):
        sql += sortby
    else:
        sql += f"CASE WHEN {sortby}='' THEN 1 ELSE 0 END, {sortby}"

    try:
        return db.session.execute(sql, {"search_term": search_term}).fetchall()
    except:
        return list()

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
