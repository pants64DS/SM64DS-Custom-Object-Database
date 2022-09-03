from db import db

columns = ["name", "creator", "rom_hack", "category", "object_id", "actor_id", "description"]

def get_all():
    return db.session.execute("SELECT * FROM objects").fetchall()

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
