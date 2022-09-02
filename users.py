from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import exc
from db import db
import traceback

def register(username, password):
    try:
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except exc.IntegrityError:
        return False

    session["username"] = username
    session["is_admin"] = False

    return True

def login(username, password):
    sql = "SELECT id, password, is_admin FROM users WHERE username=:username"
    user = db.session.execute(sql, {"username": username}).fetchone()

    if user and check_password_hash(user.password, password):
        session["username"] = username
        session["is_admin"] = user.is_admin
        return True

    return False

def logout():
    del session["username"]
    del session["is_admin"]
