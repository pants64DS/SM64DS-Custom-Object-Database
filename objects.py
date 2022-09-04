from db import db
from flask import abort

columns = ["name", "creator", "rom_hack", "category", "object_id", "actor_id", "description"]
sortable_columns = ["name", "creator", "rom_hack", "object_id", "actor_id"]
searchable_columns = sortable_columns + ["description"]

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
    if column.endswith("_id"):
        if regex_enabled:
            return f"CAST ({column} AS TEXT) ~ :search_term"
        else:
            return f"CAST ({column} AS TEXT) = :search_term"

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
        sql += f"WHERE FALSE"
        for column in searchable_columns:
            sql += " OR "
            sql += __make_comparison(column, regex_enabled, case_sensitive)

    sql += " ORDER BY "
    if sortby.endswith("_id"):
        sql += sortby
    else:
        sql += f"CASE WHEN {sortby}='' THEN 1 ELSE 0 END, {sortby}"

    try:
        return db.session.execute(sql, {"search_term": search_term}).fetchall()
    except:
        return list()

def get_matches(rows, search_term, regex_enabled, case_sensitive):
    matches = {}
    if not search_term:
        return matches

    for row in rows:
        for column in searchable_columns:
            sql = "SELECT id FROM objects WHERE id=:id AND "
            sql += __make_comparison(column, regex_enabled, case_sensitive)
            res = db.session.execute(sql, {"search_term": search_term, "id": row[0]}).fetchall()

            if res:
                if row[0] not in matches:
                    matches[row[0]] = set()

                matches[row[0]].add(column)

    return matches

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

def add_object(request):
    params = {key: __get_form_value(request.form, key) for key in columns}

    if "file" in request.files:
        image_file = request.files["file"]
        image_name = image_file.filename
        image_data = image_file.read()

        sql = "INSERT INTO images (name, data) VALUES (:name, :data) RETURNING id"
        params["image"] = db.session.execute(sql, {"name":image_name, "data":image_data}).one()[0]
        columns_to_set = columns + ["image"]
    else:
        columns_to_set = columns

    sql = f"""
        INSERT INTO objects ({','.join(columns_to_set)})
        VALUES ({','.join([':' + p for p in columns_to_set])})
    """

    db.session.execute(sql, params)
    db.session.commit()

def remove_object(id):
    image = db.session.execute("SELECT (image) FROM objects WHERE id=:id", {"id": id}).fetchone()[0]
    db.session.execute("DELETE FROM objects WHERE id=:id", {"id": id})

    if image:
        db.session.execute("DELETE FROM images WHERE id=:id", {"id": image})

    db.session.commit()

def get_image(id):
    sql = "SELECT data FROM images WHERE id=:id"

    return db.session.execute(sql, {"id": id}).fetchone()[0]
