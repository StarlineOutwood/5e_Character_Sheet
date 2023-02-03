from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2:///rktuovin?host=/home/rktuovin/pgsql/sock"
db = SQLAlchemy(app)

@app.route("/")
def index():
    return redirect ("/party")

@app.route("/party")
def party():
    result = db.session.execute(text('SELECT name, class, race, level FROM characters'))
    characters = result.fetchall()
    return render_template("party.html", hahmot = characters)

@app.route("/newC")
def newC():
    return render_template("newC.html")

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    race = request.form["race"]
    character_class = request.form["Class"]
    level = request.form["level"]
    sql = "INSERT INTO characters (name, class, race, level) VALUES (:name, :class, :race, :level)"
    db.session.execute(text(sql), {"name":name, "class":character_class, "race":race, "level":level})
    db.session.commit()
    return redirect ("/party")

@app.route("/removeC")
def removeC():
    print("täällä ollaan")
    return render_template("removeC.html")

@app.route("/remove", methods=["POST"])
def remove():
    print("täällä ollaan")
    name = request.form["poistettava"]
    sql = "DELETE FORM characters WHERE name = :poistettava"
    db.session.execute(text(sql), {"poistettava":name})
    db.session.commit()
    return redirect ("/party")

@app.route("/info", methods=["POST"])
def info():
    name = request.form["name"]
    race = request.form["race"]
    character_class = request.form["Class"]
    level = request.form["level"]
    return render_template("info.html", name=name, race=race, Class=character_class, level=level)