from db import db
from sqlalchemy.sql import text

def get_classes():
    sql = 'SELECT id, class_name FROM classes'
    classes = db.session.execute(text(sql)).fetchall()
    return classes

def get_races():
    sql = 'SELECT id, race_name FROM races'
    races = db.session.execute(text(sql)).fetchall()
    return races

def race(id):
    sql = "SELECT * FROM races WHERE id = :id"
    info = db.session.execute(text(sql), {"id":id}).fetchone()
    return info

def get_class(id):
    sql = "SELECT * FROM classes WHERE id = :id"
    info = db.session.execute(text(sql), {"id":id}).fetchone()
    return info
    