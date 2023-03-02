from db import db
from sqlalchemy.sql import text

def add_user(username, password):
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(text(sql), {"username": username, "password": password})
    db.session.commit()
    return

def log_in(username, password):
    sql = "SELECT id FROM users WHERE username = :username AND password = :password"
    tulos = db.session.execute(text(sql), {"username":username, "password": password}).fetchone()
    return tulos

