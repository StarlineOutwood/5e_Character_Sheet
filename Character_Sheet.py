from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    return redirect ("/party")

@app.route("/party")
def party():
    result = db.session.execute(text('SELECT id, name, class, race, level FROM characters'))
    characters = result.fetchall()
    return render_template("party.html", hahmot = characters)

@app.route("/newC1")
def newC1():
    sql1 = 'SELECT id, class_name FROM classes'
    sql2 = 'SELECT id, race_name FROM races'
    result1 = db.session.execute(text(sql1)).fetchall()
    result2 = db.session.execute(text(sql2)).fetchall()
    return render_template("newC1.html", classes = result1, races = result2)

@app.route("/newC2", methods =["POST"])
def newC2():
    name = request.form["name"]
    race = request.form["race"]
    character_class = request.form["class"]
    level = request.form["level"]
    sql = "INSERT INTO characters (name, class, race, level) VALUES (:name, :class, :race, :level)"
    db.session.execute(text(sql), {"name":name, "class":character_class, "race":race, "level":level})
    db.session.commit()
    sql2 = "SELECT score_increases FROM races WHERE id = :race"
    increases = db.session.execute(text(sql2), {"race":race}).fetchall()
    print(increases)
    return render_template("newC2.html", score_increase = increases[0][0])

@app.route("/newC3", methods = ["POST"])
def newC3():
    wis = request.form["Wis"]
    cha = request.form["Cha"]
    intelligence = request.form["int"]
    dex = request.form["Dex"]
    con = request.form["Con"]
    str = request.form["Srt"]
    abily_scores = [wis, cha, intelligence, dex, con, str]
    abilities = ['Wis', 'Cha', 'Int', 'Dex', 'Con', 'Str']
    for i in range(6):
        sql = "INSERT INTO ability_stats (character_id, ability) VALUES (:name, :class, :race, :level)"
        db.session.execute(text(sql), {"name":name, "class":character_class, "race":race, "level":level})
        db.session.commit()


@app.route("/add", methods=["POST"])
def add():
    return redirect ("/party")

@app.route("/removeC")
def removeC():
    sql = "SELECT id, name FROM characters"
    names = db.session.execute(text(sql))
    return render_template("removeC.html", names = names)

@app.route("/remove", methods=["POST"])
def remove():
    ids = request.form.getlist["poistettava"]
    print(ids)
    for id in ids:
        sql = "DELETE FROM characters WHERE id = :poistettava"
        db.session.execute(text(sql), {"poistettava":id})
        db.session.commit()
    return redirect ("/party")

@app.route("/hahmo/<int:character_id>")
def info(character_id):
    sql = "SELECT name, race, class, level FROM characters WHERE id = :id"
    info = db.session.execute((text(sql)), {"id":character_id}).fetchall()
    print("TÄSSÄ TULEVAT HAHMON TIEDOT")
    print(info)
    name = info[0][0]
    race_id = info[0][1]
    character_class_id = info[0][2]
    level = info[0][3]
    character_class = db.session.execute((text("SELECT class_name FROM classes WHERE id = :class_id")), {"class_id":character_class_id}).fetchone()
    race = db.session.execute((text("SELECT race_name FROM races WHERE id = :race_id")), {"race_id":race_id}).fetchone()
    return render_template("hahmo.html", name = name, race = race[0], character_class= character_class[0], level = level)